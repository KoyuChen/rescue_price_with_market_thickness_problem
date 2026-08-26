#!/usr/bin/env python3
"""Deterministic falsification runner for discounted incumbent payoffs.

Examples
--------
    PYTHONPATH=code python code/run_discount_falsification.py --quick
    PYTHONPATH=code python code/run_discount_falsification.py --full

The JSON output reports searches, not proofs.  High-precision brackets and
exact limiting candidates are emitted separately from exploratory grids.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from typing import Any

import numpy as np

from discount_model import (
    DiscountParams,
    completion,
    corrected_local_coefficient,
    cutoff_residual,
    find_equilibria,
    flat_completion,
    geometry_point,
    isolate_equilibria_mp,
    mp,
    mp_completion,
    mp_cover,
    mp_geometry_point,
    mp_cutoff_residual,
    mpf,
    old_local_coefficient,
    optimize_flat_noentry,
    optimize_geometry,
    pessimistic_value,
    rider_response,
)


SEED = 20260825


def jsonable(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 45)
    if hasattr(x, "__dict__"):
        return jsonable(vars(x))
    return x


def mp_flat_noentry(m: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    x = mp.findroot(lambda z: mp.expm1(z) + z - m, m / 2 if m < 1 else mp.log1p(m))
    p = x / m
    return p, (1 - p) * mp_cover(x)


def formula_checks(full: bool) -> dict[str, Any]:
    rng = np.random.default_rng(SEED)
    n = 20_000 if full else 1_000
    max_residual = 0.0
    max_completion_error = 0.0
    ordering_failures = []
    for _ in range(n):
        par = DiscountParams(
            10 ** rng.uniform(-5, 6),
            10 ** rng.uniform(-8, 0),
            rng.uniform(0.01, 0.99),
            0.0,
            10 ** rng.uniform(-6, 0),
        )
        a = par.beta * rng.random()
        point = geometry_point(a, par)
        if not (a - 2e-12 <= point.p <= point.q + 4e-12 <= par.beta + 6e-12):
            ordering_failures.append((par, point))
        if par.m * a < 600:
            max_residual = max(max_residual, abs(cutoff_residual(a, point.p, point.q, par)))
            max_completion_error = max(
                max_completion_error,
                abs(completion(a, point.p, point.q, par) - point.value),
            )

    local_cases = [
        (DiscountParams(2, 0.8, 0.7, 0, 0.5), 0.3),
        (DiscountParams(0.1, 1, 0.9, 0, 0.1), 0.3),
        (DiscountParams(2, 0.8, 0.8, 0.3, 0.5), 0.3),
        (DiscountParams(0.3, 0.5, 0.9, 2, 0.2), 0.3),
    ]
    eps = 1e-7
    local = []
    for par, p in local_cases:
        value, eq, _ = pessimistic_value(p, p + eps, par, grid_size=201)
        corrected = corrected_local_coefficient(p, par)
        quotient = (value - flat_completion(p, par)) / eps
        local.append({
            "params": par,
            "p": p,
            "corrected": corrected,
            "old_delta_1_formula": old_local_coefficient(p, par),
            "quotient_eps_1e-7": quotient,
            "relative_error": (quotient - corrected) / corrected,
            "cutoffs": eq.cutoffs,
        })

    # The flat cutoff should remain exactly p for every admissible delta.
    flat_bad = []
    flat_count = 0
    ds = [1, 0.5, 0.01, 1e-6]
    ms = [1e-4, 0.1, 10, 1e4]
    alphas = [0, 0.01, 0.5, 1]
    betas = [0.1, 0.5, 0.9]
    gammas = [0, 0.1, 10]
    ps = [0.01, 0.2, 0.7, 0.95]
    for d, m, alpha, beta, gamma, p in itertools.product(ds, ms, alphas, betas, gammas, ps):
        par = DiscountParams(m, alpha, beta, gamma, d)
        eq = find_equilibria(p, p, par, grid_size=65)
        flat_count += 1
        if len(eq.cutoffs) != 1 or abs(eq.cutoffs[0] - p) > 1e-12:
            flat_bad.append((par, p, eq))
    return {
        "geometry_random": {
            "points": n,
            "ordering_failures": ordering_failures,
            "max_cutoff_residual": max_residual,
            "max_completion_identity_error": max_completion_error,
        },
        "flat_cutoff": {"policies": flat_count, "failures": flat_bad},
        "local_derivative": local,
    }


def root_and_menu_scans(full: bool) -> dict[str, Any]:
    if full:
        ds = [1, 0.9, 0.5, 0.1, 0.01, 1e-4]
        ms = [0.001, 0.03, 0.3, 3, 30, 300]
        alphas = [0, 0.05, 0.3, 1]
        betas = [0.1, 0.3, 0.5, 0.7, 0.9]
        gammas = [0, 0.03, 0.3, 3]
        pn, qn = 5, 7
        random_n, hp_n = 50_000, 80
    else:
        ds = [1, 0.5, 0.01]
        ms = [0.03, 3, 300]
        alphas = [0.05, 1]
        betas = [0.3, 0.7]
        gammas = [0, 0.3]
        pn, qn = 3, 4
        random_n, hp_n = 3_000, 10
    multiple = []
    negative_gain = []
    near_p = 0
    policies = 0
    minimum_gain = (math.inf, None)
    for d, m, alpha, beta, gamma in itertools.product(ds, ms, alphas, betas, gammas):
        par = DiscountParams(m, alpha, beta, gamma, d)
        for p in np.linspace(0.001, beta * 0.995, pn):
            for q in np.linspace(p, beta * 0.999, qn):
                value, eq, _ = pessimistic_value(float(p), float(q), par, grid_size=49)
                gain = value - flat_completion(float(p), par)
                policies += 1
                near_p += sum(kind == "near-p-limit" for kind in eq.kinds)
                if eq.multiplicity > 1:
                    multiple.append((par, p, q, eq))
                if gain < minimum_gain[0]:
                    minimum_gain = (gain, (par, p, q, eq))
                if gain < -2e-9:
                    negative_gain.append((gain, par, p, q, eq))

    rng = np.random.default_rng(SEED)
    random_multiple = []
    random_negative = []
    random_near_p = 0
    for i in range(random_n):
        gamma = 0.0 if i < random_n // 2 else 10 ** rng.uniform(-5, 2)
        par = DiscountParams(
            10 ** rng.uniform(-4, 4),
            10 ** rng.uniform(-5, 0),
            rng.uniform(0.01, 0.99),
            gamma,
            10 ** rng.uniform(-6, 0),
        )
        p = rng.uniform(1e-4, min(0.98, par.beta * 0.999))
        q = rng.uniform(p, min(0.999, par.beta))
        value, eq, _ = pessimistic_value(p, q, par, grid_size=65)
        gain = value - flat_completion(p, par)
        random_near_p += sum(kind == "near-p-limit" for kind in eq.kinds)
        if eq.multiplicity > 1:
            random_multiple.append((par, p, q, eq))
        if gain < -2e-9:
            random_negative.append((gain, par, p, q, eq))

    # Moderate parameters keep all high-precision roots resolvable at the
    # reported box width.  Extreme near-p proxies are separately diagnosed.
    hp_mismatch = []
    hp_unresolved = []
    for _ in range(hp_n):
        par = DiscountParams(
            10 ** rng.uniform(-2, 1.5),
            rng.uniform(0.02, 1),
            rng.uniform(0.05, 0.95),
            0.0 if rng.random() < 0.6 else 10 ** rng.uniform(-2, 0.5),
            10 ** rng.uniform(-3, 0),
        )
        p = rng.uniform(0.001, par.beta * 0.9)
        q = rng.uniform(p + (par.beta - p) * 0.02, par.beta * 0.999)
        fast = find_equilibria(p, q, par, grid_size=161)
        high = isolate_equilibria_mp(str(p), str(q), par, dps=65, box_tol="1e-17")
        aa = np.array(fast.cutoffs)
        bb = np.array([float(z) for z in high.cutoffs])
        if len(aa) != len(bb) or (len(aa) and np.max(np.abs(aa - bb)) > 3e-8):
            hp_mismatch.append((par, p, q, fast, high.cutoffs))
        if high.unresolved:
            hp_unresolved.append((par, p, q, high.unresolved))

    return {
        "structured": {
            "policies": policies,
            "multiple": multiple,
            "negative_same_p_gain": negative_gain,
            "minimum_gain": minimum_gain,
            "near_p_binary64_proxies": near_p,
        },
        "random": {
            "policies": random_n,
            "multiple": random_multiple,
            "negative_same_p_gain": random_negative,
            "near_p_binary64_proxies": random_near_p,
        },
        "mp_crosscheck": {
            "policies": hp_n,
            "mismatches": hp_mismatch,
            "unresolved": hp_unresolved,
        },
    }


def exact_candidates() -> dict[str, Any]:
    """High-precision evaluations of two algebraic thin-limit certificates."""

    with mp.workdps(100):
        # beta=9/10, alpha=1, delta=1/2, fixed cutoff a=3/10.
        target_patient = (3 * mp.sqrt(29) - 9) / 200
        patient = []
        for m_text in ("1e-1", "1e-2", "1e-3", "1e-4", "1e-5"):
            m = mpf(m_text)
            par = DiscountParams(float(m), 1, 0.9, 0, 0.5)
            p, q, value, _ = mp_geometry_point(mpf("0.3"), par)
            _, flat = mp_flat_noentry(m)
            patient.append((m, (value - flat) / m, p, q))

        # beta=1/2, alpha=1, delta=1/2.  The candidate rescaled
        # cutoff displacement is c=1/[16(1-alpha(1-delta)/2)]=1/12.
        target_critical = mp.mpf(1) / 768
        critical = []
        for m_text in ("1e-2", "1e-3", "1e-4", "1e-5", "1e-6"):
            m = mpf(m_text)
            par = DiscountParams(float(m), 1, 0.5, 0, 0.5)
            a = mp.mpf("0.5") - m / 12
            p, q, value, _ = mp_geometry_point(a, par)
            _, flat = mp_flat_noentry(m)
            critical.append((m, (value - flat) / m**3, (value - flat) / m**4, a, p, q))

        # One arbitrary-precision cutoff bracket under the corrected model.
        par = DiscountParams(2, 0.8, 0.7, 0, 0.5)
        eq = isolate_equilibria_mp("0.3", "0.5", par, dps=90, box_tol="1e-28")
        vals = [mp_completion(a, eq.p, eq.q, par) for a in eq.cutoffs]
        root_boxes = [(z.kind, z.lo, z.hi, z.f_lo, z.f_hi) for z in eq.roots]

        # A clean example where the exact root is closer than one binary64 ulp
        # to p.  Opposite signs in the two log-gap probes certify an interior
        # root even though the fast path must represent it by p.
        near_par = DiscountParams(150, 0.36, 0.88, 0, 1e-5)
        near_p, near_q = mpf("0.84"), mpf("0.85")
        near_signs = (
            mp_cutoff_residual(near_p - mpf("1e-60"), near_p, near_q, near_par),
            mp_cutoff_residual(near_p - mpf("1e-65"), near_p, near_q, near_par),
            mp_cutoff_residual(near_p, near_p, near_q, near_par),
        )

    return {
        "patient_exact_limit": {
            "params": {"alpha": 1, "beta": "9/10", "delta": "1/2", "a": "3/10"},
            "candidate_limit": target_patient,
            "evaluations": patient,
        },
        "critical_exact_limit": {
            "params": {"alpha": 1, "beta": "1/2", "delta": "1/2", "a": "1/2-m/12"},
            "candidate_limit_V_over_m3": target_critical,
            "evaluations": critical,
        },
        "mp_root_example": {"params": par, "boxes": root_boxes, "values": vals},
        "near_p_root_certificate": {
            "params": near_par,
            "policy": (near_p, near_q),
            "f_p_minus_1e_60__f_p_minus_1e_65__f_p": near_signs,
            "implied_gap_interval": ("1e-65", "1e-60"),
        },
    }


def dominance_and_thickness(full: bool) -> dict[str, Any]:
    if full:
        ds = [1, 0.9, 0.5, 0.1, 0.01, 1e-4]
        alphas = [1, 0.1, 0.001]
        betas = [0.2, 0.49, 0.5, 0.51, 0.7, 0.9]
        ms = np.geomspace(1e-5, 1e6, 101)
        grid_size = 81
    else:
        ds = [1, 0.5, 0.01]
        alphas = [1, 0.01]
        betas = [0.3, 0.5, 0.7, 0.9]
        ms = np.geomspace(1e-4, 1e4, 41)
        grid_size = 65
    profiles = []
    dominance_violations = []
    thickness_reversals = []
    multiple_thickness_peaks = []
    multiple_scalar_peaks = []
    for delta, alpha, beta in itertools.product(ds, alphas, betas):
        values = []
        for m in ms:
            out = optimize_geometry(
                DiscountParams(float(m), alpha, beta, 0, delta), grid_size=grid_size
            )
            values.append(out.gain)
            if len(out.stationary_maxima) > 1:
                multiple_scalar_peaks.append((delta, alpha, beta, m, out.stationary_maxima))
            if beta >= 0.5 and out.gain <= -2e-12:
                dominance_violations.append((delta, alpha, beta, m, out))
        values_a = np.array(values)
        peak = float(values_a.max())
        tol = max(2e-13, peak * 1e-5)
        signs = []
        for difference in np.diff(values_a):
            sign = 1 if difference > tol else (-1 if difference < -tol else 0)
            if sign and (not signs or signs[-1] != sign):
                signs.append(sign)
        if any(signs[i] < 0 and signs[i + 1] > 0 for i in range(len(signs) - 1)):
            thickness_reversals.append((delta, alpha, beta, signs))
        if signs.count(-1) > 1:
            multiple_thickness_peaks.append((delta, alpha, beta, signs))
        profiles.append((delta, alpha, beta, peak, float(ms[int(np.argmax(values_a))]), signs))

    thick = []
    for delta in (1, 0.5, 0.01, 1e-6):
        rows = []
        for m in (1e4, 1e6, 1e8, 1e10, 1e12):
            out = optimize_geometry(DiscountParams(m, 1, 0.9, 0, delta), grid_size=201, xatol=1e-14)
            rows.append({
                "m": m,
                "a": out.point.a,
                "p": out.point.p,
                "m_loss_over_loglogm": m * (1 - out.dynamic_value) / math.log(math.log(m)),
                "m_gain_over_logm": m * out.gain / math.log(m),
            })
        thick.append((delta, rows))

    # Patience topology: at fixed (m,alpha,delta), test whether improvement is
    # a single upper beta interval; as delta falls, test pointwise that the
    # tangent-menu advantage does not fall.  Thresholds are grid markers only.
    threshold_ms = [0.01, 0.1, 1, 10, 100] if full else [0.1, 1, 10]
    threshold_alphas = [0.01, 0.1, 1] if full else [0.1, 1]
    threshold_ds = [1, 0.9, 0.5, 0.1, 0.01, 1e-4] if full else [1, 0.5, 0.01]
    beta_grid = np.linspace(0.01, 0.99, 99 if full else 41)
    threshold_rows = []
    noninterval = []
    discount_nonmonotone = []
    for m, alpha in itertools.product(threshold_ms, threshold_alphas):
        markers = []
        previous = None
        for delta in threshold_ds:
            raw_gains = []
            for beta in beta_grid:
                out = optimize_geometry(
                    DiscountParams(m, alpha, float(beta), 0, delta), grid_size=65
                )
                raw_gains.append(out.point.value - out.flat_value)
            raw = np.array(raw_gains)
            tol = max(2e-11, 1e-8 * max(float(raw.max()), 1e-12))
            active = raw > tol
            changes = np.flatnonzero(active[1:] != active[:-1])
            if len(changes) > 1 or (len(changes) == 1 and active[0]):
                noninterval.append((m, alpha, delta, changes))
            markers.append(float(beta_grid[int(np.argmax(active))]) if active.any() else None)
            if previous is not None and float(np.min(raw - previous)) < -3e-11:
                discount_nonmonotone.append((m, alpha, delta, float(np.min(raw - previous))))
            previous = raw
        threshold_rows.append((m, alpha, markers))
    return {
        "profiles": len(profiles),
        "profile_summaries": profiles,
        "dominance_violations_beta_ge_half": dominance_violations,
        "thickness_reversals": thickness_reversals,
        "multiple_thickness_peaks": multiple_thickness_peaks,
        "multiple_scalar_peaks": multiple_scalar_peaks,
        "thick_ratios": thick,
        "patience_scan": {
            "curves": len(threshold_ms) * len(threshold_alphas) * len(threshold_ds),
            "beta_grid_markers_by_decreasing_delta": threshold_rows,
            "non_upper_interval": noninterval,
            "discount_nonmonotonicity": discount_nonmonotone,
        },
    }


SECTIONS = {
    "formulas": formula_checks,
    "roots": root_and_menu_scans,
    "exact": lambda full: exact_candidates(),
    "thickness": dominance_and_thickness,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    parser.add_argument("--section", choices=["all", *SECTIONS], default="all")
    args = parser.parse_args()
    full = bool(args.full)
    selected = SECTIONS if args.section == "all" else {args.section: SECTIONS[args.section]}
    result: dict[str, Any] = {"seed": SEED, "mode": "full" if full else "quick"}
    for name, function in selected.items():
        start = time.time()
        result[name] = function(full)
        result[name]["seconds"] = time.time() - start
    print(json.dumps(jsonable(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

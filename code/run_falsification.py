#!/usr/bin/env python3
"""Reproducible numerical red-team for the announced-escalation model.

Examples
--------
Quick smoke test (roughly seconds)::

    python run_falsification.py --quick

Full deterministic grids reported in ``numerical_falsification_report.md``::

    python run_falsification.py --full

The program prints JSON.  It never edits the manuscript or selects a single
equilibrium branch without first enumerating all visible roots.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from typing import Any

import numpy as np
from scipy.optimize import brentq

from equilibria import (
    find_equilibria_fast,
    isolate_equilibria_mp,
    pessimistic_completion_fast,
    pessimistic_completion_mp,
)
from geometry import (
    certify_geometry_optimum_mp,
    flat_optimum_noentry,
    geometry_point,
    optimize_geometry,
    zero_plateau_threshold,
)
from model import Params, flat_completion, local_coefficient, mp, mp_flat_completion, mpf
from noentry import identity_error, q_first_order_residual, reduced_residual
from optimize import Settings, optimize_announced, optimize_flat


SEED = 20260825


def _jsonable(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 40)
    return x


def benchmark_and_local(full: bool) -> dict[str, Any]:
    flat_cases = [
        (Params(0.03, 0.1, 0.5, 0), 0.2),
        (Params(2.0, 0.8, 0.7, 0), 0.3),
        (Params(30.0, 1.0, 0.9, 0), 0.1),
        (Params(2.0, 0.8, 0.7, 0.3), 0.3),
    ]
    flat_errors = []
    for par, p in flat_cases:
        value, eq, vals = pessimistic_completion_fast(p, p, par, grid_size=129)
        flat_errors.append(
            {
                "params": vars(par),
                "p": p,
                "cutoffs": eq.cutoffs,
                "cutoff_error": max(abs(a - p) for a in eq.cutoffs),
                "completion_error": abs(value - flat_completion(p, par)),
            }
        )

    local_cases = [
        (Params(2.0, 0.8, 0.7, 0), 0.3),
        (Params(0.1, 1.0, 0.9, 0), 0.4),
        (Params(10.0, 0.2, 0.6, 0), 0.2),
        (Params(2.0, 0.8, 0.7, 0.3), 0.3),
    ]
    local = []
    eps = 1e-7
    for par, p in local_cases:
        claimed = local_coefficient(p, par)
        value, eq, _ = pessimistic_completion_fast(p, p + eps, par, grid_size=161)
        quotient = (value - flat_completion(p, par)) / eps
        local.append(
            {
                "params": vars(par),
                "p": p,
                "claimed": claimed,
                "quotient_eps_1e-7": quotient,
                "relative_error": (quotient - claimed) / claimed,
                "cutoffs": eq.cutoffs,
            }
        )

    # One arbitrary-precision, all-box derivative check.
    par, p = local_cases[0]
    eps_mp = mpf("1e-8")
    eq_mp = isolate_equilibria_mp(str(p), str(p + 1e-8), par, dps=90, box_tol="1e-28")
    value_mp, _ = pessimistic_completion_mp(eq_mp, par)
    derivative_mp = (value_mp - mp_flat_completion(mpf(str(p)), par)) / eps_mp
    return {
        "flat": flat_errors,
        "local": local,
        "mp_local": {
            "quotient": derivative_mp,
            "claimed": local_coefficient(p, par),
            "root_boxes": [
                (z.kind, mp.nstr(z.lo, 35), mp.nstr(z.hi, 35), mp.nstr(z.f_lo, 8), mp.nstr(z.f_hi, 8))
                for z in eq_mp.roots
            ],
        },
    }


def root_scans(full: bool) -> dict[str, Any]:
    if full:
        ms = [0.03, 0.1, 0.3, 1, 3, 10, 30]
        alphas = [0.1, 0.3, 0.6, 0.9, 1]
        betas = [0.2, 0.4, 0.6, 0.8, 0.95]
        p1n, p2n = 13, 17
    else:
        ms, alphas, betas = [0.1, 1, 10], [0.1, 1], [0.4, 0.8]
        p1n, p2n = 7, 9
    multiple0 = []
    count0 = 0
    for m, alpha, beta in itertools.product(ms, alphas, betas):
        par = Params(m, alpha, beta, 0)
        for p1 in np.linspace(0.005, min(beta * 0.995, 0.98), p1n):
            for p2 in np.linspace(p1, min(beta * 0.9999, 1), p2n):
                eq = find_equilibria_fast(float(p1), float(p2), par, grid_size=49)
                count0 += 1
                if eq.multiplicity > 1:
                    multiple0.append((vars(par), p1, p2, eq.cutoffs, eq.kinds))

    if full:
        gammas = [0.03, 0.1, 0.3, 1, 3]
        ms_g = ms
        alphas_g = [0, 0.1, 0.5, 1]
        betas_g = [0.2, 0.5, 0.8, 0.95]
        n1, n2 = 9, 11
    else:
        gammas, ms_g, alphas_g, betas_g = [0.1, 1], [0.1, 3], [0.1, 1], [0.5, 0.9]
        n1, n2 = 5, 7
    multiple_g = []
    count_g = 0
    for m, alpha, beta, gamma in itertools.product(ms_g, alphas_g, betas_g, gammas):
        par = Params(m, alpha, beta, gamma)
        for p1 in np.linspace(0.005, min(beta * 0.995, 0.98), n1):
            for p2 in np.linspace(p1, min(beta * 0.9999, 1), n2):
                eq = find_equilibria_fast(float(p1), float(p2), par, grid_size=49)
                count_g += 1
                if eq.multiplicity > 1:
                    multiple_g.append((vars(par), p1, p2, eq.cutoffs, eq.kinds))

    # Independent max-of-two-branches reduction.
    rng = np.random.default_rng(SEED)
    random_n = 100_000 if full else 5_000
    multi_reduced = []
    max_identity = 0.0
    for _ in range(random_n):
        m = 10 ** rng.uniform(-3, 2.5)
        alpha = 10 ** rng.uniform(-4, 0)
        beta = rng.uniform(0.01, 0.999)
        p = beta * rng.random()
        q = p + (beta - p) * rng.random()
        par = Params(m, alpha, beta, 0)
        xs = np.linspace(0.0, p, 97)
        fs = reduced_residual(xs, p, q, par)
        changes = np.flatnonzero(fs[:-1] * fs[1:] < 0)
        if len(changes) > 1:
            multi_reduced.append((vars(par), p, q, len(changes)))
        a = p * rng.random()
        lhs = float(reduced_residual(a, p, q, par))
        err = abs(identity_error(a, p, q, par))
        max_identity = max(max_identity, err / max(1.0, abs(lhs)))

    # Independent interval-style recertification on random policies.
    hp_n = 120 if full else 12
    hp_bad, hp_unresolved = [], []
    for i in range(hp_n):
        m = 10 ** rng.uniform(-2, 2)
        alpha = rng.random()
        beta = rng.uniform(0.05, 0.98)
        gamma = 0.0 if i < 2 * hp_n // 3 else 10 ** rng.uniform(-2, 0.5)
        p1 = rng.uniform(0, min(beta, 0.95))
        p2 = rng.uniform(p1, min(beta, 0.999999))
        par = Params(m, alpha, beta, gamma)
        fast = find_equilibria_fast(p1, p2, par, grid_size=129)
        high = isolate_equilibria_mp(str(p1), str(p2), par, dps=65, box_tol="1e-18")
        aa, bb = np.array(fast.cutoffs), np.array([float(x) for x in high.cutoffs])
        if len(aa) != len(bb) or (len(aa) and np.max(np.abs(aa - bb)) > 2e-8):
            hp_bad.append((vars(par), p1, p2, aa.tolist(), bb.tolist()))
        if high.unresolved:
            hp_unresolved.append((vars(par), p1, p2, len(high.unresolved)))
    return {
        "gamma0_grid": {"policies": count0, "multiple": multiple0},
        "gamma_positive_grid": {"policies": count_g, "multiple": multiple_g},
        "reduced_random": {"policies": random_n, "multiple": multi_reduced, "max_scaled_identity_error": max_identity},
        "mp_crosscheck": {"policies": hp_n, "mismatches": hp_bad, "unresolved": hp_unresolved},
    }


def geometry_scans(full: bool) -> dict[str, Any]:
    rng = np.random.default_rng(SEED)
    random_n = 100_000 if full else 5_000
    bad = []
    max_cutoff = max_completion = 0.0
    for i in range(random_n):
        m = 10 ** rng.uniform(-5, 6)
        alpha = 10 ** rng.uniform(-8, 0)
        beta = rng.uniform(0.01, 0.999)
        u = rng.random()
        frac = rng.random() ** 8 if u < 1 / 3 else (1 - rng.random() ** 8 if u < 2 / 3 else rng.random())
        a = beta * frac
        par = Params(m, alpha, beta, 0)
        z = geometry_point(a, par)
        if not (-2e-12 <= a <= z.p + 2e-12 <= z.q + 4e-12 <= beta + 6e-12):
            bad.append((vars(par), a, z))
        if i < min(random_n, 20_000) and 1e-14 < a < beta - 1e-14 and m * a < 600:
            from model import completion, cutoff_residual

            max_cutoff = max(max_cutoff, abs(cutoff_residual(a, z.p, z.q, par)))
            max_completion = max(max_completion, abs(completion(a, z.p, z.q, par) - z.j))

    if full:
        ms, alphas, betas = np.geomspace(1e-5, 1e6, 30), np.geomspace(1e-8, 1, 12), np.linspace(0.05, 0.99, 12)
    else:
        ms, alphas, betas = np.geomspace(1e-4, 1e4, 8), np.geomspace(1e-6, 1, 5), [0.2, 0.5, 0.9]
    multi_j = []
    curves = 0
    for m, alpha, beta in itertools.product(ms, alphas, betas):
        out = optimize_geometry(Params(float(m), float(alpha), float(beta), 0), grid_size=81)
        curves += 1
        if len(out.local_maxima) > 1:
            multi_j.append((m, alpha, beta, [(z.a, z.j) for z in out.local_maxima]))

    if full:
        p_ms, p_alphas, p_betas, p_nodes = (
            np.geomspace(1e-5, 1e6, 30),
            np.geomspace(1e-8, 1, 15),
            [0.05, 0.2, 0.5, 0.9, 0.99],
            501,
        )
    else:
        p_ms, p_alphas, p_betas, p_nodes = (
            np.geomspace(1e-4, 1e4, 5),
            np.geomspace(1e-6, 1, 4),
            [0.2, 0.5, 0.9],
            101,
        )
    nonmonotone_p, max_p0_error, p_curves = [], 0.0, 0
    for m, alpha, beta in itertools.product(p_ms, p_alphas, p_betas):
        par = Params(float(m), float(alpha), float(beta), 0)
        aa = np.linspace(0.0, beta, p_nodes)
        pp = np.array([geometry_point(float(a), par).p for a in aa])
        p_curves += 1
        if np.min(np.diff(pp)) < -2e-12:
            nonmonotone_p.append((m, alpha, beta, float(np.min(np.diff(pp)))))
        pz, _, _ = zero_plateau_threshold(par)
        max_p0_error = max(max_p0_error, abs(pp[0] - pz))

    moderate = []
    settings = Settings(p1_grid=13, p2_grid=17, root_grid=65, local_refinements=1,
                        xatol=1e-7, diagnostics=False)
    for par in [Params(2, 0.8, 0.7, 0), Params(10, 1, 0.9, 0), Params(0.1, 0.5, 0.8, 0)]:
        g = optimize_geometry(par, grid_size=121)
        nested = optimize_announced(par, settings)
        moderate.append(
            {
                "params": vars(par),
                "geometry": (g.point.a, g.point.p, g.point.q, g.dynamic_value),
                "nested": (nested.best.cutoffs, nested.best.p1, nested.best.p2, nested.best.value),
                "value_error": g.dynamic_value - nested.best.value,
                "q_foc": q_first_order_residual(g.point.a, g.point.q, par),
            }
        )
    return {
        "random_points": random_n,
        "ordering_failures": bad[:10],
        "max_cutoff_residual": max_cutoff,
        "max_completion_identity_error": max_completion,
        "J_curves": curves,
        "multiple_stationary_J": multi_j,
        "P_curves": p_curves,
        "nonmonotone_P": nonmonotone_p,
        "max_P0_minus_pz": max_p0_error,
        "nested_crosschecks": moderate,
    }


def thickness_scans(full: bool) -> dict[str, Any]:
    if full:
        alphas = np.geomspace(1e-8, 1, 9)
        betas = [0.5, 0.500001, 0.55, 0.7, 0.9, 0.99]
        ms = np.geomspace(1e-5, 1e6, 101)
    else:
        alphas, betas, ms = [1e-8, 1], [0.5, 0.9], np.geomspace(1e-5, 1e6, 41)
    profiles = []
    for alpha, beta in itertools.product(alphas, betas):
        vals, bad_local = [], []
        for m in ms:
            par = Params(float(m), float(alpha), float(beta), 0)
            g = optimize_geometry(par, grid_size=65, xatol=3e-11)
            cert = certify_geometry_optimum_mp(par, g.point.a, dps=50)
            vals.append(float(cert.escalation_value))
            if len(g.local_maxima) != 1:
                bad_local.append((float(m), len(g.local_maxima)))
        signs = np.sign(np.diff(np.log(vals)))
        down = (np.flatnonzero((signs[:-1] > 0) & (signs[1:] < 0)) + 1).tolist()
        up = (np.flatnonzero((signs[:-1] < 0) & (signs[1:] > 0)) + 1).tolist()
        imax = int(np.argmax(vals))
        profiles.append(
            {
                "alpha": alpha,
                "beta": beta,
                "down_crossings": down,
                "up_crossings": up,
                "grid_peak_m": ms[imax],
                "grid_peak_v": vals[imax],
                "endpoint_v": (vals[0], vals[-1]),
                "bad_local_counts": bad_local,
            }
        )

    # Exact zero-plateau certificate ingredients for beta=1/5.
    lower_bound = -math.log((1.0 + math.exp(-0.5)) / 2.0)
    p12, _ = flat_optimum_noentry(12.0)
    # Numerical location where p_F(m)=1/5; not needed for the exact [0,1]
    # certificate, but useful as a sharp candidate transition.
    transition = brentq(lambda m: math.exp(0.2 * m) - 1 - 0.8 * m, 1e-8, 100)

    thin = []
    for alpha in [1.0, 1e-8]:
        par = Params(1e-5, alpha, 0.5, 0)
        g = optimize_geometry(par)
        c = certify_geometry_optimum_mp(par, g.point.a, dps=80)
        thin.append((alpha, c.escalation_value, c.escalation_value / mpf("1e-20"), mpf(alpha) / 2048))

    thick = []
    for m in [1e4, 1e6, 1e8, 1e10, 1e12]:
        par = Params(m, 1, 0.9, 0)
        g = optimize_geometry(par, grid_size=161, xatol=1e-18)
        c = certify_geometry_optimum_mp(par, g.point.a, dps=60)
        thick.append(
            (
                m,
                m * (1 - float(c.dynamic_value)) / math.log(math.log(m)),
                m * float(c.escalation_value) / math.log(m),
            )
        )
    return {
        "profiles": profiles,
        "zero_plateau_beta_1_5": {
            "lower_bound_beta_L_on_0_1": lower_bound,
            "strictly_above_1_5": lower_bound > 0.2,
            "pF_at_12": p12,
            "pF_at_12_below_1_5": p12 < 0.2,
            "candidate_sharp_transition_m": transition,
        },
        "critical_thin": thin,
        "thick_ratios_alpha1_beta_0_9": thick,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--quick", action="store_true", help="small smoke-test grids")
    group.add_argument("--full", action="store_true", help="reported deterministic grids")
    parser.add_argument(
        "--section",
        choices=["all", "benchmark", "roots", "geometry", "thickness"],
        default="all",
    )
    args = parser.parse_args()
    full = bool(args.full)
    started = time.time()
    jobs = {
        "benchmark": benchmark_and_local,
        "roots": root_scans,
        "geometry": geometry_scans,
        "thickness": thickness_scans,
    }
    selected = jobs if args.section == "all" else {args.section: jobs[args.section]}
    result = {name: fn(full) for name, fn in selected.items()}
    result["meta"] = {"seed": SEED, "full": full, "seconds": time.time() - started}
    print(json.dumps(_jsonable(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

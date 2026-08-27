"""Numerical red-team checks for the mixed-supply local theorems.

Run from the repository root with

    PYTHONPATH=code python code/check_mixed_supply_theorems.py

The all-root flat optimizer is intentional because the fresh-entry flat
objective need not be unimodal on the interval below beta.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from discount_model import (
    DiscountParams,
    flat_completion,
    pessimistic_value,
    rider_response,
    share,
)


def flat_derivative_left(p: float, m: float, beta: float, gamma: float) -> float:
    """Derivative of Q^F_gamma on 0 < p < beta."""

    r = math.exp(-m * p)
    e = math.exp(-gamma * m * p)
    continuation_value = 1.0 - p / beta
    entry_coverage = 1.0 - e
    initial = -1.0 + r * (1.0 + m * (1.0 - p))
    terminal = r * (
        -m * continuation_value * entry_coverage
        - entry_coverage / beta
        + continuation_value * gamma * m * e
    )
    return initial + terminal


def flat_derivative_right(p: float, m: float) -> float:
    """Derivative of the initial-only objective on p > beta."""

    r = math.exp(-m * p)
    return -1.0 + r * (1.0 + m * (1.0 - p))


def _sign_change_roots(fun, nodes: np.ndarray) -> list[float]:
    values = np.asarray([fun(float(x)) for x in nodes])
    roots: list[float] = []
    for lo, hi, flo, fhi in zip(nodes[:-1], nodes[1:], values[:-1], values[1:]):
        if flo == 0.0:
            roots.append(float(lo))
        elif flo * fhi < 0.0:
            roots.append(
                float(
                    brentq(
                        fun,
                        float(lo),
                        float(hi),
                        xtol=5e-15,
                        rtol=4 * np.finfo(float).eps,
                    )
                )
            )
    return roots


def optimize_flat_entry(par: DiscountParams) -> tuple[float, float, tuple[float, ...]]:
    """Enumerate visible stationary points, the kink, and all endpoints."""

    m, beta, gamma = par.m, par.beta, par.gamma
    # The geometric component resolves stationary points near zero when both
    # m and gamma are large; the linear component resolves the rest.
    left_nodes = np.unique(
        np.r_[
            np.linspace(0.0, beta, 20001),
            beta * np.geomspace(1e-14, 1.0, 12001),
        ]
    )
    candidates = [0.0, beta, 1.0]
    candidates += _sign_change_roots(
        lambda p: flat_derivative_left(p, m, beta, gamma), left_nodes[1:-1]
    )
    if beta < 1.0:
        right_nodes = np.linspace(beta, 1.0, 10001)
        candidates += _sign_change_roots(
            lambda p: flat_derivative_right(p, m), right_nodes[1:-1]
        )
    candidates = sorted(set(candidates))
    values = [flat_completion(p, par) for p in candidates]
    index = int(np.argmax(values))
    return candidates[index], values[index], tuple(candidates)


def local_certificate(p: float, par: DiscountParams) -> dict[str, float | bool]:
    """Closed-form activity gate, cutoff slope, and completion derivative."""

    m, alpha, beta, gamma, delta = (
        par.m,
        par.alpha,
        par.beta,
        par.gamma,
        par.delta,
    )
    if not 0.0 < p < beta or alpha + gamma <= 0.0:
        return {"active": False, "bar_v": math.inf, "kappa": 0.0, "gain": 0.0}
    x = m * p
    r = math.exp(-x)
    e = math.exp(-gamma * x)
    sigma = float(share(x))
    ell = float(share(gamma * x))
    rho = (1.0 - p / beta) / (1.0 - p)
    bar_v = (p + math.expm1(gamma * x) / (m * (alpha + gamma))) / beta
    if not bar_v < 1.0:
        return {"active": False, "bar_v": bar_v, "kappa": 0.0, "gain": 0.0}
    eta = (1.0 - bar_v) / (1.0 - p)
    denominator = sigma - delta * r * alpha * rho * ell
    t_delta = e * (alpha + gamma) * sigma - delta * r * alpha * ell * (
        1.0 - rho + rho * e * (1.0 + gamma)
    )
    kappa = delta * r * alpha * ell * eta / denominator
    gain = m * (1.0 - p) * r * eta * t_delta / denominator
    return {
        "active": True,
        "bar_v": bar_v,
        "kappa": kappa,
        "gain": gain,
        "t_delta": t_delta,
    }


def composition_endpoints_fixed_s(
    *, m: float, beta: float, delta: float, p: float, s: float
) -> tuple[float, float, float]:
    """All-entrant, all-incumbent local gains and their patience threshold."""

    if not (0.0 < s <= 1.0 and 0.0 < p < beta < 1.0):
        raise ValueError("requires 0<s<=1 and 0<p<beta<1")
    x = m * p
    r = math.exp(-x)
    sigma = float(share(x))
    rho = (1.0 - p / beta) / (1.0 - p)
    e_s = math.exp(-s * x)
    all_entry = r / beta * (
        m * s * e_s * (beta - p) - (1.0 - e_s)
    )
    zero_patience_incumbent = m * r * s * (1.0 - p / beta)
    z = all_entry / zero_patience_incumbent
    delta_crossing = sigma * (1.0 - z) / (r * (1.0 - z * s * rho))
    all_incumbent = zero_patience_incumbent * (
        (sigma - delta * r) / (sigma - delta * r * s * rho)
    )
    return all_entry, all_incumbent, delta_crossing


def main() -> None:
    active = DiscountParams(m=1.0, alpha=0.8, beta=0.8, gamma=0.2, delta=0.8)
    p, flat, _ = optimize_flat_entry(active)
    cert = local_certificate(p, active)
    assert abs(p - 0.42214391165472114) < 2e-12
    assert cert["active"]
    assert abs(float(cert["gain"]) - 0.15291260393513486) < 2e-11
    epsilon = 1e-6
    value, equilibria, _ = pessimistic_value(p, p + epsilon, active, grid_size=1025)
    assert equilibria.multiplicity == 1
    relative_error = abs((value - flat) / epsilon / float(cert["gain"]) - 1.0)
    assert relative_error < 1e-5

    inactive = DiscountParams(m=1.0, alpha=0.5, beta=0.5, gamma=1.0, delta=0.8)
    p, flat, _ = optimize_flat_entry(inactive)
    cert = local_certificate(p, inactive)
    assert abs(p - 0.3045477768350368) < 2e-12
    assert not cert["active"] and float(cert["bar_v"]) > 1.08
    for epsilon in (1e-2, 1e-3, 1e-4):
        value, equilibria, _ = pessimistic_value(
            p, p + epsilon, inactive, grid_size=1025
        )
        assert equilibria.cutoffs == (p,)
        assert rider_response(p, p, p + epsilon, inactive).rescue == 0.0
        assert abs(value - flat) < 1e-12

    all_entry, all_incumbent, crossing = composition_endpoints_fixed_s(
        m=1.0, beta=0.8, delta=0.8, p=0.3, s=1.0
    )
    assert abs(all_entry - 0.10299904182415223) < 1e-12
    assert abs(all_incumbent - 0.37519154971816378) < 1e-12
    assert crossing > 1.13

    all_entry, all_incumbent, crossing = composition_endpoints_fixed_s(
        m=1.0, beta=0.5, delta=1.0, p=0.1, s=1.0
    )
    assert abs(crossing - 0.86030314793534034) < 1e-12
    assert all_incumbent < all_entry
    profile = []
    for alpha in (0.75, 0.92, 0.99):
        par = DiscountParams(
            m=1.0, alpha=alpha, beta=0.5, gamma=1.0 - alpha, delta=1.0
        )
        profile.append(float(local_certificate(0.1, par)["gain"]))
    assert profile[0] > profile[1] < profile[2]

    print(
        "mixed-supply red-team checks passed; nonmonotone profile =",
        tuple(f"{x:.12f}" for x in profile),
    )


if __name__ == "__main__":
    main()

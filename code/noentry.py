"""Independent gamma=0 reduction used as a falsification cross-check.

For gamma=0, multiplying the cutoff residual by m exp(ma) eliminates all
assignment-share ratios.  The resulting max-of-two-branches equation is
particularly useful for checking roots found from the manuscript formulas.
"""

from __future__ import annotations

import math
import numpy as np
from scipy.optimize import brentq

from model import Params, coverage, cutoff_residual, mp, mpf


def reduced_residual(
    a: float | np.ndarray, p: float, q: float, par: Params
) -> float | np.ndarray:
    if par.gamma != 0.0:
        raise ValueError("no-entry reduction requires gamma=0")
    aa = np.asarray(a, dtype=float)
    if p >= 1.0:
        out = np.zeros_like(aa)
        return float(out) if out.ndim == 0 else out
    # T=(p-a)(exp(ma)-1)/a, using its continuous value mp at a=0.
    ratio = np.empty_like(aa)
    zero = aa == 0.0
    ratio[zero] = par.m
    ratio[~zero] = np.expm1(par.m * aa[~zero]) / aa[~zero]
    today = (p - aa) * ratio
    if p >= par.beta:
        cont = np.zeros_like(aa)
    else:
        cp = coverage(par.alpha * par.m * (p - aa))
        cq = coverage(par.alpha * par.m * (q - aa))
        repeat = (par.beta - p) * cp
        rescue = (par.beta - q) * cq
        cont = np.maximum.reduce([repeat, rescue, np.zeros_like(aa)]) / (
            par.beta * (1.0 - p)
        )
    out = today - cont
    return float(out) if out.ndim == 0 else out


def identity_error(a: float, p: float, q: float, par: Params) -> float:
    lhs = reduced_residual(a, p, q, par)
    rhs = par.m * math.exp(par.m * a) * cutoff_residual(a, p, q, par)
    return float(lhs - rhs)


def mp_reduced_residual(
    a: mp.mpf, p: mp.mpf, q: mp.mpf, par: Params
) -> mp.mpf:
    if par.gamma != 0.0:
        raise ValueError("no-entry reduction requires gamma=0")
    m, alpha, beta = (mpf(x) for x in (par.m, par.alpha, par.beta))
    ratio = m if a == 0 else mp.expm1(m * a) / a
    today = (p - a) * ratio
    if p >= beta:
        return today
    cp = -mp.expm1(-alpha * m * (p - a))
    cq = -mp.expm1(-alpha * m * (q - a))
    cont = max((beta - p) * cp, (beta - q) * cq, mp.mpf(0)) / (
        beta * (mp.mpf(1) - p)
    )
    return today - cont


def q_first_order_residual(a: float, q: float, par: Params) -> float:
    """Interior conditional-q first-order condition candidate."""

    if par.gamma != 0.0:
        raise ValueError("no-entry reduction requires gamma=0")
    k = par.alpha * par.m
    return math.expm1(k * (q - a)) - k * (par.beta - q)


def q_star(a: float, par: Params) -> float:
    """Solve exp(k(q-a))-1=k(beta-q) on [a,beta]."""

    k = par.alpha * par.m
    if k == 0.0:
        return par.beta
    return float(brentq(lambda q: q_first_order_residual(a, q, par), a, par.beta,
                        xtol=5e-15, rtol=4 * np.finfo(float).eps))


def active_supply_term(a: float, par: Params) -> tuple[float, float]:
    q = q_star(a, par)
    s = (par.beta - q) * float(coverage(par.alpha * par.m * (q - a)))
    return s, q


def zero_cutoff_p_threshold(par: Params) -> tuple[float, float]:
    """Candidate fixed-p boundary p_z and its q=Q(0)."""

    s0, q0 = active_supply_term(0.0, par)
    disc = 1.0 - 4.0 * s0 / (par.beta * par.m)
    if disc < -2e-13:
        raise ValueError("negative discriminant in p_z formula")
    return (1.0 - math.sqrt(max(0.0, disc))) / 2.0, q0


def lower_p_branch(a: float, par: Params) -> tuple[float, float]:
    """Candidate lower root P(a) and q=Q(a) of the cutoff equation."""

    s, q = active_supply_term(a, par)
    h = par.m if a == 0.0 else math.expm1(par.m * a) / a
    disc = (1.0 - a) ** 2 - 4.0 * s / (par.beta * h)
    if disc < -2e-12:
        raise ValueError("negative discriminant in P(a) formula")
    p = (1.0 + a - math.sqrt(max(0.0, disc))) / 2.0
    return p, q

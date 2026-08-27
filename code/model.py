"""Numerically stable primitives for the announced-escalation model.

The formulas in this module are an independent numerical transcription of the
model maintained in ``paper/formal/main.tex``.  Both binary64 and arbitrary
precision versions are provided.  The arbitrary precision path deliberately
uses only mpmath primitives and is used to validate, rather than merely repeat,
the scipy optimization path.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import sys
from typing import NamedTuple

import numpy as np


# mpmath is vendored so that the numerical audit is reproducible in the task
# container.  A system installation, if present, remains usable.
_VENDOR = Path(__file__).resolve().parent / "_vendor"
if _VENDOR.exists() and str(_VENDOR) not in sys.path:
    sys.path.insert(0, str(_VENDOR))
import mpmath as mp  # noqa: E402


@dataclass(frozen=True)
class Params:
    m: float
    alpha: float
    beta: float
    gamma: float = 0.0

    def validate(self) -> None:
        if not (self.m > 0.0):
            raise ValueError("m must be strictly positive")
        if not (0.0 <= self.alpha <= 1.0):
            raise ValueError("alpha must lie in [0,1]")
        if not (0.0 < self.beta < 1.0):
            raise ValueError("beta must lie in (0,1)")
        if not (self.gamma >= 0.0):
            raise ValueError("gamma must be nonnegative")


class RiderResponse(NamedTuple):
    v_m: float
    eta_repeat: float
    eta_escalate: float
    rho: float


class MPRiderResponse(NamedTuple):
    v_m: mp.mpf
    eta_repeat: mp.mpf
    eta_escalate: mp.mpf
    rho: mp.mpf


def _policy_check(p1: float, p2: float) -> None:
    if not (0.0 <= p1 <= p2 <= 1.0):
        raise ValueError(f"invalid policy ({p1}, {p2})")


def phi(x: float | np.ndarray) -> float | np.ndarray:
    """Poisson assignment share (1-exp(-x))/x, stably at zero."""

    xa = np.asarray(x, dtype=float)
    out = np.empty_like(xa)
    tiny = np.abs(xa) < 1.0e-7
    xt = xa[tiny]
    # Enough terms to make the truncation negligible in binary64 here.
    out[tiny] = 1.0 - xt / 2.0 + xt * xt / 6.0 - xt**3 / 24.0 + xt**4 / 120.0
    xn = xa[~tiny]
    out[~tiny] = -np.expm1(-xn) / xn
    return float(out) if out.ndim == 0 else out


def coverage(x: float | np.ndarray) -> float | np.ndarray:
    xa = np.asarray(x, dtype=float)
    out = -np.expm1(-xa)
    return float(out) if out.ndim == 0 else out


def lambdas(a: float, p1: float, p2: float, par: Params) -> tuple[float, float]:
    lam1 = par.m * (par.alpha * (p1 - a) + par.gamma * p1)
    lam2 = par.m * (par.alpha * (p2 - a) + par.gamma * p2)
    # Roundoff can put a theoretically zero intensity just below zero.
    return max(0.0, lam1), max(0.0, lam2)


def rho_mass(p1: float, beta: float) -> float:
    if p1 >= 1.0:
        return 0.0
    return max(1.0 - p1 / beta, 0.0) / (1.0 - p1)


def rider_response(a: float, p1: float, p2: float, par: Params) -> RiderResponse:
    """Continuation masses, with a stable computation of the coverage ratio.

    For p2 > p1 and alpha+gamma > 0,

        v_M = p2/beta + C1 (p2-p1)/(beta (C2-C1)),

    and C2-C1 = exp(-lambda1) * (1-exp(-(lambda2-lambda1))).
    This avoids catastrophic cancellation close to the flat diagonal.
    """

    if p1 >= 1.0:
        return RiderResponse(math.inf, 0.0, 0.0, 0.0)
    rho = rho_mass(p1, par.beta)
    if rho == 0.0 or p2 == p1 or par.alpha + par.gamma == 0.0:
        return RiderResponse(math.inf, rho, 0.0, rho)

    dp = p2 - p1
    lam1, _ = lambdas(a, p1, p2, par)
    dlam = par.m * (par.alpha + par.gamma) * dp
    c1 = float(coverage(lam1))
    dc = math.exp(-lam1) * (-math.expm1(-dlam))
    if dc == 0.0:
        # Both coverages round to one and their difference is below binary64.
        # The threshold is then far above one, so escalation is inactive.
        return RiderResponse(math.inf, rho, 0.0, rho)
    v_m = p2 / par.beta + c1 * dp / (par.beta * dc)
    eta_e = max(1.0 - v_m, 0.0) / (1.0 - p1)
    # Direct clipping protects the exact identity eta_R + eta = rho.
    eta_e = min(max(eta_e, 0.0), rho)
    eta_r = rho - eta_e
    return RiderResponse(v_m, eta_r, eta_e, rho)


def cutoff_residual(a: float, p1: float, p2: float, par: Params) -> float:
    """f_m(a;p1,p2) = accept payoff minus wait payoff at c=a."""

    if not (0.0 <= a <= p1):
        raise ValueError("cutoff a must lie in [0,p1]")
    rr = rider_response(a, p1, p2, par)
    lam1, lam2 = lambdas(a, p1, p2, par)
    accept = float(phi(par.m * a)) * (p1 - a)
    wait = math.exp(-par.m * a) * par.alpha * (
        rr.eta_repeat * float(phi(lam1)) * (p1 - a)
        + rr.eta_escalate * float(phi(lam2)) * (p2 - a)
    )
    return accept - wait


def cutoff_residual_array(
    a: np.ndarray, p1: float, p2: float, par: Params
) -> np.ndarray:
    """Vectorized binary64 residual used by the exploratory global scan."""

    aa = np.asarray(a, dtype=float)
    if np.any(aa < -2e-15) or np.any(aa > p1 + 2e-15):
        raise ValueError("cutoff array must lie in [0,p1]")
    aa = np.clip(aa, 0.0, p1)
    lam1 = par.m * (par.alpha * (p1 - aa) + par.gamma * p1)
    lam2 = par.m * (par.alpha * (p2 - aa) + par.gamma * p2)
    rho = rho_mass(p1, par.beta)
    if rho == 0.0 or p2 == p1 or par.alpha + par.gamma == 0.0:
        eta_e = np.zeros_like(aa)
    else:
        dp = p2 - p1
        dlam = par.m * (par.alpha + par.gamma) * dp
        dc = np.exp(-lam1) * (-np.expm1(-dlam))
        v_m = p2 / par.beta + coverage(lam1) * dp / (par.beta * dc)
        eta_e = np.clip(np.maximum(1.0 - v_m, 0.0) / (1.0 - p1), 0.0, rho)
    eta_r = rho - eta_e
    return phi(par.m * aa) * (p1 - aa) - np.exp(-par.m * aa) * par.alpha * (
        eta_r * phi(lam1) * (p1 - aa)
        + eta_e * phi(lam2) * (p2 - aa)
    )


def completion(a: float, p1: float, p2: float, par: Params) -> float:
    if p1 >= 1.0:
        return 0.0
    rr = rider_response(a, p1, p2, par)
    lam1, lam2 = lambdas(a, p1, p2, par)
    first = float(coverage(par.m * a))
    rescue = math.exp(-par.m * a) * (
        rr.eta_repeat * float(coverage(lam1))
        + rr.eta_escalate * float(coverage(lam2))
    )
    return (1.0 - p1) * (first + rescue)


def flat_completion(p: float, par: Params) -> float:
    if p >= 1.0:
        return 0.0
    first = (1.0 - p) * float(coverage(par.m * p))
    rescue = (
        math.exp(-par.m * p)
        * max(1.0 - p / par.beta, 0.0)
        * float(coverage(par.gamma * par.m * p))
    )
    return first + rescue


def local_coefficient(p: float, par: Params) -> float:
    """The manuscript's claimed right derivative at (p,p)."""

    if not (0.0 < p < par.beta) or par.alpha + par.gamma == 0.0:
        return 0.0
    r = math.exp(-par.m * p)
    e = math.exp(-par.gamma * par.m * p)
    sigma = float(phi(par.m * p))
    ell = float(phi(par.gamma * par.m * p))
    rho = (1.0 - p / par.beta) / (1.0 - p)
    bar_v = (p + (1.0 - e) / (par.m * e * (par.alpha + par.gamma))) / par.beta
    eta0 = max(1.0 - bar_v, 0.0) / (1.0 - p)
    denom = sigma - r * par.alpha * ell * rho
    kappa = r * par.alpha * ell * eta0 / denom
    b = 1.0 - rho * (1.0 - (1.0 - par.alpha) * e)
    return par.m * (1.0 - p) * r * (
        e * (par.alpha + par.gamma) * eta0 - kappa * b
    )


# ------------------------- arbitrary precision path -------------------------


def mpf(x: object) -> mp.mpf:
    """Convert without importing the binary representation of a float."""

    if isinstance(x, mp.mpf):
        return x
    return mp.mpf(str(x))


def mp_params(par: Params) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    return tuple(mpf(x) for x in (par.m, par.alpha, par.beta, par.gamma))  # type: ignore[return-value]


def mp_phi(x: mp.mpf) -> mp.mpf:
    if x == 0:
        return mp.mpf(1)
    return -mp.expm1(-x) / x


def mp_coverage(x: mp.mpf) -> mp.mpf:
    return -mp.expm1(-x)


def mp_lambdas(
    a: mp.mpf, p1: mp.mpf, p2: mp.mpf, par: Params
) -> tuple[mp.mpf, mp.mpf]:
    m, alpha, _, gamma = mp_params(par)
    return (
        m * (alpha * (p1 - a) + gamma * p1),
        m * (alpha * (p2 - a) + gamma * p2),
    )


def mp_rider_response(
    a: mp.mpf, p1: mp.mpf, p2: mp.mpf, par: Params
) -> MPRiderResponse:
    _, alpha, beta, gamma = mp_params(par)
    zero = mp.mpf(0)
    one = mp.mpf(1)
    if p1 >= 1:
        return MPRiderResponse(mp.inf, zero, zero, zero)
    rho = max(one - p1 / beta, zero) / (one - p1)
    if rho == 0 or p2 == p1 or alpha + gamma == 0:
        return MPRiderResponse(mp.inf, rho, zero, rho)
    m, _, _, _ = mp_params(par)
    dp = p2 - p1
    lam1, _ = mp_lambdas(a, p1, p2, par)
    dlam = m * (alpha + gamma) * dp
    c1 = mp_coverage(lam1)
    dc = mp.exp(-lam1) * (-mp.expm1(-dlam))
    v_m = p2 / beta + c1 * dp / (beta * dc)
    eta_e = max(one - v_m, zero) / (one - p1)
    eta_e = min(max(eta_e, zero), rho)
    return MPRiderResponse(v_m, rho - eta_e, eta_e, rho)


def mp_cutoff_residual(
    a: mp.mpf, p1: mp.mpf, p2: mp.mpf, par: Params
) -> mp.mpf:
    m, alpha, _, _ = mp_params(par)
    rr = mp_rider_response(a, p1, p2, par)
    lam1, lam2 = mp_lambdas(a, p1, p2, par)
    return mp_phi(m * a) * (p1 - a) - mp.exp(-m * a) * alpha * (
        rr.eta_repeat * mp_phi(lam1) * (p1 - a)
        + rr.eta_escalate * mp_phi(lam2) * (p2 - a)
    )


def mp_completion(
    a: mp.mpf, p1: mp.mpf, p2: mp.mpf, par: Params
) -> mp.mpf:
    if p1 >= 1:
        return mp.mpf(0)
    m, _, _, _ = mp_params(par)
    rr = mp_rider_response(a, p1, p2, par)
    lam1, lam2 = mp_lambdas(a, p1, p2, par)
    return (mp.mpf(1) - p1) * (
        mp_coverage(m * a)
        + mp.exp(-m * a)
        * (
            rr.eta_repeat * mp_coverage(lam1)
            + rr.eta_escalate * mp_coverage(lam2)
        )
    )


def mp_flat_completion(p: mp.mpf, par: Params) -> mp.mpf:
    m, _, beta, gamma = mp_params(par)
    if p >= 1:
        return mp.mpf(0)
    one = mp.mpf(1)
    return (one - p) * mp_coverage(m * p) + mp.exp(-m * p) * max(
        one - p / beta, mp.mpf(0)
    ) * mp_coverage(gamma * m * p)

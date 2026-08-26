"""Stable implementation of the no-entry P,Q,J cutoff parameterization.

This is numerically independent of the follower-payoff implementation in
``model.py``.  It is usable from m=1e-5 through m=1e6 without exponentiating
``m`` or ``alpha*m`` at the wrong endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from model import Params, coverage, mp, mpf


@dataclass(frozen=True)
class GeometryPoint:
    a: float
    p: float
    q: float
    j: float
    s: float
    r: float


@dataclass(frozen=True)
class GeometryOptimum:
    point: GeometryPoint
    flat_p: float
    flat_value: float
    dynamic_value: float
    escalation_value: float
    local_maxima: tuple[GeometryPoint, ...]
    boundary_value: float


@dataclass(frozen=True)
class MPGeometryCertificate:
    a: mp.mpf
    p: mp.mpf
    q: mp.mpf
    dynamic_value: mp.mpf
    flat_p: mp.mpf
    flat_value: mp.mpf
    escalation_value: mp.mpf
    foc_residual: mp.mpf
    dps: int


def _t_from_d(d: float) -> float:
    """Solve d-t=log(1+t), 0<=t<=d, without overflow."""

    if d <= 0.0:
        return 0.0
    if d < 1e-7:
        # Reversion of d=2t-t^2/2+t^3/3-... .  Newton polishing uses a
        # derivative bounded away from zero and retains relative accuracy.
        t = d / 2.0 + d * d / 16.0 - d**3 / 192.0
        for _ in range(3):
            f = d - t - math.log1p(t)
            t += f / (1.0 + 1.0 / (1.0 + t))
        return min(max(t, 0.0), d)
    return float(
        brentq(
            lambda t: d - t - math.log1p(t),
            0.0,
            d,
            xtol=5e-15 * min(1.0, d),
            rtol=4 * np.finfo(float).eps,
        )
    )


def q_and_s(a: float, par: Params) -> tuple[float, float]:
    if par.gamma != 0.0 or par.alpha <= 0.0:
        raise ValueError("P,Q,J geometry requires gamma=0 and alpha>0")
    if not (0.0 <= a <= par.beta):
        raise ValueError("a must lie in [0,beta]")
    k = par.alpha * par.m
    d = k * (par.beta - a)
    t = _t_from_d(d)  # t=k(beta-Q)
    y = t / k
    q = par.beta - y
    s = t * t / (k * (1.0 + t))
    return q, s


def log_h(a: float, m: float) -> float:
    if a == 0.0:
        return math.log(m)
    x = m * a
    if x < 50.0:
        return math.log(math.expm1(x)) - math.log(a)
    return x + math.log1p(-math.exp(-x)) - math.log(a)


def geometry_point(a: float, par: Params) -> GeometryPoint:
    q, s = q_and_s(a, par)
    log_r = math.log(s) - math.log(par.beta) - log_h(a, par.m) if s > 0 else -math.inf
    r = math.exp(log_r) if log_r > -745.0 else 0.0
    width = 1.0 - a
    disc = max(0.0, width * width - 4.0 * r)
    # Stable smaller quadratic root: p=a+2r/(width+sqrt(disc)).
    u = 0.0 if r == 0.0 else 2.0 * r / (width + math.sqrt(disc))
    p = a + u
    if a == 0.0:
        j = s / par.beta
    else:
        j = (1.0 - p) * p * float(coverage(par.m * a)) / a
    return GeometryPoint(a, p, q, j, s, r)


def j_log_derivative(a: float, par: Params) -> float:
    """Analytic derivative of log J on the open cutoff interval."""

    if not (0.0 < a < par.beta):
        return math.nan
    point = geometry_point(a, par)
    x = par.m * a
    if abs(x) < 1e-4:
        h_log_der = par.m / 2.0 + par.m * x / 12.0 - par.m * x**3 / 720.0
        cov_log_der = -par.m / 2.0 + par.m * x / 12.0 - par.m * x**3 / 720.0
    else:
        h_log_der = par.m / (-math.expm1(-x)) - 1.0 / a
        cov_log_der = par.m / math.expm1(x) - 1.0 / a if x < 700 else -1.0 / a
    y = par.beta - point.q
    r_prime = -point.r * (1.0 / y + h_log_der)
    p_prime = (1.0 - point.p + r_prime) / (1.0 + a - 2.0 * point.p)
    return (
        p_prime * (1.0 - 2.0 * point.p) / (point.p * (1.0 - point.p))
        + cov_log_der
    )


def flat_optimum_noentry(m: float) -> tuple[float, float]:
    hi = math.log1p(m)
    x = float(
        brentq(
            lambda z: math.expm1(z) + z - m,
            0.0,
            hi,
            xtol=max(5e-324, 2e-15 * min(1.0, m)),
            rtol=4 * np.finfo(float).eps,
        )
    )
    p = x / m
    return p, (1.0 - p) * float(coverage(x))


def zero_plateau_threshold(par: Params) -> tuple[float, float, float]:
    point = geometry_point(0.0, par)
    # p_z(1-p_z)=S0/(beta*m), stable smaller root.
    z = point.s / (par.beta * par.m)
    pz = 2.0 * z / (1.0 + math.sqrt(max(0.0, 1.0 - 4.0 * z)))
    return pz, point.q, point.j


def _a_grid(beta: float, n: int) -> np.ndarray:
    linear = np.linspace(0.0, beta, max(n, 17))
    geometric = beta * np.geomspace(1e-14, 1.0, max(n, 17))
    # Endpoint clustering also resolves optima approaching beta.
    upper = beta * (1.0 - np.geomspace(1e-14, 1.0, max(n // 2, 17)))
    return np.unique(np.clip(np.r_[linear, geometric, upper, 0.0, beta], 0.0, beta))


def optimize_geometry(par: Params, *, grid_size: int = 161, xatol: float = 2e-12) -> GeometryOptimum:
    """Global grid plus every visible local refinement of scalar J(a)."""

    if par.gamma != 0.0 or par.alpha <= 0.0:
        raise ValueError("P,Q,J geometry requires gamma=0 and alpha>0")
    xs = _a_grid(par.beta, grid_size)
    pts = [geometry_point(float(a), par) for a in xs]
    candidates: list[GeometryPoint] = list(pts)
    refined: list[GeometryPoint] = []
    for i in range(1, len(xs) - 1):
        # Endpoint clouds from the geometric grid are boundary samples, not
        # stationary local maxima.  Exclude them before refinement.
        endpoint_margin = 1e-12 * max(par.beta, 1.0)
        if not (endpoint_margin < xs[i] < par.beta - endpoint_margin):
            continue
        if pts[i].j >= pts[i - 1].j and pts[i].j >= pts[i + 1].j:
            opt = minimize_scalar(
                lambda a: -geometry_point(float(a), par).j,
                bounds=(float(xs[i - 1]), float(xs[i + 1])),
                method="bounded",
                options={"xatol": xatol, "maxiter": 300},
            )
            point = geometry_point(float(opt.x), par)
            refined.append(point)
            candidates.append(point)

    # Include the repeat-only/flat region p>=beta explicitly for beta<1/2.
    flat_p, flat_value = flat_optimum_noentry(par.m)
    if flat_p >= par.beta:
        boundary = flat_value
    else:
        boundary = max(
            (1.0 - par.beta) * float(coverage(par.m * par.beta)),
            geometry_point(0.0, par).j,
        )
    # Deduplicate overlapping refinements by both cutoff and value.  Do not
    # relabel raw boundary/grid samples as stationary extrema.
    local: list[GeometryPoint] = []
    a_tol = max(20.0 * xatol, 2e-10 * max(par.beta, 1.0))
    v_tol = 5e-13 * max(1.0, max((p.j for p in candidates), default=1.0))
    for point in sorted(refined, key=lambda x: x.a):
        delta = max(50.0 * xatol, 2e-8 * max(par.beta, 1.0))
        lo = max(np.nextafter(0.0, 1.0), point.a - delta)
        hi = min(np.nextafter(par.beta, 0.0), point.a + delta)
        # A true interior maximum has positive log derivative on its left and
        # negative log derivative on its right.  This rejects flat-looking
        # boundary clouds caused by binary64 value ties.
        if not (lo < point.a < hi):
            continue
        if not (j_log_derivative(lo, par) > 0.0 and j_log_derivative(hi, par) < 0.0):
            continue
        if local and abs(point.a - local[-1].a) <= a_tol and abs(point.j - local[-1].j) <= v_tol:
            if point.j > local[-1].j:
                local[-1] = point
        else:
            local.append(point)
    best_j = max(candidates, key=lambda x: x.j)
    dynamic = max(best_j.j, boundary, flat_value)
    # If the repeat-only flat region wins, retain its actual policy in the
    # scalar point's p field only through the separate flat_p return value.
    return GeometryOptimum(
        best_j,
        flat_p,
        flat_value,
        dynamic,
        dynamic - flat_value,
        tuple(local),
        boundary,
    )


# ---------------------- arbitrary precision certificates -------------------


def _mp_t_from_d(d: mp.mpf) -> mp.mpf:
    if d <= 0:
        return mp.mpf(0)
    t = d / 2 if d < 1 else d - mp.log1p(d)
    t = min(max(t, mp.mpf(0)), d)
    for _ in range(100):
        f = d - t - mp.log1p(t)
        step = f / (-1 - 1 / (1 + t))
        nxt = t - step
        if not (0 <= nxt <= d):
            nxt = (t + (mp.mpf(0) if f < 0 else d)) / 2
        if abs(nxt - t) <= mp.eps * max(1, abs(t)):
            return nxt
        t = nxt
    return t


def mp_geometry_point(a: mp.mpf, par: Params) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    m, alpha, beta = (mpf(x) for x in (par.m, par.alpha, par.beta))
    k = alpha * m
    d = k * (beta - a)
    t = _mp_t_from_d(d)
    q = beta - t / k
    s = t * t / (k * (1 + t))
    h = m if a == 0 else mp.expm1(m * a) / a
    r = s / (beta * h)
    width = 1 - a
    u = 2 * r / (width + mp.sqrt(width * width - 4 * r)) if r else mp.mpf(0)
    p = a + u
    j = s / beta if a == 0 else (1 - p) * p * (-mp.expm1(-m * a)) / a
    return p, q, j, s, r


def mp_j_log_derivative(a: mp.mpf, par: Params) -> mp.mpf:
    m, _, beta = (mpf(x) for x in (par.m, par.alpha, par.beta))
    p, q, _, _, r = mp_geometry_point(a, par)
    x = m * a
    h_log_der = m / (-mp.expm1(-x)) - 1 / a
    cov_log_der = m / mp.expm1(x) - 1 / a
    r_prime = -r * (1 / (beta - q) + h_log_der)
    p_prime = (1 - p + r_prime) / (1 + a - 2 * p)
    return p_prime * (1 - 2 * p) / (p * (1 - p)) + cov_log_der


def certify_geometry_optimum_mp(
    par: Params,
    a_start: float | None = None,
    *,
    dps: int = 90,
) -> MPGeometryCertificate:
    """Refine a double global candidate and evaluate V without cancellation."""

    if par.gamma != 0.0 or par.alpha <= 0.0:
        raise ValueError("P,Q,J geometry requires gamma=0 and alpha>0")
    if a_start is None:
        a_start = optimize_geometry(par).point.a
    with mp.workdps(dps):
        beta = mpf(par.beta)
        x0 = mpf(a_start)
        edge = beta * mp.mpf(10) ** (-(dps // 2))
        x1 = max(edge, x0 / 2)
        x2 = min(beta - edge, max(x0 * 2, x0 + beta * mp.mpf("1e-8")))
        g1, g2 = mp_j_log_derivative(x1, par), mp_j_log_derivative(x2, par)
        # Expand around the double global candidate until the stationary
        # maximum is bracketed by +/− log-derivative signs.
        for _ in range(100):
            if g1 > 0 and g2 < 0:
                break
            if g1 <= 0:
                x1 = max(edge, x1 / 2)
                g1 = mp_j_log_derivative(x1, par)
            if g2 >= 0:
                x2 = min(beta - edge, x2 + (beta - x2) / 2)
                g2 = mp_j_log_derivative(x2, par)
        else:
            raise RuntimeError("could not bracket high-precision J stationary point")
        target = mp.mpf(10) ** (-(dps - 15))
        try:
            trial = mp.findroot(
                lambda z: mp_j_log_derivative(z, par),
                (x1, x2),
                solver="anderson",
                tol=target,
                maxsteps=80,
            )
            if not (x1 < trial < x2) or abs(mp_j_log_derivative(trial, par)) > mp.sqrt(target):
                raise ValueError("invalid bracketed refinement")
            a = trial
        except (ValueError, ZeroDivisionError):
            while x2 - x1 > target * max(1, abs(x0)):
                mid = (x1 + x2) / 2
                gm = mp_j_log_derivative(mid, par)
                if gm > 0:
                    x1, g1 = mid, gm
                else:
                    x2, g2 = mid, gm
            a = (x1 + x2) / 2
        if not (0 < a < beta):
            raise RuntimeError("high-precision stationary refinement left (0,beta)")
        p, q, dynamic, _, _ = mp_geometry_point(a, par)
        m = mpf(par.m)
        x_guess = mpf(flat_optimum_noentry(par.m)[0]) * m
        xflat = mp.findroot(lambda x: mp.expm1(x) + x - m, x_guess)
        flat_p = xflat / m
        flat = (1 - flat_p) * (-mp.expm1(-xflat))
        return MPGeometryCertificate(
            a,
            p,
            q,
            dynamic,
            flat_p,
            flat,
            dynamic - flat,
            mp_j_log_derivative(a, par),
            dps,
        )

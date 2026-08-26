"""Independent numerical model with discounted incumbent continuation payoffs.

The correction studied here is deliberately narrow:

* an incumbent driver's period-2 net payoff is ``delta * (p-c)``;
* a fresh entrant's terminal payoff is ``p-c``;
* physical survival, acceptance, rationing, rider payoffs, and completion are
  not discounted.

Consequently ``delta`` multiplies the focal incumbent's wait payoff but does
not multiply either post-failure supply intensity or completion.  This module
is standalone and leaves the baseline implementation untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import sys
from typing import Iterable, NamedTuple

import numpy as np
from scipy.optimize import brentq, minimize_scalar


_VENDOR = Path(__file__).resolve().parent / "_vendor"
if _VENDOR.exists() and str(_VENDOR) not in sys.path:
    sys.path.insert(0, str(_VENDOR))
import mpmath as mp  # noqa: E402


@dataclass(frozen=True)
class DiscountParams:
    m: float
    alpha: float
    beta: float
    gamma: float = 0.0
    delta: float = 1.0

    def validate(self) -> None:
        if not self.m > 0:
            raise ValueError("m must be positive")
        if not 0 <= self.alpha <= 1:
            raise ValueError("alpha must lie in [0,1]")
        if not 0 < self.beta < 1:
            raise ValueError("beta must lie in (0,1)")
        if self.gamma < 0:
            raise ValueError("gamma must be nonnegative")
        if not 0 < self.delta <= 1:
            raise ValueError("incumbent discount delta must lie in (0,1]")


class RiderResponse(NamedTuple):
    switch: float
    repeat: float
    rescue: float
    continuation: float


class MPRiderResponse(NamedTuple):
    switch: mp.mpf
    repeat: mp.mpf
    rescue: mp.mpf
    continuation: mp.mpf


def share(x: float | np.ndarray) -> float | np.ndarray:
    """E[1/(1+Pois(x))], with a stable zero expansion."""

    z = np.asarray(x, dtype=float)
    ans = np.empty_like(z)
    small = np.abs(z) < 1e-7
    y = z[small]
    ans[small] = 1 - y / 2 + y * y / 6 - y**3 / 24 + y**4 / 120
    y = z[~small]
    ans[~small] = -np.expm1(-y) / y
    return float(ans) if ans.ndim == 0 else ans


def cover(x: float | np.ndarray) -> float | np.ndarray:
    z = np.asarray(x, dtype=float)
    ans = -np.expm1(-z)
    return float(ans) if ans.ndim == 0 else ans


def rho_mass(p: float, beta: float) -> float:
    if p >= 1:
        return 0.0
    return max(1 - p / beta, 0.0) / (1 - p)


def intensities(a: float, p: float, q: float, par: DiscountParams) -> tuple[float, float]:
    return (
        max(0.0, par.m * (par.alpha * (p - a) + par.gamma * p)),
        max(0.0, par.m * (par.alpha * (q - a) + par.gamma * q)),
    )


def rider_response(a: float, p: float, q: float, par: DiscountParams) -> RiderResponse:
    """Posting-conditional rider masses after first-period failure."""

    if p >= 1:
        return RiderResponse(math.inf, 0.0, 0.0, 0.0)
    rho = rho_mass(p, par.beta)
    if rho == 0 or q == p or par.alpha + par.gamma == 0:
        return RiderResponse(math.inf, rho, 0.0, rho)
    dp = q - p
    lam1, _ = intensities(a, p, q, par)
    dlam = par.m * (par.alpha + par.gamma) * dp
    dc = math.exp(-lam1) * (-math.expm1(-dlam))
    if dc == 0 or par.beta * dc == 0:
        return RiderResponse(math.inf, rho, 0.0, rho)
    c1 = float(cover(lam1))
    switch = q / par.beta + c1 * dp / (par.beta * dc)
    rescue = max(1 - switch, 0.0) / (1 - p)
    rescue = min(max(rescue, 0.0), rho)
    return RiderResponse(switch, rho - rescue, rescue, rho)


def cutoff_residual(a: float, p: float, q: float, par: DiscountParams) -> float:
    """Cutoff type's accept payoff minus discounted wait payoff."""

    if not 0 <= a <= p:
        raise ValueError("cutoff must lie in [0,p]")
    rr = rider_response(a, p, q, par)
    lam1, lam2 = intensities(a, p, q, par)
    accept = float(share(par.m * a)) * (p - a)
    wait = par.delta * par.alpha * math.exp(-par.m * a) * (
        rr.repeat * float(share(lam1)) * (p - a)
        + rr.rescue * float(share(lam2)) * (q - a)
    )
    return accept - wait


def cutoff_residual_array(
    aa: np.ndarray, p: float, q: float, par: DiscountParams
) -> np.ndarray:
    a = np.clip(np.asarray(aa, dtype=float), 0.0, p)
    lam1 = par.m * (par.alpha * (p - a) + par.gamma * p)
    lam2 = par.m * (par.alpha * (q - a) + par.gamma * q)
    rho = rho_mass(p, par.beta)
    if rho == 0 or q == p or par.alpha + par.gamma == 0:
        rescue = np.zeros_like(a)
    else:
        dp = q - p
        dlam = par.m * (par.alpha + par.gamma) * dp
        dc = np.exp(-lam1) * (-np.expm1(-dlam))
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            switch = q / par.beta + cover(lam1) * dp / (par.beta * dc)
        rescue = np.clip(np.maximum(1 - switch, 0.0) / (1 - p), 0.0, rho)
    repeat = rho - rescue
    return share(par.m * a) * (p - a) - par.delta * par.alpha * np.exp(-par.m * a) * (
        repeat * share(lam1) * (p - a) + rescue * share(lam2) * (q - a)
    )


def completion(a: float, p: float, q: float, par: DiscountParams) -> float:
    """Unconditional physical completion; delta correctly does not enter."""

    if p >= 1:
        return 0.0
    rr = rider_response(a, p, q, par)
    lam1, lam2 = intensities(a, p, q, par)
    conditional = float(cover(par.m * a)) + math.exp(-par.m * a) * (
        rr.repeat * float(cover(lam1)) + rr.rescue * float(cover(lam2))
    )
    return (1 - p) * conditional


def flat_completion(p: float, par: DiscountParams) -> float:
    """Flat benchmark.  Its cutoff and completion are independent of delta."""

    if p >= 1:
        return 0.0
    return (1 - p) * float(cover(par.m * p)) + math.exp(-par.m * p) * max(
        1 - p / par.beta, 0.0
    ) * float(cover(par.gamma * par.m * p))


@dataclass(frozen=True)
class Equilibria:
    cutoffs: tuple[float, ...]
    kinds: tuple[str, ...]
    residuals: tuple[float, ...]

    @property
    def multiplicity(self) -> int:
        return len(self.cutoffs)


def _nodes(lo: float, hi: float, n: int) -> np.ndarray:
    if hi <= lo:
        return np.array([lo])
    u = np.linspace(0.0, 1.0, n)
    cosine = (1 - np.cos(np.linspace(0.0, math.pi, n))) / 2
    return lo + (hi - lo) * np.unique(np.r_[u, cosine])


def _dedup_roots(items: list[tuple[float, str, float]], p: float) -> list[tuple[float, str, float]]:
    items.sort(key=lambda z: z[0])
    ans: list[tuple[float, str, float]] = []
    tol = max(2e-10, 2e-8 * p)
    rank = {"boundary-0": 0, "boundary-p": 0, "bracket": 1, "tangent": 2, "sample": 3}
    for item in items:
        if ans and abs(item[0] - ans[-1][0]) <= tol:
            if (abs(item[2]), rank.get(item[1], 9)) < (abs(ans[-1][2]), rank.get(ans[-1][1], 9)):
                ans[-1] = item
        else:
            ans.append(item)
    return ans


def find_equilibria(
    p: float,
    q: float,
    par: DiscountParams,
    *,
    grid_size: int = 129,
    residual_tol: float = 5e-11,
) -> Equilibria:
    """Deterministic all-visible-root scan with sign brackets and tangency search."""

    if not 0 <= p <= q <= 1:
        raise ValueError("policy must satisfy 0 <= p <= q <= 1")
    if p == 0:
        f0 = cutoff_residual(0.0, p, q, par)
        return Equilibria((0.0,), ("boundary-0",), (f0,))
    fun = lambda x: cutoff_residual(float(x), p, q, par)
    f0, fp = fun(0.0), fun(p)
    scale = max(p, q, 1e-4)
    items: list[tuple[float, str, float]] = []
    if f0 <= 0.0:
        items.append((0.0, "boundary-0", f0))
    # At p the residual can be a negative subnormal under thick-market
    # underflow.  The exact boundary condition is structural: it holds iff
    # the rescue displacement payoff vanishes, not when fp is merely close
    # to zero in binary64.
    upper_is_equilibrium = (
        q == p or par.alpha == 0.0 or rider_response(p, p, q, par).rescue == 0.0
    )
    if upper_is_equilibrium:
        items.append((p, "boundary-p", fp))
    xs = _nodes(0.0, p, max(33, grid_size))
    fs = cutoff_residual_array(xs, p, q, par)
    for i in range(len(xs) - 1):
        lo, hi = float(xs[i]), float(xs[i + 1])
        flo, fhi = float(fs[i]), float(fs[i + 1])
        if flo * fhi < 0:
            root = float(brentq(fun, lo, hi, xtol=5e-15, rtol=4 * np.finfo(float).eps))
            if 0 < root < p:
                items.append((root, "bracket", fun(root)))
        elif flo == 0 and 0 < lo < p:
            items.append((lo, "sample", flo))
    af = np.abs(fs)
    for i in range(1, len(xs) - 1):
        if af[i] <= af[i - 1] and af[i] <= af[i + 1] and af[i] < 2e-5 * scale:
            lo, hi = float(xs[i - 1]), float(xs[i + 1])
            opt = minimize_scalar(lambda z: abs(fun(float(z))), bounds=(lo, hi), method="bounded",
                                  options={"xatol": 2e-14, "maxiter": 120})
            if opt.fun <= residual_tol * scale and 0 < opt.x < p:
                items.append((float(opt.x), "tangent", fun(float(opt.x))))
    clean = [z for z in _dedup_roots(items, p)
             if z[1].startswith("boundary") or abs(z[2]) <= residual_tol * scale]
    if not clean:
        # With very large ma or tiny delta the unique interior root can lie
        # less than one binary64 ulp below p.  The exact upper boundary still
        # fails when rescue is active, but no float represents the root.  Keep
        # an explicitly labelled limiting proxy; arbitrary precision is used
        # for every reported/candidate certificate of this kind.
        if f0 > 0 and not upper_is_equilibrium:
            clean = [(p, "near-p-limit", fp)]
        else:
            raise RuntimeError("no cutoff equilibrium found")
    return Equilibria(tuple(z[0] for z in clean), tuple(z[1] for z in clean), tuple(z[2] for z in clean))


def pessimistic_value(
    p: float, q: float, par: DiscountParams, *, grid_size: int = 129
) -> tuple[float, Equilibria, tuple[float, ...]]:
    eq = find_equilibria(p, q, par, grid_size=grid_size)
    values = tuple(completion(a, p, q, par) for a in eq.cutoffs)
    return min(values), eq, values


# ---------------------------- high precision -----------------------------


def mpf(x: object) -> mp.mpf:
    return x if isinstance(x, mp.mpf) else mp.mpf(str(x))


def mp_share(x: mp.mpf) -> mp.mpf:
    return mp.mpf(1) if x == 0 else -mp.expm1(-x) / x


def mp_cover(x: mp.mpf) -> mp.mpf:
    return -mp.expm1(-x)


def mp_intensities(
    a: mp.mpf, p: mp.mpf, q: mp.mpf, par: DiscountParams
) -> tuple[mp.mpf, mp.mpf]:
    m, alpha, gamma = mpf(par.m), mpf(par.alpha), mpf(par.gamma)
    return m * (alpha * (p - a) + gamma * p), m * (alpha * (q - a) + gamma * q)


def mp_rider_response(
    a: mp.mpf, p: mp.mpf, q: mp.mpf, par: DiscountParams
) -> MPRiderResponse:
    one, zero = mp.mpf(1), mp.mpf(0)
    beta = mpf(par.beta)
    if p >= one:
        return MPRiderResponse(mp.inf, zero, zero, zero)
    rho = max(one - p / beta, zero) / (one - p)
    ag = mpf(par.alpha) + mpf(par.gamma)
    if rho == 0 or q == p or ag == 0:
        return MPRiderResponse(mp.inf, rho, zero, rho)
    lam1, _ = mp_intensities(a, p, q, par)
    dlam = mpf(par.m) * ag * (q - p)
    dc = mp.exp(-lam1) * (-mp.expm1(-dlam))
    switch = q / beta + mp_cover(lam1) * (q - p) / (beta * dc)
    rescue = min(max(max(one - switch, zero) / (one - p), zero), rho)
    return MPRiderResponse(switch, rho - rescue, rescue, rho)


def mp_cutoff_residual(
    a: mp.mpf, p: mp.mpf, q: mp.mpf, par: DiscountParams
) -> mp.mpf:
    rr = mp_rider_response(a, p, q, par)
    lam1, lam2 = mp_intensities(a, p, q, par)
    m, alpha, delta = mpf(par.m), mpf(par.alpha), mpf(par.delta)
    return mp_share(m * a) * (p - a) - delta * alpha * mp.exp(-m * a) * (
        rr.repeat * mp_share(lam1) * (p - a)
        + rr.rescue * mp_share(lam2) * (q - a)
    )


def mp_completion(
    a: mp.mpf, p: mp.mpf, q: mp.mpf, par: DiscountParams
) -> mp.mpf:
    if p >= 1:
        return mp.mpf(0)
    rr = mp_rider_response(a, p, q, par)
    lam1, lam2 = mp_intensities(a, p, q, par)
    m = mpf(par.m)
    return (1 - p) * (
        mp_cover(m * a)
        + mp.exp(-m * a) * (rr.repeat * mp_cover(lam1) + rr.rescue * mp_cover(lam2))
    )


Interval = tuple[mp.mpf, mp.mpf]


def _imul(x: Interval, y: Interval) -> Interval:
    z = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(z), max(z)


def residual_enclosure(
    lo: mp.mpf, hi: mp.mpf, p: mp.mpf, q: mp.mpf, par: DiscountParams
) -> Interval:
    """Natural interval-style enclosure; retained boxes are never discarded."""

    m, alpha, delta = mpf(par.m), mpf(par.alpha), mpf(par.delta)
    x1, x2 = (p - hi, p - lo), (q - hi, q - lo)
    accept = _imul((mp_share(m * hi), mp_share(m * lo)), x1)
    reach = (mp.exp(-m * hi), mp.exp(-m * lo))
    l1lo, l2lo = mp_intensities(lo, p, q, par)
    l1hi, l2hi = mp_intensities(hi, p, q, par)
    s1, s2 = (mp_share(l1lo), mp_share(l1hi)), (mp_share(l2lo), mp_share(l2hi))
    rrlo, rrhi = mp_rider_response(lo, p, q, par), mp_rider_response(hi, p, q, par)
    er, ee = (rrhi.repeat, rrlo.repeat), (rrlo.rescue, rrhi.rescue)
    repeat = _imul(_imul(er, s1), x1)
    rescue = _imul(_imul(ee, s2), x2)
    inside = repeat[0] + rescue[0], repeat[1] + rescue[1]
    wait = _imul(_imul(reach, (delta * alpha, delta * alpha)), inside)
    raw = accept[0] - wait[1], accept[1] - wait[0]
    pad = 128 * mp.eps * max(1, abs(raw[0]), abs(raw[1]))
    return raw[0] - pad, raw[1] + pad


@dataclass(frozen=True)
class RootBox:
    lo: mp.mpf
    hi: mp.mpf
    f_lo: mp.mpf
    f_hi: mp.mpf
    kind: str

    @property
    def root(self) -> mp.mpf:
        return (self.lo + self.hi) / 2


@dataclass(frozen=True)
class MPEquilibria:
    p: mp.mpf
    q: mp.mpf
    boundary_zero: bool
    boundary_p: bool
    roots: tuple[RootBox, ...]
    unresolved: tuple[RootBox, ...]
    excluded: int

    @property
    def cutoffs(self) -> tuple[mp.mpf, ...]:
        ans: list[mp.mpf] = []
        if self.boundary_zero:
            ans.append(mp.mpf(0))
        ans.extend(z.root for z in self.roots)
        if self.boundary_p:
            ans.append(self.p)
        return tuple(ans)


def _merge_boxes(boxes: Iterable[Interval], gap: mp.mpf) -> list[Interval]:
    ordered = sorted(boxes)
    ans: list[list[mp.mpf]] = []
    for lo, hi in ordered:
        if ans and lo <= ans[-1][1] + gap:
            ans[-1][1] = max(ans[-1][1], hi)
        else:
            ans.append([lo, hi])
    return [(z[0], z[1]) for z in ans]


def isolate_equilibria_mp(
    p_in: float | str | mp.mpf,
    q_in: float | str | mp.mpf,
    par: DiscountParams,
    *,
    dps: int = 70,
    box_tol: str = "1e-20",
    max_depth: int = 160,
) -> MPEquilibria:
    """Globally retain every interval box not excluded by factor bounds."""

    with mp.workdps(dps):
        p, q, tol = mpf(p_in), mpf(q_in), mpf(box_tol)
        fun = lambda z: mp_cutoff_residual(z, p, q, par)
        f0, fp = fun(mp.mpf(0)), fun(p)
        b0, bp = f0 <= 0, fp >= 0
        if p == 0:
            return MPEquilibria(p, q, b0, False, (), (), 0)
        queue = [(mp.mpf(0), p, 0)]
        terminal: list[Interval] = []
        excluded = 0
        while queue:
            lo, hi, depth = queue.pop()
            enclosure = residual_enclosure(lo, hi, p, q, par)
            if enclosure[0] > 0 or enclosure[1] < 0:
                excluded += 1
                continue
            if hi - lo <= tol or depth >= max_depth:
                terminal.append((lo, hi))
                continue
            mid = (lo + hi) / 2
            queue.append((mid, hi, depth + 1))
            queue.append((lo, mid, depth + 1))
        roots: list[RootBox] = []
        unresolved: list[RootBox] = []
        for lo, hi in _merge_boxes(terminal, 2 * tol):
            if b0 and hi <= 8 * tol:
                continue
            if bp and p - lo <= 8 * tol:
                continue
            nodes = [lo + (hi - lo) * i / 64 for i in range(65)]
            values = [fun(x) for x in nodes]
            brackets = []
            for i in range(64):
                if values[i] * values[i + 1] < 0:
                    brackets.append((nodes[i], nodes[i + 1], values[i], values[i + 1]))
            if not brackets:
                box = RootBox(lo, hi, values[0], values[-1], "unresolved")
                unresolved.append(box)
                roots.append(box)
                continue
            for blo, bhi, flo, fhi in brackets:
                while bhi - blo > tol / 16:
                    mid = (blo + bhi) / 2
                    fm = fun(mid)
                    if flo * fm <= 0:
                        bhi, fhi = mid, fm
                    else:
                        blo, flo = mid, fm
                roots.append(RootBox(blo, bhi, flo, fhi, "sign-change"))
        roots.sort(key=lambda z: z.root)
        dedup: list[RootBox] = []
        for z in roots:
            if dedup and abs(z.root - dedup[-1].root) <= 8 * tol:
                if z.kind == "sign-change" and dedup[-1].kind != "sign-change":
                    dedup[-1] = z
            else:
                dedup.append(z)
        unresolved_final = tuple(z for z in dedup if z.kind == "unresolved")
        return MPEquilibria(p, q, b0, bp, tuple(dedup), unresolved_final, excluded)


# -------------------------- no-entry geometry ----------------------------


@dataclass(frozen=True)
class GeometryPoint:
    a: float
    p: float
    q: float
    value: float
    rescue_surplus: float
    implementer_rhs: float


@dataclass(frozen=True)
class GeometryOptimum:
    point: GeometryPoint
    dynamic_value: float
    flat_p: float
    flat_value: float
    gain: float
    stationary_maxima: tuple[GeometryPoint, ...]


def _t_from_span(span: float) -> float:
    """Solve span-t=log(1+t), avoiding exp(span)."""

    if span <= 0:
        return 0.0
    if span < 1e-7:
        t = span / 2 + span * span / 16 - span**3 / 192
        for _ in range(3):
            f = span - t - math.log1p(t)
            t += f / (1 + 1 / (1 + t))
        return min(max(t, 0.0), span)
    return float(brentq(lambda t: span - t - math.log1p(t), 0.0, span,
                        xtol=max(5e-324, 5e-15 * min(1.0, span)),
                        rtol=4 * np.finfo(float).eps))


def _log_h(a: float, m: float) -> float:
    if a == 0:
        return math.log(m)
    x = m * a
    if x < 50:
        return math.log(math.expm1(x)) - math.log(a)
    return x + math.log1p(-math.exp(-x)) - math.log(a)


def geometry_point(a: float, par: DiscountParams) -> GeometryPoint:
    """Tangent rescue menu implementing cutoff a when gamma=0."""

    if par.gamma != 0 or par.alpha <= 0:
        raise ValueError("geometry requires gamma=0 and alpha>0")
    if not 0 <= a <= par.beta:
        raise ValueError("a must lie in [0,beta]")
    k = par.alpha * par.m
    t = _t_from_span(k * (par.beta - a))  # t = k(beta-q)
    q = par.beta - t / k
    surplus = t * t / (k * (1 + t))  # (beta-q)[1-exp(-k(q-a))]
    log_rhs = (math.log(par.delta) + math.log(surplus) - math.log(par.beta)
               - _log_h(a, par.m)) if surplus > 0 else -math.inf
    rhs = math.exp(log_rhs) if log_rhs > -745 else 0.0
    width = 1 - a
    disc = max(0.0, width * width - 4 * rhs)
    step = 0.0 if rhs == 0 else 2 * rhs / (width + math.sqrt(disc))
    p = a + step
    value = ((1 - p) * float(cover(par.m * a))
             + math.exp(-par.m * a) * surplus / par.beta)
    return GeometryPoint(a, p, q, value, surplus, rhs)


def optimize_flat_noentry(m: float) -> tuple[float, float]:
    hi = math.log1p(m)
    x = float(brentq(lambda z: math.expm1(z) + z - m, 0.0, hi,
                     xtol=max(5e-324, 2e-15 * min(1.0, m)),
                     rtol=4 * np.finfo(float).eps))
    p = x / m
    return p, (1 - p) * float(cover(x))


def _a_grid(beta: float, n: int) -> np.ndarray:
    linear = np.linspace(0.0, beta, max(n, 17))
    low = beta * np.geomspace(1e-14, 1.0, max(n, 17))
    high = beta * (1 - np.geomspace(1e-14, 1.0, max(n // 2, 17)))
    return np.unique(np.clip(np.r_[linear, low, high, 0.0, beta], 0.0, beta))


def optimize_geometry(
    par: DiscountParams, *, grid_size: int = 161, xatol: float = 2e-12
) -> GeometryOptimum:
    xs = _a_grid(par.beta, grid_size)
    pts = [geometry_point(float(a), par) for a in xs]
    candidates = list(pts)
    refined: list[GeometryPoint] = []
    for i in range(1, len(xs) - 1):
        if pts[i].value >= pts[i - 1].value and pts[i].value >= pts[i + 1].value:
            if xs[i] <= 1e-12 or xs[i] >= par.beta - 1e-12:
                continue
            opt = minimize_scalar(lambda z: -geometry_point(float(z), par).value,
                                  bounds=(float(xs[i - 1]), float(xs[i + 1])), method="bounded",
                                  options={"xatol": xatol, "maxiter": 300})
            point = geometry_point(float(opt.x), par)
            refined.append(point)
            candidates.append(point)
    flat_p, flat = optimize_flat_noentry(par.m)
    best = max(candidates, key=lambda z: z.value)
    dynamic = max(best.value, flat)
    local: list[GeometryPoint] = []
    atol = max(20 * xatol, 2e-9 * max(1.0, par.beta))
    vtol = 1e-12 * max(1.0, dynamic)
    for z in sorted(refined, key=lambda x: x.a):
        # Verify with actual one-sided values and de-duplicate endpoint clouds.
        h = max(50 * xatol, 2e-7 * max(1.0, par.beta))
        if not h < z.a < par.beta - h:
            continue
        if not (geometry_point(z.a - h, par).value < z.value
                and geometry_point(z.a + h, par).value < z.value):
            continue
        if local and abs(z.a - local[-1].a) <= atol and abs(z.value - local[-1].value) <= vtol:
            if z.value > local[-1].value:
                local[-1] = z
        else:
            local.append(z)
    return GeometryOptimum(best, dynamic, flat_p, flat, dynamic - flat, tuple(local))


def mp_geometry_point(
    a_in: float | str | mp.mpf, par: DiscountParams
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    """High-precision (p,q,value,surplus) for the no-entry tangent menu."""

    a = mpf(a_in)
    m, alpha, beta, delta = map(mpf, (par.m, par.alpha, par.beta, par.delta))
    k = alpha * m
    span = k * (beta - a)
    t = span / 2 if span < 1 else span - mp.log1p(span)
    for _ in range(100):
        f = span - t - mp.log1p(t)
        nxt = t + f / (1 + 1 / (1 + t))
        if abs(nxt - t) <= mp.eps * max(1, abs(t)):
            t = nxt
            break
        t = min(max(nxt, mp.mpf(0)), span)
    q = beta - t / k
    surplus = t * t / (k * (1 + t))
    h = m if a == 0 else mp.expm1(m * a) / a
    rhs = delta * surplus / (beta * h)
    width = 1 - a
    step = 2 * rhs / (width + mp.sqrt(width * width - 4 * rhs)) if rhs else mp.mpf(0)
    p = a + step
    value = (1 - p) * mp_cover(m * a) + mp.exp(-m * a) * surplus / beta
    return p, q, value, surplus


def corrected_local_coefficient(p: float, par: DiscountParams) -> float:
    """Right derivative at (p,p) when limiting rescue is active."""

    if not 0 < p < par.beta or par.alpha + par.gamma == 0:
        return 0.0
    x = par.m * p
    r = math.exp(-x)
    e = math.exp(-par.gamma * x)
    sigma = float(share(x))
    ell = float(share(par.gamma * x))
    rho = (1 - p / par.beta) / (1 - p)
    bar_v = (p + (1 - e) / (par.m * e * (par.alpha + par.gamma))) / par.beta
    eta0 = max(1 - bar_v, 0.0) / (1 - p)
    if eta0 == 0:
        return 0.0
    denom = sigma - r * par.delta * par.alpha * ell * rho
    b = 1 - rho + rho * e * (1 - par.alpha)
    kappa = r * par.delta * par.alpha * ell * eta0 / denom
    return par.m * (1 - p) * r * (e * (par.alpha + par.gamma) * eta0 - kappa * b)


def old_local_coefficient(p: float, par: DiscountParams) -> float:
    """Counterfactual coefficient obtained by silently setting delta=1."""

    return corrected_local_coefficient(p, DiscountParams(
        par.m, par.alpha, par.beta, par.gamma, 1.0
    ))

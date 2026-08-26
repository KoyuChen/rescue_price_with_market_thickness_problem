"""All-branch equilibrium search and high-precision root isolation.

The fast path is designed for tens of thousands of policy evaluations during
global optimization.  The independent high-precision path uses monotonic
interval enclosures to exclude root-free boxes, retains every non-excluded
box, and certifies ordinary roots by a sign-changing mpmath bracket.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Literal

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from model import (
    Params,
    completion,
    cutoff_residual,
    cutoff_residual_array,
    lambdas,
    mp,
    mp_completion,
    mp_cutoff_residual,
    mp_lambdas,
    mp_phi,
    mp_rider_response,
    mpf,
    phi,
    rider_response,
)


@dataclass(frozen=True)
class FastEquilibria:
    cutoffs: tuple[float, ...]
    kinds: tuple[str, ...]
    residuals: tuple[float, ...]
    kink: float | None

    @property
    def multiplicity(self) -> int:
        return len(self.cutoffs)


def escalation_kink(p1: float, p2: float, par: Params) -> float | None:
    """Return the unique a with v_M(a)=1, if it lies strictly inside."""

    if p2 == p1 or par.alpha + par.gamma == 0.0 or p1 >= par.beta:
        return None

    def g(a: float) -> float:
        return rider_response(a, p1, p2, par).v_m - 1.0

    g0, g1 = g(0.0), g(p1)
    if not (g0 > 0.0 and g1 < 0.0):
        return None
    return float(brentq(g, 0.0, p1, xtol=5e-15, rtol=4 * np.finfo(float).eps))


def _deduplicate(items: list[tuple[float, str, float]], tol: float) -> list[tuple[float, str, float]]:
    if not items:
        return []
    items.sort(key=lambda z: z[0])
    groups: list[list[tuple[float, str, float]]] = [[items[0]]]
    for item in items[1:]:
        if abs(item[0] - groups[-1][-1][0]) <= tol:
            groups[-1].append(item)
        else:
            groups.append([item])
    ans: list[tuple[float, str, float]] = []
    rank = {"boundary-0": 0, "boundary-p1": 0, "bracket": 1, "sample": 2, "tangent-candidate": 3}
    for group in groups:
        best = min(group, key=lambda z: (abs(z[2]), rank.get(z[1], 9)))
        ans.append(best)
    return ans


def find_equilibria_fast(
    p1: float,
    p2: float,
    par: Params,
    *,
    grid_size: int = 161,
    residual_tol: float = 2e-10,
) -> FastEquilibria:
    """Find all visible cutoff branches with deterministic global sampling.

    Sign-changing roots are bracketing certificates in binary64.  Possible
    even-multiplicity roots are searched for as local minima of |f| and are
    explicitly marked as candidates.  Final reported policies should always
    be passed through :func:`isolate_equilibria_mp`.
    """

    if not (0.0 <= p1 <= p2 <= 1.0):
        raise ValueError("policy must satisfy 0 <= p1 <= p2 <= 1")
    if p1 == 0.0:
        f0 = cutoff_residual(0.0, p1, p2, par)
        return FastEquilibria((0.0,), ("boundary-0",), (f0,), None)

    fun = lambda x: cutoff_residual(float(x), p1, p2, par)
    kink = escalation_kink(p1, p2, par)
    breakpoints = [0.0]
    if kink is not None:
        breakpoints.append(kink)
    breakpoints.append(p1)

    candidates: list[tuple[float, str, float]] = []
    f0, fp = fun(0.0), fun(p1)
    scale = max(p1, p2, 1e-3)
    b_tol = 64 * np.finfo(float).eps * scale
    if f0 <= b_tol:
        candidates.append((0.0, "boundary-0", f0))
    if fp >= -b_tol:
        candidates.append((p1, "boundary-p1", fp))

    # Allocate at least grid_size points to each analytic piece.  The union of
    # uniform and cosine-spaced nodes catches narrow endpoint branches better
    # than either grid alone.
    for left, right in zip(breakpoints[:-1], breakpoints[1:]):
        if right <= left:
            continue
        n = max(33, grid_size)
        u = np.linspace(0.0, 1.0, n)
        c = (1.0 - np.cos(np.linspace(0.0, math.pi, n))) / 2.0
        xs = np.clip(left + (right - left) * np.unique(np.r_[u, c]), left, right)
        fs = cutoff_residual_array(xs, p1, p2, par)

        for x, fx in zip(xs[1:-1], fs[1:-1]):
            if abs(fx) <= residual_tol * scale:
                candidates.append((float(x), "sample", float(fx)))

        for i in range(len(xs) - 1):
            xlo, xhi = float(xs[i]), float(xs[i + 1])
            flo, fhi = float(fs[i]), float(fs[i + 1])
            if flo == 0.0:
                if xlo not in (0.0, p1):
                    candidates.append((xlo, "sample", flo))
            elif flo * fhi < 0.0:
                sflo, sfhi = fun(xlo), fun(xhi)
                if sflo * sfhi < 0.0:
                    root = float(brentq(fun, xlo, xhi, xtol=5e-15, rtol=4 * np.finfo(float).eps))
                    candidates.append((root, "bracket", fun(root)))
                elif abs(sflo) <= residual_tol * scale:
                    candidates.append((xlo, "sample", sflo))
                elif abs(sfhi) <= residual_tol * scale:
                    candidates.append((xhi, "sample", sfhi))

        absf = np.abs(fs)
        for i in range(1, len(xs) - 1):
            if absf[i] <= absf[i - 1] and absf[i] <= absf[i + 1]:
                # Only launch the expensive tangency refinement when the
                # sampled valley is already plausibly close to zero.
                if absf[i] > max(2e-5 * scale, 0.02 * min(absf[i - 1], absf[i + 1])):
                    continue
                lo, hi = float(xs[i - 1]), float(xs[i + 1])
                opt = minimize_scalar(lambda z: abs(fun(float(z))), bounds=(lo, hi), method="bounded",
                                      options={"xatol": 2e-14, "maxiter": 100})
                if opt.fun <= residual_tol * scale:
                    x = float(opt.x)
                    if 0.0 < x < p1:
                        candidates.append((x, "tangent-candidate", fun(x)))

    merged = _deduplicate(candidates, tol=max(2e-8 * p1, 2e-11))
    # Samples only close to, but not at, a root can otherwise survive.  Keep
    # them only at a much stricter residual than the exploratory threshold.
    clean: list[tuple[float, str, float]] = []
    for x, kind, fx in merged:
        if kind in ("sample", "tangent-candidate") and abs(fx) > 5e-11 * scale:
            continue
        clean.append((x, kind, fx))
    if not clean:
        raise RuntimeError("equilibrium search returned an empty set")
    return FastEquilibria(
        tuple(x for x, _, _ in clean),
        tuple(k for _, k, _ in clean),
        tuple(f for _, _, f in clean),
        kink,
    )


def pessimistic_completion_fast(
    p1: float,
    p2: float,
    par: Params,
    *,
    grid_size: int = 161,
) -> tuple[float, FastEquilibria, tuple[float, ...]]:
    eq = find_equilibria_fast(p1, p2, par, grid_size=grid_size)
    vals = tuple(completion(a, p1, p2, par) for a in eq.cutoffs)
    return min(vals), eq, vals


# ---------------------- high precision interval isolator --------------------


Interval = tuple[mp.mpf, mp.mpf]


def _iadd(x: Interval, y: Interval) -> Interval:
    return x[0] + y[0], x[1] + y[1]


def _isub(x: Interval, y: Interval) -> Interval:
    return x[0] - y[1], x[1] - y[0]


def _imul(x: Interval, y: Interval) -> Interval:
    products = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(products), max(products)


def residual_range_mp(
    lo: mp.mpf, hi: mp.mpf, p1: mp.mpf, p2: mp.mpf, par: Params
) -> Interval:
    """A conservative high-precision natural interval enclosure on [lo,hi].

    The bounds exploit monotonicity of phi, exp(-ma), lambda_j and the rider
    masses.  All product factors are enclosed independently, so dependency can
    widen the box.  This is interval-style exclusion with an explicit rounding
    pad, not a machine-checked directed-rounding proof.
    """

    if not (0 <= lo <= hi <= p1):
        raise ValueError("invalid cutoff interval")
    m, alpha, _, _ = (mpf(x) for x in (par.m, par.alpha, par.beta, par.gamma))
    x1: Interval = (p1 - hi, p1 - lo)
    x2: Interval = (p2 - hi, p2 - lo)
    share_a: Interval = (mp_phi(m * hi), mp_phi(m * lo))
    reach: Interval = (mp.exp(-m * hi), mp.exp(-m * lo))

    lam1_lo, lam2_lo = mp_lambdas(lo, p1, p2, par)
    lam1_hi, lam2_hi = mp_lambdas(hi, p1, p2, par)
    share1: Interval = (mp_phi(lam1_lo), mp_phi(lam1_hi))
    share2: Interval = (mp_phi(lam2_lo), mp_phi(lam2_hi))
    rr_lo = mp_rider_response(lo, p1, p2, par)
    rr_hi = mp_rider_response(hi, p1, p2, par)
    eta_e: Interval = (rr_lo.eta_escalate, rr_hi.eta_escalate)
    eta_r: Interval = (rr_hi.eta_repeat, rr_lo.eta_repeat)

    accept = _imul(share_a, x1)
    repeat = _imul(_imul(eta_r, share1), x1)
    escalate = _imul(_imul(eta_e, share2), x2)
    wait_inside = _iadd(repeat, escalate)
    wait = _imul(_imul(reach, (alpha, alpha)), wait_inside)
    raw = _isub(accept, wait)
    pad = 128 * mp.eps * max(mp.mpf(1), abs(raw[0]), abs(raw[1]))
    return raw[0] - pad, raw[1] + pad


@dataclass(frozen=True)
class RootBox:
    lo: mp.mpf
    hi: mp.mpf
    f_lo: mp.mpf
    f_hi: mp.mpf
    kind: Literal["sign-change", "unresolved", "exact"]
    root: mp.mpf

    @property
    def width(self) -> mp.mpf:
        return self.hi - self.lo


@dataclass(frozen=True)
class MPEquilibria:
    p1: mp.mpf
    p2: mp.mpf
    boundary_zero: bool
    boundary_p1: bool
    f_zero: mp.mpf
    f_p1: mp.mpf
    roots: tuple[RootBox, ...]
    excluded_boxes: int
    terminal_boxes: int
    dps: int

    @property
    def unresolved(self) -> tuple[RootBox, ...]:
        return tuple(r for r in self.roots if r.kind == "unresolved")

    @property
    def cutoffs(self) -> tuple[mp.mpf, ...]:
        ans: list[mp.mpf] = []
        if self.boundary_zero:
            ans.append(mp.mpf(0))
        ans.extend(r.root for r in self.roots)
        if self.boundary_p1:
            ans.append(self.p1)
        return tuple(ans)

    @property
    def multiplicity(self) -> int:
        return len(self.cutoffs)


def _bisect_sign_change(
    fun, lo: mp.mpf, hi: mp.mpf, flo: mp.mpf, fhi: mp.mpf, tol: mp.mpf
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    if flo == 0:
        return lo, lo, flo, flo
    if fhi == 0:
        return hi, hi, fhi, fhi
    if flo * fhi >= 0:
        raise ValueError("not a sign-changing bracket")
    while hi - lo > tol:
        mid = (lo + hi) / 2
        fm = fun(mid)
        if fm == 0:
            return mid, mid, fm, fm
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return lo, hi, flo, fhi


def _merge_intervals(boxes: Iterable[Interval], gap: mp.mpf) -> list[Interval]:
    ordered = sorted(boxes, key=lambda z: z[0])
    if not ordered:
        return []
    merged: list[list[mp.mpf]] = [[ordered[0][0], ordered[0][1]]]
    for lo, hi in ordered[1:]:
        if lo <= merged[-1][1] + gap:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return [(x[0], x[1]) for x in merged]


def isolate_equilibria_mp(
    p1_in: float | str | mp.mpf,
    p2_in: float | str | mp.mpf,
    par: Params,
    *,
    dps: int = 80,
    box_tol: str = "1e-24",
    max_depth: int = 180,
    max_boxes: int = 2_000_000,
) -> MPEquilibria:
    """Globally isolate every non-excluded interior root at high precision.

    Ordinary roots receive sign-changing interval certificates.  A box that
    still contains zero in its interval extension but lacks a sign change is
    *retained and labelled unresolved*; it is never silently discarded.  Such
    a box is the numerical signature expected at an even-multiplicity branch
    birth or under severe interval dependency.
    """

    with mp.workdps(dps):
        p1, p2 = mpf(p1_in), mpf(p2_in)
        if not (0 <= p1 <= p2 <= 1):
            raise ValueError("policy must satisfy 0 <= p1 <= p2 <= 1")
        fun = lambda a: mp_cutoff_residual(a, p1, p2, par)
        f0, fp = fun(mp.mpf(0)), fun(p1)
        b0, bp = f0 <= 0, fp >= 0
        if p1 == 0:
            return MPEquilibria(p1, p2, b0, False, f0, fp, (), 0, 0, dps)

        target = mp.mpf(box_tol)
        queue: list[tuple[mp.mpf, mp.mpf, int]] = [(mp.mpf(0), p1, 0)]
        terminal: list[Interval] = []
        excluded = 0
        seen = 0
        while queue:
            lo, hi, depth = queue.pop()
            seen += 1
            if seen > max_boxes:
                raise RuntimeError("interval root isolation exceeded max_boxes")
            fr = residual_range_mp(lo, hi, p1, p2, par)
            if fr[0] > 0 or fr[1] < 0:
                excluded += 1
                continue
            if hi - lo <= target or depth >= max_depth:
                terminal.append((lo, hi))
                continue
            mid = (lo + hi) / 2
            queue.append((mid, hi, depth + 1))
            queue.append((lo, mid, depth + 1))

        merged = _merge_intervals(terminal, 2 * target)
        roots: list[RootBox] = []
        for lo, hi in merged:
            # Remove boxes whose only zero is a separately handled endpoint.
            if b0 and hi <= 4 * target:
                sample = min(p1, hi + 8 * target)
                if sample > 0 and fun(sample) != 0:
                    continue
            if bp and p1 - lo <= 4 * target:
                sample = max(mp.mpf(0), lo - 8 * target)
                if sample < p1 and fun(sample) != 0:
                    continue

            # Search within the retained enclosure for a sign change.  This
            # also separates two roots if interval dependency merged boxes.
            nodes = [lo + (hi - lo) * k / 32 for k in range(33)]
            vals = [fun(x) for x in nodes]
            brackets: list[tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]] = []
            exact_nodes: list[tuple[mp.mpf, mp.mpf]] = []
            for x, fx in zip(nodes, vals):
                if fx == 0 and x not in (mp.mpf(0), p1):
                    exact_nodes.append((x, fx))
            for i in range(32):
                if vals[i] * vals[i + 1] < 0:
                    brackets.append((nodes[i], nodes[i + 1], vals[i], vals[i + 1]))
            if brackets:
                for blo, bhi, bflo, bfhi in brackets:
                    rlo, rhi, rflo, rfhi = _bisect_sign_change(
                        fun, blo, bhi, bflo, bfhi, target / 16
                    )
                    roots.append(RootBox(rlo, rhi, rflo, rfhi, "sign-change", (rlo + rhi) / 2))
            elif exact_nodes:
                for x, fx in exact_nodes:
                    roots.append(RootBox(x, x, fx, fx, "exact", x))
            else:
                flo, fhi = vals[0], vals[-1]
                best_i = min(range(len(vals)), key=lambda k: abs(vals[k]))
                roots.append(RootBox(lo, hi, flo, fhi, "unresolved", nodes[best_i]))

        # De-duplicate high precision boxes produced on adjacent terminal cells.
        roots.sort(key=lambda r: r.root)
        dedup: list[RootBox] = []
        for r in roots:
            if dedup and abs(r.root - dedup[-1].root) <= 8 * target:
                if r.kind == "sign-change" and dedup[-1].kind != "sign-change":
                    dedup[-1] = r
                continue
            if r.root <= 4 * target and b0:
                continue
            if p1 - r.root <= 4 * target and bp:
                continue
            dedup.append(r)
        return MPEquilibria(
            p1, p2, b0, bp, f0, fp, tuple(dedup), excluded, len(terminal), dps
        )


def pessimistic_completion_mp(
    eq: MPEquilibria, par: Params
) -> tuple[mp.mpf, tuple[mp.mpf, ...]]:
    """Evaluate every certified/candidate branch retained by the isolator."""

    with mp.workdps(eq.dps):
        vals = tuple(mp_completion(a, eq.p1, eq.p2, par) for a in eq.cutoffs)
        if not vals:
            raise RuntimeError("empty high-precision equilibrium set")
        return min(vals), vals

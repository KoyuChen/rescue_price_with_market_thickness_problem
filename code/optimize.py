"""Deterministic nested policy optimization with branch diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import math
from typing import Callable

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from equilibria import FastEquilibria, pessimistic_completion_fast
from model import Params, cutoff_residual, flat_completion


@dataclass(frozen=True)
class Settings:
    p1_grid: int = 33
    p2_grid: int = 41
    root_grid: int = 81
    local_refinements: int = 5
    xatol: float = 2e-8
    diagnostics: bool = True


@dataclass(frozen=True)
class PolicyEval:
    p1: float
    p2: float
    value: float
    cutoffs: tuple[float, ...]
    completions: tuple[float, ...]
    kinds: tuple[str, ...]

    @property
    def multiplicity(self) -> int:
        return len(self.cutoffs)


@dataclass(frozen=True)
class BoundaryDiagnostic:
    left: float
    right: float
    estimate: float
    center_value: float
    left_values: tuple[tuple[float, float], ...]
    right_values: tuple[tuple[float, float], ...]
    signature: str


@dataclass(frozen=True)
class ConditionalResult:
    p1: float
    best: PolicyEval
    samples: tuple[PolicyEval, ...]
    branch_boundaries: tuple[BoundaryDiagnostic, ...]


@dataclass(frozen=True)
class GlobalResult:
    best: PolicyEval
    conditional: tuple[ConditionalResult, ...]
    flat_p: float
    flat_value: float
    settings: Settings

    @property
    def escalation_value(self) -> float:
        return self.best.value - self.flat_value


class Evaluator:
    def __init__(self, par: Params, root_grid: int = 81):
        self.par = par
        self.root_grid = root_grid
        self._cache: dict[tuple[float, float], PolicyEval] = {}

    def __call__(self, p1: float, p2: float) -> PolicyEval:
        p1 = float(np.clip(p1, 0.0, 1.0))
        p2 = float(np.clip(p2, p1, 1.0))
        key = (p1, p2)
        if key in self._cache:
            return self._cache[key]
        val, eq, vals = pessimistic_completion_fast(
            p1, p2, self.par, grid_size=self.root_grid
        )
        ans = PolicyEval(p1, p2, val, eq.cutoffs, vals, eq.kinds)
        self._cache[key] = ans
        return ans


def _clustered_grid(lo: float, hi: float, n: int) -> np.ndarray:
    if hi <= lo:
        return np.array([lo])
    k = max(3, int(math.ceil(n / 3)))
    u = np.linspace(0.0, 1.0, k)
    nodes = np.r_[u, u * u, 1.0 - (1.0 - u) ** 2]
    return lo + (hi - lo) * np.unique(nodes)


def optimize_flat(par: Params) -> tuple[float, float]:
    """Grid plus all visible local refinements for the nested flat class."""

    xs = np.unique(np.r_[_clustered_grid(0.0, 1.0, 161), par.beta])
    ys = np.array([flat_completion(float(x), par) for x in xs])
    candidates = [(float(ys[i]), float(xs[i])) for i in range(len(xs))]
    for i in range(1, len(xs) - 1):
        if ys[i] >= ys[i - 1] and ys[i] >= ys[i + 1]:
            opt = minimize_scalar(
                lambda p: -flat_completion(float(p), par),
                bounds=(float(xs[i - 1]), float(xs[i + 1])),
                method="bounded",
                options={"xatol": 2e-14, "maxiter": 300},
            )
            candidates.append((-float(opt.fun), float(opt.x)))
    val, p = max(candidates)
    return p, val


def _diagnose_boundary(
    p1: float, lo: PolicyEval, hi: PolicyEval, evaluator: Evaluator
) -> BoundaryDiagnostic:
    """Locate a branch-count transition and compare one-sided sequences."""

    left, right = lo.p2, hi.p2
    def regime(x: PolicyEval) -> tuple[int, bool, bool]:
        return (
            x.multiplicity,
            any(k == "boundary-0" for k in x.kinds),
            any(k == "boundary-p1" for k in x.kinds),
        )

    state_left, state_right = regime(lo), regime(hi)
    # Bisection by branch count is intentionally deterministic.  If the count
    # oscillates (a numerical red flag), the final interval still records it.
    for _ in range(55):
        mid = (left + right) / 2.0
        state_mid = regime(evaluator(p1, mid))
        if state_mid == state_left:
            left = mid
        else:
            right = mid
        if right - left <= 2e-13 * max(1.0, abs(mid)):
            break
    boundary = (left + right) / 2.0
    center = evaluator(p1, boundary).value
    span = max(hi.p2 - lo.p2, 1e-8)
    lvals: list[tuple[float, float]] = []
    rvals: list[tuple[float, float]] = []
    for k in (2, 3, 4, 5, 6, 7, 8):
        delta = span * 10.0 ** (-k)
        if boundary - delta >= p1:
            lvals.append((delta, evaluator(p1, boundary - delta).value))
        if boundary + delta <= 1.0:
            rvals.append((delta, evaluator(p1, boundary + delta).value))
    limits = [x[1] for x in lvals[-2:] + rvals[-2:]]
    gap = max(limits, default=center) - center
    if gap > 2e-7:
        sig = "possible nonattainment: one-sided value exceeds boundary value"
    elif lvals and rvals and abs(lvals[-1][1] - rvals[-1][1]) > 2e-7:
        sig = "possible jump discontinuity"
    else:
        sig = "branch transition appears continuous at tested scales"
    return BoundaryDiagnostic(left, right, boundary, center, tuple(lvals), tuple(rvals), sig)


def optimize_p2_given_p1(
    p1: float,
    par: Params,
    settings: Settings,
    evaluator: Evaluator | None = None,
) -> ConditionalResult:
    evaluator = evaluator or Evaluator(par, settings.root_grid)
    p1 = float(np.clip(p1, 0.0, 1.0))
    # v_M >= p2/beta, so p2 >= beta is never activated.  One representative
    # of the resulting plateau suffices; the flat endpoint remains included.
    upper = p1 if p1 >= par.beta else par.beta
    grid = _clustered_grid(p1, upper, settings.p2_grid)
    sampled = [evaluator(p1, float(p2)) for p2 in grid]

    candidates: list[PolicyEval] = list(sampled)
    local_idx_all = [
        i
        for i in range(1, len(grid) - 1)
        if sampled[i].value >= sampled[i - 1].value
        and sampled[i].value >= sampled[i + 1].value
    ]
    local_idx = sorted(
        local_idx_all, key=lambda i: sampled[i].value, reverse=True
    )[: settings.local_refinements]
    # Also refine the strongest grid cells in case a narrow peak sits between
    # nodes or the objective is only piecewise smooth.
    local_idx.extend(
        int(i) for i in np.argsort([x.value for x in sampled])[-settings.local_refinements :]
    )
    for i in sorted(set(local_idx)):
        if i <= 0 or i >= len(grid) - 1:
            continue
        lo, hi = float(grid[i - 1]), float(grid[i + 1])
        opt = minimize_scalar(
            lambda q: -evaluator(p1, float(q)).value,
            bounds=(lo, hi),
            method="bounded",
            options={"xatol": settings.xatol, "maxiter": 60},
        )
        candidates.append(evaluator(p1, float(opt.x)))

    diagnostics: list[BoundaryDiagnostic] = []
    for left_eval, right_eval in zip(sampled[:-1], sampled[1:]):
        if not settings.diagnostics:
            continue
        left_regime = (
            left_eval.multiplicity,
            any(k == "boundary-0" for k in left_eval.kinds),
            any(k == "boundary-p1" for k in left_eval.kinds),
        )
        right_regime = (
            right_eval.multiplicity,
            any(k == "boundary-0" for k in right_eval.kinds),
            any(k == "boundary-p1" for k in right_eval.kinds),
        )
        if left_regime != right_regime:
            diagnostics.append(_diagnose_boundary(p1, left_eval, right_eval, evaluator))

    # Explicit one-sided samples around every detected branch transition are
    # eligible for the numerical supremum.
    for d in diagnostics:
        for delta, _ in d.left_values + d.right_values:
            if p1 <= d.estimate - delta <= upper:
                candidates.append(evaluator(p1, d.estimate - delta))
            if p1 <= d.estimate + delta <= upper:
                candidates.append(evaluator(p1, d.estimate + delta))
    best = max(candidates, key=lambda x: (x.value, -x.p2))
    sampled_sorted = tuple(sorted({x.p2: x for x in candidates}.values(), key=lambda x: x.p2))
    return ConditionalResult(p1, best, sampled_sorted, tuple(diagnostics))


def optimize_announced(par: Params, settings: Settings = Settings()) -> GlobalResult:
    """Optimize p2 conditional on p1, then optimize p1."""

    par.validate()
    evaluator = Evaluator(par, settings.root_grid)
    flat_p, flat_val = optimize_flat(par)

    # The beta kink and optimized flat policy are forced into the outer grid.
    grid = np.unique(
        np.r_[ _clustered_grid(0.0, par.beta, settings.p1_grid),
               _clustered_grid(par.beta, 1.0, max(9, settings.p1_grid // 3)),
               par.beta, flat_p ]
    )
    cache: dict[float, ConditionalResult] = {}

    def cond(p: float) -> ConditionalResult:
        p = float(np.clip(p, 0.0, 1.0))
        if p not in cache:
            cache[p] = optimize_p2_given_p1(p, par, settings, evaluator)
        return cache[p]

    initial = [cond(float(p)) for p in grid]
    vals = np.array([x.best.value for x in initial])
    idx_all = [
        i for i in range(1, len(grid) - 1)
        if vals[i] >= vals[i - 1] and vals[i] >= vals[i + 1]
    ]
    idx = sorted(idx_all, key=lambda i: vals[i], reverse=True)[: settings.local_refinements]
    idx.extend(int(i) for i in np.argsort(vals)[-settings.local_refinements :])
    for i in sorted(set(idx)):
        if i <= 0 or i >= len(grid) - 1:
            continue
        lo, hi = float(grid[i - 1]), float(grid[i + 1])
        opt = minimize_scalar(
            lambda p: -cond(float(p)).best.value,
            bounds=(lo, hi), method="bounded",
            options={"xatol": settings.xatol, "maxiter": 40},
        )
        cond(float(opt.x))

    all_cond = tuple(sorted(cache.values(), key=lambda x: x.p1))
    best = max((x.best for x in all_cond), key=lambda x: (x.value, -x.p1, -x.p2))
    return GlobalResult(best, all_cond, flat_p, flat_val, settings)

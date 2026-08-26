#!/usr/bin/env python3
"""Global one-dimensional thickness falsifier for the no-entry reduction.

This program uses the cutoff parametrization described in
``thickness_topology.md``.  It does not assume that the objective is unimodal
in the cutoff: a hybrid grid is used to bracket every visible local maximum,
and every bracket is refined.  The calculation is a falsification device, not
an interval-arithmetic proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq, minimize_scalar


def _inverse_h(t: np.ndarray) -> np.ndarray:
    """Solve z + log(1+z) = t, elementwise, by safeguarded Newton steps."""
    t = np.asarray(t, dtype=float)
    z = np.where(t < 1.0, 0.5 * t, np.maximum(t - np.log1p(t), 0.0))
    for _ in range(16):
        step = (z + np.log1p(z) - t) / (1.0 + 1.0 / (1.0 + z))
        z = np.maximum(z - step, 0.0)
    return z


def cutoff_objective(
    m: float, alpha: float, beta: float, a: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return J_m(a), P_m(a), Q_m(a) on an array of cutoff parameters."""
    a = np.asarray(a, dtype=float)
    k = alpha * m
    z = _inverse_h(k * (beta - a))
    y = z / k
    q = a + np.log1p(z) / k

    x = m * a
    ratio = np.empty_like(a)
    small = x < 1.0e-5
    ratio[small] = (1.0 / m) * (
        1.0 - x[small] / 2.0 + x[small] ** 2 / 12.0
    )
    middle = (~small) & (x < 700.0)
    ratio[middle] = a[middle] / np.expm1(x[middle])
    ratio[(~small) & (~middle)] = 0.0

    t_envelope = k * y**2 / (beta * (1.0 + z))
    b = ratio * t_envelope
    discriminant = np.maximum((1.0 - a) ** 2 - 4.0 * b, 0.0)
    # Stable lower root of p^2-(1+a)p+(a+B)=0.
    p = 2.0 * (a + b) / (1.0 + a + np.sqrt(discriminant))

    phi = np.empty_like(a)
    phi[small] = (
        1.0 - x[small] / 2.0 + x[small] ** 2 / 6.0 - x[small] ** 3 / 24.0
    )
    phi[~small] = -np.expm1(-x[~small]) / x[~small]
    value = m * (1.0 - p) * p * phi
    return value, p, q


@dataclass(frozen=True)
class DynamicSolution:
    value: float
    a: float
    p: float
    q: float
    visible_local_maxima: int


def dynamic_value(
    m: float, alpha: float, beta: float, grid_size: int = 1200
) -> DynamicSolution:
    """Enumerate visible cutoff peaks and refine each one."""
    linear = np.linspace(0.0, beta, grid_size)
    xmax = m * beta
    if xmax > 0.0:
        xgrid = np.geomspace(1.0e-12, max(xmax, 1.0e-12), grid_size) / m
        grid = np.unique(np.concatenate((linear, xgrid[xgrid <= beta])))
    else:
        grid = linear

    values, _, _ = cutoff_objective(m, alpha, beta, grid)
    peaks = list(
        np.where((values[1:-1] >= values[:-2]) & (values[1:-1] >= values[2:]))[
            0
        ]
        + 1
    )
    # Include endpoints and several top grid points to guard against a coarse
    # grid missing a narrow peak.
    top_count = min(8, len(grid))
    candidates = set(peaks)
    candidates.update(np.argpartition(values, -top_count)[-top_count:])
    candidates.update((0, len(grid) - 1))

    best_value = -np.inf
    best_a = 0.0

    def negative_value(a_scalar: float) -> float:
        return -float(cutoff_objective(m, alpha, beta, np.array([a_scalar]))[0][0])

    for index in candidates:
        lo = grid[max(0, index - 2)]
        hi = grid[min(len(grid) - 1, index + 2)]
        if hi > lo:
            result = minimize_scalar(
                negative_value,
                bounds=(lo, hi),
                method="bounded",
                options={"xatol": 2.0e-14},
            )
            trial_value, trial_a = -result.fun, result.x
        else:
            trial_a = lo
            trial_value = -negative_value(lo)
        if trial_value > best_value:
            best_value, best_a = trial_value, trial_a

    best, p, q = cutoff_objective(m, alpha, beta, np.array([best_a]))
    return DynamicSolution(
        value=float(best[0]),
        a=float(best_a),
        p=float(p[0]),
        q=float(q[0]),
        visible_local_maxima=len(peaks),
    )


def flat_value(m: float) -> tuple[float, float]:
    """Return the exact optimized-flat value and payment."""
    x = brentq(lambda u: u - np.log1p(m - u), 0.0, np.log1p(m), xtol=1e-14)
    p = x / m
    value = (1.0 - p) * (-np.expm1(-x))
    return value, p


def scan(alpha: float, beta: float, count: int, m_min: float, m_max: float) -> None:
    ms = np.geomspace(m_min, m_max, count)
    gains = np.empty_like(ms)
    solutions: list[DynamicSolution] = []
    for i, m in enumerate(ms):
        solution = dynamic_value(m, alpha, beta)
        flat, _ = flat_value(m)
        gains[i] = solution.value - flat
        solutions.append(solution)

    peak_index = int(np.argmax(gains))
    # A down-up certificate candidate must exceed both an absolute and a
    # relative threshold.  Any candidate still requires high-precision or
    # interval validation outside this script.
    tolerance = max(1.0e-11, 1.0e-7 * float(np.max(gains)))
    candidates = []
    prefix_max = np.maximum.accumulate(gains)
    suffix_max = np.maximum.accumulate(gains[::-1])[::-1]
    for i in range(1, len(ms) - 1):
        drop = prefix_max[i - 1] - gains[i]
        rebound = suffix_max[i + 1] - gains[i]
        if drop > tolerance and rebound > tolerance:
            candidates.append((i, drop, rebound))

    peak = solutions[peak_index]
    print(f"alpha={alpha:.12g}, beta={beta:.12g}")
    print(
        "grid peak: "
        f"m={ms[peak_index]:.12g}, V={gains[peak_index]:.12g}, "
        f"a={peak.a:.12g}, p={peak.p:.12g}, q={peak.q:.12g}"
    )
    print(
        f"endpoint grid values: V({ms[0]:.3g})={gains[0]:.12g}, "
        f"V({ms[-1]:.3g})={gains[-1]:.12g}"
    )
    print(f"robust down-up candidates: {len(candidates)}")
    for i, drop, rebound in candidates[:10]:
        print(
            f"  m={ms[i]:.12g}, V={gains[i]:.12g}, "
            f"drop={drop:.4g}, rebound={rebound:.4g}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=0.9)
    parser.add_argument("--count", type=int, default=241)
    parser.add_argument("--m-min", type=float, default=1.0e-5)
    parser.add_argument("--m-max", type=float, default=1.0e8)
    args = parser.parse_args()
    if not (0.0 < args.alpha <= 1.0):
        raise ValueError("alpha must lie in (0,1]")
    if not (0.5 < args.beta < 1.0):
        raise ValueError("this audit targets beta in (1/2,1)")
    scan(args.alpha, args.beta, args.count, args.m_min, args.m_max)


if __name__ == "__main__":
    main()

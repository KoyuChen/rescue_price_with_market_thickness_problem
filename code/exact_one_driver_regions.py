"""Reproduce the exact-one-driver menus and type-region widths in the note.

For each (beta, delta), the program enumerates every interior zero of the
unsquared cutoff first-order condition, adds the cutoff boundaries, recovers
(p1, p2) from the WPBE envelope, and compares completion with the best flat
menu.  It therefore does not impose a cutoff or reuse prices across
calibrations.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq


TOL = 1.0e-9
CALIBRATIONS = ((0.6, 0.5), (0.6, 0.8), (0.8, 0.5),
                (0.8, 0.8), (0.9, 0.5), (0.9, 0.8))


@dataclass(frozen=True)
class ActiveMenu:
    beta: float
    delta: float
    cutoff: float
    p1: float
    p2: float
    completion: float
    rider_widths: tuple[float, float, float, float]
    driver_widths: tuple[float, float, float, float]


def discriminant(cutoff: float, beta: float, delta: float) -> float:
    """Discriminant in equation (5)."""
    return (1.0 - cutoff) ** 2 - (delta / beta) * (beta - cutoff) ** 2


def prices(cutoff: float, beta: float, delta: float) -> tuple[float, float]:
    """Recover the sign-screened WPBE prices in equation (5)."""
    disc = discriminant(cutoff, beta, delta)
    if disc < -TOL:
        raise ValueError("negative price discriminant")
    p1 = (1.0 + cutoff - np.sqrt(max(0.0, disc))) / 2.0
    p2 = (beta + cutoff) / 2.0
    return float(p1), float(p2)


def objective(cutoff: float, beta: float, delta: float) -> float:
    """Envelope completion J_delta(cutoff) in equation (6)."""
    disc = discriminant(cutoff, beta, delta)
    if disc < -TOL:
        return float("-inf")
    return float(
        cutoff * (1.0 - cutoff + np.sqrt(max(0.0, disc))) / 2.0
        + (beta - cutoff) ** 2 / (4.0 * beta)
    )


def cutoff_foc(cutoff: float, beta: float, delta: float) -> float:
    """Left side minus right side of the unsquared equation (7)."""
    disc = discriminant(cutoff, beta, delta)
    if disc < 0.0:
        return float("nan")
    left = (
        1.0
        - delta * beta
        + 3.0 * (delta - 1.0) * cutoff
        + 2.0 * (1.0 - delta / beta) * cutoff**2
    )
    right = ((2.0 * beta - 1.0) / beta) * cutoff * np.sqrt(disc)
    return float(left - right)


def all_stationary_cutoffs(beta: float, delta: float) -> list[float]:
    """Bracket and enumerate all roots of (7) on the feasible interval."""
    grid = np.linspace(0.0, beta, 20_001)
    values = np.array([cutoff_foc(x, beta, delta) for x in grid])
    roots: list[float] = []
    for left, right, f_left, f_right in zip(
        grid[:-1], grid[1:], values[:-1], values[1:], strict=True
    ):
        if not np.isfinite(f_left) or not np.isfinite(f_right):
            continue
        if abs(f_left) <= TOL:
            roots.append(float(left))
        if f_left * f_right < 0.0:
            roots.append(float(brentq(cutoff_foc, left, right,
                                      args=(beta, delta))))
    if abs(values[-1]) <= TOL:
        roots.append(float(beta))
    return sorted({round(root, 12) for root in roots})


def solve_active_menu(beta: float, delta: float) -> ActiveMenu:
    """Select the global active-menu candidate and verify its type regions."""
    candidates = [0.0, beta, *all_stationary_cutoffs(beta, delta)]
    cutoff = max(candidates, key=lambda x: objective(x, beta, delta))
    p1, p2 = prices(cutoff, beta, delta)
    completion = objective(cutoff, beta, delta)

    rider = (
        p1,
        p1 / beta - p1,
        (p2 - cutoff) / beta,
        (beta - p1 - p2 + cutoff) / beta,
    )
    driver = (cutoff, p1 - cutoff, p2 - p1, 1.0 - p2)

    assert completion >= 0.25 - TOL, "flat menu dominates this candidate"
    assert cutoff <= p1 + TOL <= p2 + TOL <= 1.0 + TOL
    assert min(rider) >= -TOL and abs(sum(rider) - 1.0) <= TOL
    assert min(driver) >= -TOL and abs(sum(driver) - 1.0) <= TOL

    return ActiveMenu(beta, delta, cutoff, p1, p2, completion, rider, driver)


def main() -> None:
    header = "beta delta cutoff       p1       p2       M1 | rider widths | driver widths"
    print(header)
    for beta, delta in CALIBRATIONS:
        menu = solve_active_menu(beta, delta)
        rider = " ".join(f"{x:.6f}" for x in menu.rider_widths)
        driver = " ".join(f"{x:.6f}" for x in menu.driver_widths)
        print(
            f"{beta:4.1f} {delta:5.1f} {menu.cutoff:7.6f} "
            f"{menu.p1:8.6f} {menu.p2:8.6f} {menu.completion:8.6f} | "
            f"{rider} | {driver}"
        )


if __name__ == "__main__":
    main()

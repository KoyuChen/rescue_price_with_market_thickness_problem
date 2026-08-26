"""Reproduce optimal menus and type regions at m = 1, 5, 10, and 20.

Calibration: alpha = 1, beta = delta = 0.8, gamma = 0, and uniform rider and
driver types.  For every m, the code solves the rescue-price envelope, the
driver cutoff indifference, and every visible root of the outer cutoff first-
order condition.  Boundaries are included in the global comparison.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, sqrt

import numpy as np
from scipy.optimize import brentq


ALPHA = 1.0
BETA = 0.8
DELTA = 0.8
THICKNESSES = (1.0, 5.0, 10.0, 20.0)
TOL = 1.0e-9


@dataclass(frozen=True)
class ThicknessMenu:
    m: float
    cutoff: float
    p1: float
    p2: float
    completion: float
    c1: float
    c2: float
    switch_value: float
    rider_widths: tuple[float, float, float, float]
    driver_widths: tuple[float, float, float, float]


def rescue_price(m: float, cutoff: float) -> float:
    """Solve equation (12) on [cutoff, beta]."""
    k = ALPHA * m
    return float(
        brentq(
            lambda p2: expm1(k * (p2 - cutoff)) - k * (BETA - p2),
            cutoff,
            BETA,
            xtol=1.0e-14,
        )
    )


def evaluate(m: float, cutoff: float) -> tuple[float, float, float, float, float, float]:
    """Return J, p1, p2, S, h, and R at a candidate cutoff."""
    p2 = rescue_price(m, cutoff)
    k = ALPHA * m
    c2 = -expm1(-k * (p2 - cutoff))
    supply_term = (BETA - p2) * c2
    h = m if cutoff == 0.0 else expm1(m * cutoff) / cutoff
    rhs = DELTA * supply_term / (BETA * h)
    disc = (1.0 - cutoff) ** 2 - 4.0 * rhs
    if disc < -TOL:
        raise ValueError("negative p1 discriminant")
    p1 = (1.0 + cutoff - sqrt(max(0.0, disc))) / 2.0
    completion = (
        (1.0 - p1) * (-expm1(-m * cutoff))
        + exp(-m * cutoff) * supply_term / BETA
    )
    return completion, p1, p2, supply_term, h, rhs


def cutoff_derivative(m: float, cutoff: float) -> float:
    """Evaluate the analytical outer derivative in equation (20)."""
    completion, p1, p2, supply_term, h, rhs = evaluate(m, cutoff)
    del completion, h
    supply_prime = -supply_term / (BETA - p2)
    h_log_prime = m / (-expm1(-m * cutoff)) - 1.0 / cutoff
    rhs_prime = rhs * (-1.0 / (BETA - p2) - h_log_prime)
    p1_prime = (1.0 - p1 + rhs_prime) / (1.0 + cutoff - 2.0 * p1)
    failure = exp(-m * cutoff)
    return float(
        -(1.0 - failure) * p1_prime
        + m * failure * (1.0 - p1)
        + failure * (supply_prime - m * supply_term) / BETA
    )


def stationary_cutoffs(m: float) -> list[float]:
    """Bracket and enumerate all sign-changing roots of equation (20)."""
    grid = np.linspace(1.0e-9, BETA - 1.0e-9, 20_001)
    values = np.array([cutoff_derivative(m, x) for x in grid])
    roots: list[float] = []
    for left, right, f_left, f_right in zip(
        grid[:-1], grid[1:], values[:-1], values[1:], strict=True
    ):
        if abs(f_left) <= TOL:
            roots.append(float(left))
        if f_left * f_right < 0.0:
            roots.append(
                float(
                    brentq(
                        lambda cutoff: cutoff_derivative(m, cutoff),
                        left,
                        right,
                        xtol=1.0e-14,
                    )
                )
            )
    return sorted({round(root, 12) for root in roots})


def solve(m: float) -> ThicknessMenu:
    """Globally compare all stationary and boundary cutoff candidates."""
    candidates = [0.0, BETA, *stationary_cutoffs(m)]
    cutoff = max(candidates, key=lambda x: evaluate(m, x)[0])
    completion, p1, p2, _, _, _ = evaluate(m, cutoff)

    c1 = 1.0 - exp(-ALPHA * m * (p1 - cutoff))
    c2 = 1.0 - exp(-ALPHA * m * (p2 - cutoff))
    switch_value = (p2 * c2 - p1 * c1) / (BETA * (c2 - c1))
    rider = (
        p1,
        p1 / BETA - p1,
        switch_value - p1 / BETA,
        1.0 - switch_value,
    )
    driver = (cutoff, p1 - cutoff, p2 - p1, 1.0 - p2)

    assert cutoff <= p1 + TOL <= p2 + TOL <= BETA + TOL
    assert 0.0 < c1 < c2 < 1.0
    assert min(rider) >= -TOL and abs(sum(rider) - 1.0) <= TOL
    assert min(driver) >= -TOL and abs(sum(driver) - 1.0) <= TOL

    return ThicknessMenu(
        m, cutoff, p1, p2, completion, c1, c2, switch_value, rider, driver
    )


def main() -> None:
    print("m cutoff       p1       p2       MR | C1 C2 vM | rider widths | driver widths")
    for m in THICKNESSES:
        menu = solve(m)
        rider = " ".join(f"{x:.6f}" for x in menu.rider_widths)
        driver = " ".join(f"{x:.6f}" for x in menu.driver_widths)
        print(
            f"{m:2.0f} {menu.cutoff:.6f} {menu.p1:.6f} {menu.p2:.6f} "
            f"{menu.completion:.6f} | {menu.c1:.6f} {menu.c2:.6f} "
            f"{menu.switch_value:.6f} | {rider} | {driver}"
        )


if __name__ == "__main__":
    main()

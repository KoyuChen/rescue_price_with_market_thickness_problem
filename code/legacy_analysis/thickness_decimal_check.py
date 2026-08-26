#!/usr/bin/env python3
"""Independent Decimal refinement of a bracketed thickness peak.

The default brackets validate the apparent peak for alpha=1, beta=.9.  This
is a high-precision local refinement; globality comes only from the separate
all-bracket scan in ``thickness_search.py`` and is still not a proof.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext


def inverse_h(t: Decimal, tolerance: Decimal) -> Decimal:
    one = Decimal(1)
    z = t / 2 if t < one else max(t - (one + t).ln(), Decimal(0))
    for _ in range(80):
        step = (z + (one + z).ln() - t) / (one + one / (one + z))
        z -= step
        if abs(step) < tolerance:
            break
    return z


def menu_value(
    m: Decimal, a: Decimal, alpha: Decimal, beta: Decimal, tolerance: Decimal
) -> tuple[Decimal, Decimal, Decimal]:
    one = Decimal(1)
    k = alpha * m
    z = inverse_h(k * (beta - a), tolerance)
    y = z / k
    ratio = a / ((m * a).exp() - one) if a else one / m
    b = ratio * k * y * y / (beta * (one + z))
    p = (one + a - ((one - a) ** 2 - 4 * b).sqrt()) / 2
    x = m * a
    phi = (one - (-x).exp()) / x if x else one
    q = a + (one + z).ln() / k
    return m * (one - p) * p * phi, p, q


def flat_value(m: Decimal, tolerance: Decimal) -> Decimal:
    one = Decimal(1)
    x = (one + m).ln()
    for _ in range(80):
        step = (x - (one + m - x).ln()) / (one + one / (one + m - x))
        x -= step
        if abs(step) < tolerance:
            break
    p = x / m
    return (one - p) * (one - (-x).exp())


def golden_max(function, lo: Decimal, hi: Decimal, iterations: int):
    one = Decimal(1)
    ratio = (Decimal(5).sqrt() - one) / 2
    c = hi - ratio * (hi - lo)
    d = lo + ratio * (hi - lo)
    fc, fd = function(c), function(d)
    for _ in range(iterations):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - ratio * (hi - lo)
            fc = function(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + ratio * (hi - lo)
            fd = function(d)
    x = (lo + hi) / 2
    return x, function(x)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", default="1")
    parser.add_argument("--beta", default=".9")
    parser.add_argument("--m-lo", default="5")
    parser.add_argument("--m-hi", default="20")
    parser.add_argument("--a-lo", default=".03")
    parser.add_argument("--a-hi", default=".3")
    parser.add_argument("--precision", type=int, default=60)
    parser.add_argument("--iterations", type=int, default=110)
    args = parser.parse_args()

    getcontext().prec = args.precision
    alpha, beta = Decimal(args.alpha), Decimal(args.beta)
    a_lo, a_hi = Decimal(args.a_lo), Decimal(args.a_hi)
    tolerance = Decimal(10) ** (-(args.precision - 8))

    def optimized_dynamic(m: Decimal):
        return golden_max(
            lambda a: menu_value(m, a, alpha, beta, tolerance)[0],
            a_lo,
            a_hi,
            args.iterations,
        )

    m_star, gain = golden_max(
        lambda m: optimized_dynamic(m)[1] - flat_value(m, tolerance),
        Decimal(args.m_lo),
        Decimal(args.m_hi),
        args.iterations,
    )
    a_star, dynamic = optimized_dynamic(m_star)
    _, p_star, q_star = menu_value(m_star, a_star, alpha, beta, tolerance)
    flat = flat_value(m_star, tolerance)

    for label, value in (
        ("m", m_star),
        ("V", dynamic - flat),
        ("D", dynamic),
        ("F", flat),
        ("a", a_star),
        ("p1", p_star),
        ("p2", q_star),
    ):
        print(f"{label} {value}")


if __name__ == "__main__":
    main()

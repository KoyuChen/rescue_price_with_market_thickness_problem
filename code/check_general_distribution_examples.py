"""High-precision certificates for the paper's distributional examples."""

from __future__ import annotations

import mpmath as mp


mp.mp.dps = 60


def phi(x: mp.mpf) -> mp.mpf:
    return -mp.expm1(-x) / x if x else mp.mpf(1)


def extended_cdf(x: mp.mpf, power: int = 1) -> mp.mpf:
    if x <= 0:
        return mp.mpf(0)
    if x >= 1:
        return mp.mpf(1)
    return x**power


def evaluate(a: mp.mpf, cost_cdf, rider_cdf, **parameters) -> tuple[mp.mpf, mp.mpf]:
    m = parameters["m"]
    alpha = parameters["alpha"]
    beta = parameters["beta"]
    delta = parameters["delta"]
    gamma = parameters["gamma"]
    p1 = parameters["p1"]
    p2 = parameters["p2"]
    lambda1 = m * (alpha * (cost_cdf(p1) - cost_cdf(a)) + gamma * cost_cdf(p1))
    lambda2 = m * (alpha * (cost_cdf(p2) - cost_cdf(a)) + gamma * cost_cdf(p2))
    coverage1 = -mp.expm1(-lambda1)
    coverage2 = -mp.expm1(-lambda2)
    switch = (coverage2 * p2 - coverage1 * p1) / (
        beta * (coverage2 - coverage1)
    )
    repeat_mass = (rider_cdf(switch) - rider_cdf(p1 / beta)) / (1 - rider_cdf(p1))
    rescue_mass = (1 - rider_cdf(switch)) / (1 - rider_cdf(p1))
    failure = mp.exp(-m * cost_cdf(a))
    residual = phi(m * cost_cdf(a)) * (p1 - a) - delta * alpha * failure * (
        repeat_mass * phi(lambda1) * (p1 - a)
        + rescue_mass * phi(lambda2) * (p2 - a)
    )
    completion = (1 - rider_cdf(p1)) * (
        1 - failure + failure * (repeat_mass * coverage1 + rescue_mass * coverage2)
    )
    return residual, completion


def ramp(c: mp.mpf, left: str, right: str) -> mp.mpf:
    lo, hi = mp.mpf(left), mp.mpf(right)
    if c <= lo:
        return mp.mpf(0)
    if c >= hi:
        return mp.mpf(1)
    return (c - lo) / (hi - lo)


def certify_concave_example() -> None:
    cost_cdf = mp.sqrt
    rider_cdf = lambda value: extended_cdf(value)
    parameters = dict(
        m=mp.mpf("0.5"), alpha=mp.mpf("0.75"), beta=mp.mpf("0.3"),
        delta=mp.mpf(1), gamma=mp.mpf(0), p1=mp.mpf("0.06"), p2=mp.mpf("0.17")
    )
    left, right = mp.mpf("0.0203133"), mp.mpf("0.0203134")
    f_left, _ = evaluate(left, cost_cdf, rider_cdf, **parameters)
    f_right, _ = evaluate(right, cost_cdf, rider_cdf, **parameters)
    assert f_left > 0 > f_right
    root = mp.findroot(
        lambda value: evaluate(value, cost_cdf, rider_cdf, **parameters)[0],
        (left, right),
    )
    _, dynamic = evaluate(root, cost_cdf, rider_cdf, **parameters)
    flat = (1 - parameters["p1"]) * (
        1 - mp.exp(-parameters["m"] * cost_cdf(parameters["p1"]))
    )
    assert left < root < right
    assert flat - dynamic > mp.mpf("0.0048")


def certify_multiple_cutoffs() -> None:
    def cost_cdf(c: mp.mpf) -> mp.mpf:
        return (
            mp.mpf("0.2") * c
            + mp.mpf("0.4") * ramp(c, "0.04", "0.045")
            + mp.mpf("0.4") * ramp(c, "0.15", "0.155")
        )

    rider_cdf = lambda value: extended_cdf(value, 20)
    parameters = dict(
        m=mp.mpf(2), alpha=mp.mpf("0.7"), beta=mp.mpf("0.9"),
        delta=mp.mpf(1), gamma=mp.mpf(0), p1=mp.mpf("0.1"), p2=mp.mpf("0.2")
    )
    brackets = [
        (mp.mpf("0.03035"), mp.mpf("0.03037")),
        (mp.mpf("0.04343"), mp.mpf("0.04345")),
        (mp.mpf("0.04859"), mp.mpf("0.04862")),
    ]
    roots = []
    completions = []
    for left, right in brackets:
        f_left, _ = evaluate(left, cost_cdf, rider_cdf, **parameters)
        f_right, _ = evaluate(right, cost_cdf, rider_cdf, **parameters)
        assert f_left * f_right < 0
        root = mp.findroot(
            lambda value: evaluate(value, cost_cdf, rider_cdf, **parameters)[0],
            (left, right),
        )
        assert left < root < right
        roots.append(root)
        completions.append(evaluate(root, cost_cdf, rider_cdf, **parameters)[1])
    assert roots[0] < roots[1] < roots[2]
    assert max(completions) - min(completions) > mp.mpf("0.066")


if __name__ == "__main__":
    certify_concave_example()
    certify_multiple_cutoffs()
    print("general-distribution counterexample certificates passed")

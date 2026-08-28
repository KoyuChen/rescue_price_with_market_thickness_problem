"""Cutoff-WPBE engine with assignment-contingent spatial pickup costs.

This is the maintained numerical model for three successive notification
regimes:

    incumbent_only: recall first-window rejectors only;
    core_arrivals:  also notify a fresh core Poisson cohort of mean m;
    expanded_search: additionally notify an outer annulus of mean (s-1)m.

The first two regimes optimize ``(p1,p2)`` at fixed reach.  The third optimizes
``(p1,p2,s)``, where ``s`` is the catchment-area multiplier and ``s=1``
exactly collapses expanded search to the core-arrival regime.

Fresh drivers pay no sunk activation or relocation cost.  A driver at area
rank u (normalized radius sqrt(u)) pays the extra pickup cost

    pickup_rate * (sqrt(u) - 1)_+

only when selected for the order.  Consequently the lottery probability
scales both revenue and pickup cost and does not affect the sign of a fresh
driver's response.  Poisson thinning therefore gives fresh accepted intensity

    m * integral_0^s F(p - pickup_cost(u)) du.

Every candidate mechanism is nevertheless evaluated at a full cutoff-WPBE:
incumbents strategically accept or wait, riders choose abandon/repeat/rescue
after universal rejection, and on-path beliefs are induced by the same cutoff.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np
from scipy.optimize import brentq


Selection = Literal["conservative", "optimistic", "stable"]
SupplyRegime = Literal["incumbent_only", "core_arrivals", "expanded_search"]
RootMethod = Literal["unique", "enumerate"]


@dataclass(frozen=True)
class Params:
    """Economic primitives.

    Rider values and drivers' base order costs are Uniform[0,1].  ``m`` is
    both the first-window incumbent intensity and the fresh-arrival intensity
    in a unit-area second-window catchment.  ``pickup_rate`` is the extra
    driver-paid pickup cost per normalized radial unit beyond the core.
    ``incumbent_retention`` is the probability that a first-window rejector
    both remains physically available and remains eligible for the focal
    order's terminal lottery.  It is independent of cost in this benchmark.
    """

    m: float
    beta: float
    delta: float
    pickup_rate: float = 0.25
    incumbent_retention: float = 1.0

    def __post_init__(self) -> None:
        if self.m <= 0:
            raise ValueError("m must be strictly positive")
        if not (0 < self.beta <= 1):
            raise ValueError("beta must lie in (0,1]")
        if not (0 < self.delta <= 1):
            raise ValueError("delta must lie in (0,1]")
        if self.pickup_rate < 0:
            raise ValueError("pickup_rate must be nonnegative")
        if not (0 <= self.incumbent_retention <= 1):
            raise ValueError("incumbent_retention must lie in [0,1]")


@dataclass(frozen=True)
class Policy:
    """Committed anonymous transaction prices and notification regime.

    The rider pays ``p_j`` and the assigned driver receives the same ``p_j``;
    a profit extension would separate fare from wage.
    """

    p1: float
    p2: float
    s: float = 1.0
    regime: SupplyRegime = "core_arrivals"

    def __post_init__(self) -> None:
        if not (0 <= self.p1 <= self.p2 <= 1):
            raise ValueError("policy must satisfy 0 <= p1 <= p2 <= 1")
        if self.s < 1:
            raise ValueError("search multiplier s must be at least one")
        if self.regime not in {
            "incumbent_only",
            "core_arrivals",
            "expanded_search",
        }:
            raise ValueError(f"unknown supply regime: {self.regime}")
        if self.regime != "expanded_search" and abs(self.s - 1.0) > 1e-12:
            raise ValueError("only expanded_search may use s greater than one")


@dataclass(frozen=True)
class TerminalMarket:
    payment: float
    search_multiplier: float
    potential_fresh_intensity: float
    incumbent_intensity: float
    core_fresh_accept_intensity: float
    outer_fresh_accept_intensity: float
    fresh_accept_intensity: float
    total_intensity: float
    assignment_probability: float
    coverage: float
    fresh_pickup_cost_intensity: float


@dataclass(frozen=True)
class EquilibriumOutcome:
    policy: Policy
    params: Params
    cutoff: float
    stable: bool
    residual: float
    repeat_mass: float
    rescue_mass: float
    abandon_mass: float
    repeat: TerminalMarket
    rescue: TerminalMarket
    posted_probability: float
    first_completion: float
    repeat_completion: float
    rescue_completion: float
    repeat_incumbent_completion: float
    repeat_fresh_completion: float
    rescue_incumbent_completion: float
    rescue_fresh_completion: float
    completion: float
    expected_transfer: float
    expected_fresh_acceptors: float
    expected_pickup_cost: float
    expected_notifications: float
    expected_extra_notifications: float
    expected_committed_outer_capacity: float


@dataclass(frozen=True)
class PolicySolution:
    policy: Policy
    params: Params
    equilibria: tuple[EquilibriumOutcome, ...]
    selected: EquilibriumOutcome
    selection: Selection

    @property
    def equilibrium_count(self) -> int:
        return len(self.equilibria)

    @property
    def completion_spread(self) -> float:
        values = [eq.completion for eq in self.equilibria]
        return max(values) - min(values)


@dataclass(frozen=True)
class CertificationResult:
    """A policy solution whose cutoff roots are stable under grid doubling."""

    solution: PolicySolution
    grids: tuple[int, ...]
    root_sets: tuple[tuple[float, ...], ...]
    stable: bool


def uniform_cdf(x: float | np.ndarray) -> float | np.ndarray:
    """CDF of Uniform[0,1], with scalar-preserving output."""

    result = np.clip(np.asarray(x, dtype=float), 0.0, 1.0)
    if np.isscalar(x):
        return float(result)
    return result


def assignment_probability(z: float | np.ndarray) -> float | np.ndarray:
    """E[1/(1+Pois(z))] = (1-exp(-z))/z, evaluated stably."""

    arr = np.asarray(z, dtype=float)
    result = np.empty_like(arr)
    small = np.abs(arr) < 1e-7
    result[small] = 1 - arr[small] / 2 + arr[small] ** 2 / 6
    result[~small] = -np.expm1(-arr[~small]) / arr[~small]
    if np.isscalar(z):
        return float(result)
    return result


def extra_pickup_cost(area_rank: float | np.ndarray, pickup_rate: float):
    """Winner-only pickup cost outside the normalized core catchment."""

    rank = np.asarray(area_rank, dtype=float)
    result = pickup_rate * np.maximum(np.sqrt(np.maximum(rank, 0.0)) - 1.0, 0.0)
    if np.isscalar(area_rank):
        return float(result)
    return result


def fresh_accept_intensity(payment: float, reach: float, params: Params) -> float:
    """Accepted fresh-driver intensity under spatial Poisson thinning.

    For Uniform[0,1] base cost and the piecewise-linear radial pickup cost the
    integral has a closed form.  The formula also covers a fractional core
    reach, although maintained mechanisms use ``reach >= 1``.
    """

    if payment <= 0 or reach <= 0:
        return 0.0

    core = min(reach, 1.0)
    accepted = params.m * core * float(uniform_cdf(payment))
    if reach <= 1 or params.pickup_rate == 0:
        if reach > 1 and params.pickup_rate == 0:
            accepted = params.m * reach * float(uniform_cdf(payment))
        return float(accepted)

    tau = params.pickup_rate
    radius_cap = min(np.sqrt(reach), 1.0 + payment / tau)
    if radius_cap <= 1:
        return float(accepted)

    # 2m int_1^R r [payment - tau(r-1)] dr.
    outer = params.m * (
        (payment + tau) * (radius_cap**2 - 1.0)
        - (2.0 * tau / 3.0) * (radius_cap**3 - 1.0)
    )
    return float(accepted + max(outer, 0.0))


def fresh_pickup_cost_intensity(
    payment: float, reach: float, params: Params
) -> float:
    """Pickup-cost-weighted intensity of fresh volunteers.

    Multiplying this value by a terminal volunteer's assignment probability
    gives expected pickup cost paid by the selected fresh driver.
    """

    if payment <= 0 or reach <= 1 or params.pickup_rate <= 0:
        return 0.0

    tau = params.pickup_rate
    radius_cap = min(np.sqrt(reach), 1.0 + payment / tau)
    if radius_cap <= 1:
        return 0.0

    # 2m int_1^R r * tau(r-1) * [payment-tau(r-1)] dr.
    # Antiderivative expanded symbolically for fast repeated evaluation.
    def primitive(radius: float) -> float:
        return 2.0 * params.m * tau * (
            -tau * radius**4 / 4.0
            + (payment + 2.0 * tau) * radius**3 / 3.0
            - (payment + tau) * radius**2 / 2.0
        )

    return float(max(primitive(radius_cap) - primitive(1.0), 0.0))


def solve_terminal_market(
    cutoff: float,
    payment: float,
    reach: float,
    params: Params,
    regime: SupplyRegime,
) -> TerminalMarket:
    """Terminal volunteer market conditional on universal rejection."""

    incumbent = params.incumbent_retention * params.m * max(
        float(uniform_cdf(payment)) - float(uniform_cdf(cutoff)), 0.0
    )
    if regime == "incumbent_only":
        potential_fresh = 0.0
        core_fresh = 0.0
        outer_fresh = 0.0
        fresh = 0.0
        pickup_intensity = 0.0
    else:
        effective_reach = reach if regime == "expanded_search" else 1.0
        potential_fresh = params.m * effective_reach
        core_fresh = fresh_accept_intensity(payment, 1.0, params)
        fresh = fresh_accept_intensity(payment, effective_reach, params)
        outer_fresh = max(fresh - core_fresh, 0.0)
        pickup_intensity = fresh_pickup_cost_intensity(
            payment, effective_reach, params
        )
    total = incumbent + fresh
    assignment = assignment_probability(total)
    return TerminalMarket(
        payment=payment,
        search_multiplier=reach,
        potential_fresh_intensity=potential_fresh,
        incumbent_intensity=incumbent,
        core_fresh_accept_intensity=core_fresh,
        outer_fresh_accept_intensity=outer_fresh,
        fresh_accept_intensity=fresh,
        total_intensity=total,
        assignment_probability=assignment,
        coverage=float(-np.expm1(-total)),
        fresh_pickup_cost_intensity=pickup_intensity,
    )


def _choose_rider_action(
    value: float, policy: Policy, params: Params, c_repeat: float, c_rescue: float
) -> int:
    """Return 0 abandon, 1 repeat, or 2 rescue with deterministic ties.

    The closure follows the theory note: abandon before repeat before rescue.
    Comparisons are exact rather than tolerance based.  A fixed absolute
    utility tolerance is unsafe in very thin markets because every continuation
    utility is then small even when the rider has a strict preference.
    """

    u_repeat = c_repeat * (params.beta * value - policy.p1)
    u_rescue = c_rescue * (params.beta * value - policy.p2)
    if 0.0 >= u_repeat and 0.0 >= u_rescue:
        return 0
    if u_repeat >= u_rescue:
        return 1
    return 2


def rider_action_masses(
    policy: Policy, params: Params, c_repeat: float, c_rescue: float
) -> tuple[float, float, float]:
    """Exact ordered-envelope action masses conditional on posting.

    Maintained terminal supply implies ``0 <= c_repeat <= c_rescue``.  Scaling
    both coverages before forming the repeat-rescue crossing keeps the formula
    accurate even when market thickness, and hence both coverages, approach
    zero.
    """

    if policy.p1 >= 1:
        return 0.0, 0.0, 1.0

    lower, upper = policy.p1, 1.0
    posted = upper - lower
    c1 = max(float(c_repeat), 0.0)
    c2 = max(float(c_rescue), 0.0)
    scale = max(c1, c2)
    if scale == 0.0:
        return 0.0, 0.0, 1.0

    c1_scaled, c2_scaled = c1 / scale, c2 / scale
    if c2_scaled < c1_scaled:
        if c1_scaled - c2_scaled <= 32 * np.finfo(float).eps:
            c2_scaled = c1_scaled
        else:
            raise ValueError("maintained model requires rescue coverage >= repeat coverage")

    repeat_start = max(lower, policy.p1 / params.beta)
    repeat_length = 0.0
    rescue_length = 0.0
    coverage_gap = c2_scaled - c1_scaled

    if coverage_gap > 0.0:
        # Algebraically equivalent to (C2*p2-C1*p1)/(beta*(C2-C1)),
        # but avoids catastrophic cancellation when prices or coverages are
        # nearly equal.  It is exact at p2=p1.
        crossing = policy.p1 / params.beta + (
            c2_scaled * (policy.p2 - policy.p1)
        ) / (params.beta * coverage_gap)
        rescue_start = max(lower, crossing)
        if rescue_start < upper:
            rescue_length = upper - rescue_start
            if c1 > 0.0 and repeat_start < rescue_start:
                repeat_length = min(rescue_start, upper) - repeat_start
        elif c1 > 0.0 and repeat_start < upper:
            repeat_length = upper - repeat_start
    elif c1 > 0.0 and repeat_start < upper:
        # Equal coverage: repeat weakly dominates because p1 <= p2, with the
        # deterministic tie closure selecting repeat when prices are equal.
        repeat_length = upper - repeat_start

    repeat_mass = max(repeat_length / posted, 0.0)
    rescue_mass = max(rescue_length / posted, 0.0)
    abandon_mass = max(1.0 - repeat_mass - rescue_mass, 0.0)
    total = repeat_mass + rescue_mass + abandon_mass
    return (
        float(repeat_mass / total),
        float(rescue_mass / total),
        float(abandon_mass / total),
    )


def rider_terminal_completion_mass(
    policy: Policy, params: Params, c_repeat: float, c_rescue: float
) -> float:
    """Unconditional rider mass completed after first-window failure.

    This is the exact upper-envelope formula from the theory note.  It remains
    valid on the full price domain and avoids reconstructing completion from
    potentially tie-dependent action labels.
    """

    repeat_value = (1.0 - policy.p1 / params.beta) * c_repeat
    rescue_value = (1.0 - policy.p2 / params.beta) * c_rescue
    return float(max(0.0, repeat_value, rescue_value))


def continuation_at_cutoff(
    cutoff: float, policy: Policy, params: Params
) -> tuple[TerminalMarket, TerminalMarket, float, float, float]:
    """Solve both counterfactual terminal branches at one incumbent cutoff."""

    repeat = solve_terminal_market(
        cutoff, policy.p1, 1.0, params, policy.regime
    )
    rescue = solve_terminal_market(
        cutoff, policy.p2, policy.s, params, policy.regime
    )
    repeat_mass, rescue_mass, abandon_mass = rider_action_masses(
        policy, params, repeat.coverage, rescue.coverage
    )
    return repeat, rescue, repeat_mass, rescue_mass, abandon_mass


def cutoff_residual(cutoff: float, policy: Policy, params: Params) -> float:
    """Immediate-accept payoff minus reject-and-wait payoff for type cutoff."""

    repeat, rescue, eta_repeat, eta_rescue, _ = continuation_at_cutoff(
        cutoff, policy, params
    )
    immediate = assignment_probability(params.m * uniform_cdf(cutoff)) * (
        policy.p1 - cutoff
    )
    universal_rejection = np.exp(-params.m * uniform_cdf(cutoff))
    waiting = params.delta * params.incumbent_retention * universal_rejection * (
        eta_repeat
        * repeat.assignment_probability
        * max(policy.p1 - cutoff, 0.0)
        + eta_rescue
        * rescue.assignment_probability
        * max(policy.p2 - cutoff, 0.0)
    )
    return float(immediate - waiting)


def _payoff_difference(
    cost: float,
    cutoff: float,
    policy: Policy,
    params: Params,
    repeat: TerminalMarket,
    rescue: TerminalMarket,
    eta_repeat: float,
    eta_rescue: float,
) -> float:
    immediate = assignment_probability(params.m * uniform_cdf(cutoff)) * (
        policy.p1 - cost
    )
    universal_rejection = np.exp(-params.m * uniform_cdf(cutoff))
    waiting = params.delta * params.incumbent_retention * universal_rejection * (
        eta_repeat
        * repeat.assignment_probability
        * max(policy.p1 - cost, 0.0)
        + eta_rescue
        * rescue.assignment_probability
        * max(policy.p2 - cost, 0.0)
    )
    return float(immediate - waiting)


def is_cutoff_best_response(cutoff: float, policy: Policy, params: Params) -> bool:
    """Exactly check the cutoff strategy's one-shot deviation inequalities.

    Conditional on a proposed aggregate cutoff, a driver's accept-minus-wait
    payoff is continuous and piecewise affine in her cost.  Its only kinks are
    at ``p1`` and ``p2``.  It is therefore sufficient (and exact up to floating
    point tolerance) to check interval endpoints rather than a sampled type
    grid.
    """

    repeat, rescue, eta_repeat, eta_rescue, _ = continuation_at_cutoff(
        cutoff, policy, params
    )
    def difference(cost: float) -> float:
        return _payoff_difference(
            cost,
            cutoff,
            policy,
            params,
            repeat,
            rescue,
            eta_repeat,
            eta_rescue,
        )

    payoff_scale = max(policy.p1, policy.p2, np.finfo(float).tiny)
    tolerance = 256 * np.finfo(float).eps * payoff_scale
    accept_points = [0.0, cutoff] if cutoff > 0.0 else []
    wait_points = [cutoff, policy.p1, policy.p2, 1.0]
    wait_points = [
        point for point in wait_points if cutoff <= point <= 1.0
    ]
    accept_ok = all(difference(point) >= -tolerance for point in accept_points)
    wait_ok = all(difference(point) <= tolerance for point in wait_points)
    return bool(accept_ok and wait_ok)


def _deduplicate(values: Iterable[float]) -> list[float]:
    values = sorted(values)
    if not values:
        return []
    scale = max(max(abs(value) for value in values), np.finfo(float).tiny)
    tolerance = 64 * np.finfo(float).eps * scale
    result: list[float] = []
    for value in values:
        if not result or abs(value - result[-1]) > tolerance:
            result.append(float(value))
    return result


def find_cutoff_equilibria(
    policy: Policy,
    params: Params,
    grid_size: int = 301,
    validate: bool = True,
) -> list[float]:
    """Enumerate boundary and sign-changing roots for independent audit.

    Under the maintained unique-cutoff theorem every interior root crosses
    strictly downward, so tangential-root heuristics are neither needed nor
    desirable for certification.
    """

    if (
        policy.p1 == policy.p2
        or policy.p1 >= params.beta
        or params.incumbent_retention == 0
    ):
        return [policy.p1]
    if policy.p1 == 0:
        candidates = (
            [0.0] if cutoff_residual(0.0, policy, params) <= 0.0 else []
        )
    else:
        grid = np.linspace(0.0, policy.p1, grid_size)
        values = np.array([cutoff_residual(point, policy, params) for point in grid])
        candidates: list[float] = []

        if values[0] <= 0.0:
            candidates.append(0.0)
        if values[-1] == 0.0 and is_cutoff_best_response(
            policy.p1, policy, params
        ):
            candidates.append(policy.p1)

        for left, right, f_left, f_right in zip(
            grid[:-1], grid[1:], values[:-1], values[1:]
        ):
            if f_left * f_right < 0:
                left_unit, right_unit = left / policy.p1, right / policy.p1
                root_unit = brentq(
                    lambda unit: cutoff_residual(
                        policy.p1 * unit, policy, params
                    ),
                    left_unit,
                    right_unit,
                    xtol=1e-14,
                    rtol=1e-14,
                )
                candidates.append(float(policy.p1 * root_unit))

    candidates = _deduplicate(candidates)
    if validate:
        candidates = [
            candidate
            for candidate in candidates
            if is_cutoff_best_response(candidate, policy, params)
        ]
    if not candidates:
        raise RuntimeError(
            f"No cutoff-WPBE found for policy={policy}, params={params}"
        )
    return candidates


def find_unique_cutoff(
    policy: Policy,
    params: Params,
    validate: bool = True,
) -> float:
    """Solve the unique maintained-model cutoff by endpoint bracketing.

    The unique-cutoff theorem applies to the maintained uniform-cost,
    type-independent-retention, cutoff-independent-fresh-supply model.  Dense
    all-root enumeration remains available as an independent certification
    method through ``find_cutoff_equilibria``.
    """

    if (
        policy.p1 == 0.0
        or policy.p1 == policy.p2
        or policy.p1 >= params.beta
        or params.incumbent_retention == 0.0
    ):
        cutoff = policy.p1
    else:
        left_value = cutoff_residual(0.0, policy, params)
        if left_value <= 0.0:
            cutoff = 0.0
        else:
            right_value = cutoff_residual(policy.p1, policy, params)
            if right_value > 0.0:
                raise RuntimeError(
                    "Unique-cutoff bracket failed: residual is positive at p1 "
                    f"for policy={policy}, params={params}"
                )
            if right_value == 0.0:
                cutoff = policy.p1
            else:
                root_unit = brentq(
                    lambda unit: cutoff_residual(
                        policy.p1 * unit, policy, params
                    ),
                    0.0,
                    1.0,
                    xtol=1e-14,
                    rtol=1e-14,
                )
                cutoff = float(policy.p1 * root_unit)
    if validate and not is_cutoff_best_response(cutoff, policy, params):
        raise RuntimeError(
            "Bracketed cutoff fails the full best-response test: "
            f"cutoff={cutoff}, policy={policy}, params={params}, "
            f"residual={cutoff_residual(cutoff, policy, params)}"
        )
    return float(cutoff)


def outcome_at_cutoff(
    cutoff: float, policy: Policy, params: Params
) -> EquilibriumOutcome:
    """Evaluate all equilibrium outcomes at a validated cutoff."""

    repeat, rescue, eta_repeat, eta_rescue, eta_abandon = continuation_at_cutoff(
        cutoff, policy, params
    )
    posted = 1.0 - policy.p1
    universal_rejection = np.exp(-params.m * uniform_cdf(cutoff))
    first = posted * (1.0 - universal_rejection)
    repeat_completion = (
        posted * universal_rejection * eta_repeat * repeat.coverage
    )
    rescue_completion = (
        posted * universal_rejection * eta_rescue * rescue.coverage
    )

    repeat_incumbent = (
        posted
        * universal_rejection
        * eta_repeat
        * repeat.incumbent_intensity
        * repeat.assignment_probability
    )
    repeat_fresh = (
        posted
        * universal_rejection
        * eta_repeat
        * repeat.fresh_accept_intensity
        * repeat.assignment_probability
    )
    rescue_incumbent = (
        posted
        * universal_rejection
        * eta_rescue
        * rescue.incumbent_intensity
        * rescue.assignment_probability
    )
    rescue_fresh = (
        posted
        * universal_rejection
        * eta_rescue
        * rescue.fresh_accept_intensity
        * rescue.assignment_probability
    )
    terminal_completion = universal_rejection * rider_terminal_completion_mass(
        policy, params, repeat.coverage, rescue.coverage
    )
    completion = first + terminal_completion

    transfer = posted * (
        policy.p1 * (1.0 - universal_rejection)
        + universal_rejection
        * (
            eta_repeat * policy.p1 * repeat.coverage
            + eta_rescue * policy.p2 * rescue.coverage
        )
    )
    fresh_acceptors = posted * universal_rejection * (
        eta_repeat * repeat.fresh_accept_intensity
        + eta_rescue * rescue.fresh_accept_intensity
    )
    pickup_cost = posted * universal_rejection * (
        eta_repeat
        * repeat.assignment_probability
        * repeat.fresh_pickup_cost_intensity
        + eta_rescue
        * rescue.assignment_probability
        * rescue.fresh_pickup_cost_intensity
    )
    if policy.regime == "incumbent_only":
        notifications = 0.0
        extra_notifications = 0.0
        committed_outer_capacity = 0.0
    else:
        core_notifications = (
            posted
            * universal_rejection
            * params.m
            * (eta_repeat + eta_rescue)
        )
        extra_notifications = (
            posted
            * universal_rejection
            * eta_rescue
            * params.m
            * (policy.s - 1.0)
            if policy.regime == "expanded_search"
            else 0.0
        )
        notifications = core_notifications + extra_notifications
        committed_outer_capacity = (
            posted
            * universal_rejection
            * params.m
            * (policy.s - 1.0)
            if policy.regime == "expanded_search"
            else 0.0
        )

    step = max(1e-5, min(1e-3, policy.p1 / 100 if policy.p1 > 0 else 1e-4))
    left = max(0.0, cutoff - step)
    right = min(policy.p1, cutoff + step)
    if right > left:
        derivative = (
            cutoff_residual(right, policy, params)
            - cutoff_residual(left, policy, params)
        ) / (right - left)
    else:
        derivative = np.nan

    return EquilibriumOutcome(
        policy=policy,
        params=params,
        cutoff=cutoff,
        stable=bool(np.isfinite(derivative) and derivative < 0),
        residual=cutoff_residual(cutoff, policy, params),
        repeat_mass=eta_repeat,
        rescue_mass=eta_rescue,
        abandon_mass=eta_abandon,
        repeat=repeat,
        rescue=rescue,
        posted_probability=posted,
        first_completion=first,
        repeat_completion=repeat_completion,
        rescue_completion=rescue_completion,
        repeat_incumbent_completion=repeat_incumbent,
        repeat_fresh_completion=repeat_fresh,
        rescue_incumbent_completion=rescue_incumbent,
        rescue_fresh_completion=rescue_fresh,
        completion=completion,
        expected_transfer=transfer,
        expected_fresh_acceptors=fresh_acceptors,
        expected_pickup_cost=pickup_cost,
        expected_notifications=notifications,
        expected_extra_notifications=extra_notifications,
        expected_committed_outer_capacity=committed_outer_capacity,
    )


def solve_policy(
    policy: Policy,
    params: Params,
    selection: Selection = "conservative",
    grid_size: int = 301,
    validate: bool = True,
    root_method: RootMethod = "unique",
) -> PolicySolution:
    """Solve the complete inner cutoff-WPBE correspondence for one mechanism."""

    if root_method == "unique":
        cutoffs = [find_unique_cutoff(policy, params, validate)]
    elif root_method == "enumerate":
        cutoffs = find_cutoff_equilibria(policy, params, grid_size, validate)
    else:
        raise ValueError(f"unknown root method: {root_method}")
    equilibria = tuple(outcome_at_cutoff(cutoff, policy, params) for cutoff in cutoffs)
    if selection == "conservative":
        selected = min(equilibria, key=lambda outcome: outcome.completion)
    elif selection == "optimistic":
        selected = max(equilibria, key=lambda outcome: outcome.completion)
    elif selection == "stable":
        stable = [outcome for outcome in equilibria if outcome.stable]
        selected = min(stable or list(equilibria), key=lambda outcome: outcome.completion)
    else:
        raise ValueError(f"unknown equilibrium selection: {selection}")
    return PolicySolution(policy, params, equilibria, selected, selection)


def solve_policy_certified(
    policy: Policy,
    params: Params,
    selection: Selection = "conservative",
    initial_grid: int = 301,
    max_grid: int = 2401,
    root_tolerance: float = 5e-6,
) -> CertificationResult:
    """Grid-double until the complete numerical cutoff correspondence stabilizes.

    Exact best-response validation is applied at every grid.  Requiring the
    same root count and locations on two successive refinements protects the
    outer mechanism design from a root found only on one coarse discretization.
    """

    if initial_grid < 31:
        raise ValueError("initial_grid must be at least 31")
    if max_grid < initial_grid:
        raise ValueError("max_grid must be no smaller than initial_grid")

    grids: list[int] = []
    root_sets: list[tuple[float, ...]] = []
    solutions: list[PolicySolution] = []
    grid = initial_grid
    stable_rounds = 0

    while True:
        solution = solve_policy(
            policy,
            params,
            selection=selection,
            grid_size=grid,
            validate=True,
            root_method="enumerate",
        )
        roots = tuple(equilibrium.cutoff for equilibrium in solution.equilibria)
        grids.append(grid)
        root_sets.append(roots)
        solutions.append(solution)

        if len(root_sets) >= 2:
            previous, current = root_sets[-2], root_sets[-1]
            same = len(previous) == len(current) and all(
                abs(left - right) <= root_tolerance
                for left, right in zip(previous, current)
            )
            stable_rounds = stable_rounds + 1 if same else 0
        if stable_rounds >= 2:
            return CertificationResult(
                solutions[-1], tuple(grids), tuple(root_sets), True
            )
        if grid >= max_grid:
            return CertificationResult(
                solutions[-1], tuple(grids), tuple(root_sets), False
            )
        grid = min(2 * grid - 1, max_grid)


def outcome_record(solution: PolicySolution) -> dict[str, float | int | bool | str]:
    """Flatten the selected WPBE for tables and audits."""

    outcome = solution.selected
    return {
        "m": outcome.params.m,
        "beta": outcome.params.beta,
        "delta": outcome.params.delta,
        "pickup_rate": outcome.params.pickup_rate,
        "incumbent_retention": outcome.params.incumbent_retention,
        "regime": outcome.policy.regime,
        "p1": outcome.policy.p1,
        "p2": outcome.policy.p2,
        "s": outcome.policy.s,
        "cutoff": outcome.cutoff,
        "equilibrium_count": solution.equilibrium_count,
        "completion_spread": solution.completion_spread,
        "stable": outcome.stable,
        "repeat_mass": outcome.repeat_mass,
        "rescue_mass": outcome.rescue_mass,
        "abandon_mass": outcome.abandon_mass,
        "first_completion": outcome.first_completion,
        "repeat_completion": outcome.repeat_completion,
        "rescue_completion": outcome.rescue_completion,
        "completion": outcome.completion,
        "repeat_coverage": outcome.repeat.coverage,
        "rescue_coverage": outcome.rescue.coverage,
        "repeat_fresh_accept_intensity": outcome.repeat.fresh_accept_intensity,
        "rescue_fresh_accept_intensity": outcome.rescue.fresh_accept_intensity,
        "repeat_incumbent_intensity": outcome.repeat.incumbent_intensity,
        "rescue_incumbent_intensity": outcome.rescue.incumbent_intensity,
        "repeat_core_fresh_intensity": outcome.repeat.core_fresh_accept_intensity,
        "rescue_core_fresh_intensity": outcome.rescue.core_fresh_accept_intensity,
        "repeat_outer_fresh_intensity": outcome.repeat.outer_fresh_accept_intensity,
        "rescue_outer_fresh_intensity": outcome.rescue.outer_fresh_accept_intensity,
        "repeat_total_intensity": outcome.repeat.total_intensity,
        "rescue_total_intensity": outcome.rescue.total_intensity,
        "expected_transfer": outcome.expected_transfer,
        "expected_fresh_acceptors": outcome.expected_fresh_acceptors,
        "expected_pickup_cost": outcome.expected_pickup_cost,
        "expected_notifications": outcome.expected_notifications,
        "expected_extra_notifications": outcome.expected_extra_notifications,
        "expected_committed_outer_capacity": (
            outcome.expected_committed_outer_capacity
        ),
    }

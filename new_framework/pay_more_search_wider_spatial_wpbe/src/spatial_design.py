"""Outer mechanism design over inner cutoff-WPBE outcomes.

For each environment theta=(m,beta,delta), the platform solves three successive
notification regimes under conservative equilibrium selection:

    incumbent only:  max_{p1<=p2}       J(p1,p2,1)
    core arrivals:   max_{p1<=p2}       J(p1,p2,1)
    expanded search: max_{p1<=p2,s>=1} J(p1,p2,s).

The first two have different terminal supply technologies.  The latter two
are genuinely nested because ``s=1`` exactly reproduces core arrivals.

Every objective evaluation calls ``solve_policy`` and therefore re-enumerates
the induced cutoff-WPBE correspondence.  No cutoff, rider continuation share,
or terminal supply outcome is fixed in the outer design.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Literal

import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar

from spatial_wpbe import (
    Params,
    Policy,
    PolicySolution,
    outcome_record,
    solve_policy,
    solve_policy_certified,
)


Mechanism = Literal[
    "incumbent_only",
    "fixed_arrivals",
    "expanded_search",
]
SearchCostBasis = Literal["committed_reach", "executed_contacts"]


@dataclass(frozen=True)
class Environment:
    m: float
    beta: float
    delta: float
    pickup_rate: float = 0.25
    incumbent_retention: float = 1.0
    completion_value: float = 1.0
    search_cost: float = 0.0
    search_cost_basis: SearchCostBasis = "committed_reach"

    def __post_init__(self) -> None:
        if self.completion_value <= 0:
            raise ValueError("completion_value must be strictly positive")
        if self.search_cost < 0:
            raise ValueError("search_cost must be nonnegative")
        if self.search_cost_basis not in {
            "committed_reach",
            "executed_contacts",
        }:
            raise ValueError(f"unknown search cost basis: {self.search_cost_basis}")

    def params(self) -> Params:
        return Params(
            self.m,
            self.beta,
            self.delta,
            self.pickup_rate,
            self.incumbent_retention,
        )

    def search_resource(self, outcome) -> float:
        """Failure-contingent resource charged by the outer objective."""

        if self.search_cost_basis == "committed_reach":
            return float(outcome.expected_committed_outer_capacity)
        return float(outcome.expected_extra_notifications)

    def outcome_value(self, outcome) -> float:
        return float(
            self.completion_value * outcome.completion
            - self.search_cost * self.search_resource(outcome)
        )


@dataclass(frozen=True)
class SearchConfig:
    s_bar: float = 2.5
    cutoff_grid: int = 81
    final_cutoff_grid: int = 1001
    p1_nodes: int = 13
    p1_refine_levels: int = 3
    inner_refine_levels: int = 3
    adversarial_seeds: int = 0
    adversarial_maxiter: int = 16
    adversarial_popsize: int = 8
    adversarial_tol: float = 2e-5
    certify_top_k: int = 10
    certify_finalists: int = 3
    certification_max_grid: int = 2001

    def __post_init__(self) -> None:
        if self.s_bar < 1:
            raise ValueError("s_bar must be at least one")
        if self.cutoff_grid < 31 or self.final_cutoff_grid < self.cutoff_grid:
            raise ValueError("cutoff grids are too small or incorrectly ordered")
        if self.p1_nodes < 7:
            raise ValueError("p1_nodes must be at least seven")
        if self.adversarial_seeds < 0:
            raise ValueError("adversarial_seeds must be nonnegative")
        if self.adversarial_maxiter < 1 or self.adversarial_popsize < 4:
            raise ValueError("adversarial DE settings are too small")
        if self.adversarial_tol <= 0:
            raise ValueError("adversarial_tol must be strictly positive")
        if self.certify_top_k < 1:
            raise ValueError("certify_top_k must be positive")
        if self.certify_finalists < 1:
            raise ValueError("certify_finalists must be positive")
        if self.certification_max_grid < self.final_cutoff_grid:
            raise ValueError("certification_max_grid must exceed final cutoff grid")


@dataclass(frozen=True)
class InnerResult:
    mechanism: Mechanism
    p1: float
    solution: PolicySolution


@dataclass(frozen=True)
class MechanismResult:
    mechanism: Mechanism
    environment: Environment
    solution: PolicySolution
    profile: tuple[InnerResult, ...]
    exploration_evaluations: int
    certification_stable: bool = False
    certification_grids: tuple[int, ...] = ()
    adversarial_seed_count: int = 0
    adversarial_evaluations: int = 0
    adversarial_improvement: float = 0.0

    @property
    def p1(self) -> float:
        return self.solution.policy.p1

    @property
    def p2(self) -> float:
        return self.solution.policy.p2

    @property
    def s(self) -> float:
        return self.solution.policy.s

    @property
    def completion(self) -> float:
        return self.solution.selected.completion

    @property
    def design_value(self) -> float:
        return self.environment.outcome_value(self.solution.selected)

    @property
    def search_resource(self) -> float:
        return self.environment.search_resource(self.solution.selected)


def _chebyshev_lobatto(lower: float, upper: float, count: int) -> np.ndarray:
    if upper <= lower:
        return np.array([lower], dtype=float)
    indices = np.arange(count)
    raw = 0.5 * (1.0 - np.cos(np.pi * indices / (count - 1)))
    return lower + (upper - lower) * raw


def _deduplicate(values: Iterable[float], digits: int = 10) -> list[float]:
    return sorted({round(float(value), digits) for value in values})


class SpatialMechanismSolver:
    """Profile continuation tools at p1, then optimize p1."""

    def __init__(
        self, environment: Environment, config: SearchConfig | None = None
    ) -> None:
        self.environment = environment
        self.params = environment.params()
        self.config = config or SearchConfig()
        self._cache: dict[tuple[float, float, float, str], PolicySolution] = {}
        self._evaluation_count = 0

    @property
    def evaluation_count(self) -> int:
        return self._evaluation_count

    def _outcome_value(self, outcome) -> float:
        return self.environment.outcome_value(outcome)

    def _reselect(self, solution: PolicySolution) -> PolicySolution:
        """Apply conservative selection to the platform's actual objective."""

        selected = min(solution.equilibria, key=self._outcome_value)
        return replace(solution, selected=selected)

    def _solution_key(
        self, solution: PolicySolution
    ) -> tuple[float, float, float, float, float, float]:
        policy = solution.policy
        return (
            self._outcome_value(solution.selected),
            -policy.s,
            -self.environment.search_resource(solution.selected),
            solution.selected.completion,
            -(policy.p2 - policy.p1),
            -policy.p1,
        )

    def _solve(self, policy: Policy) -> PolicySolution:
        key = (
            round(policy.p1, 10),
            round(policy.p2, 10),
            round(policy.s, 10),
            policy.regime,
        )
        if key not in self._cache:
            self._cache[key] = self._reselect(
                solve_policy(
                    policy,
                    self.params,
                    selection="conservative",
                    grid_size=self.config.cutoff_grid,
                    validate=True,
                )
            )
            self._evaluation_count += 1
        return self._cache[key]

    def _policy(
        self,
        p1: float,
        price_unit: float,
        search_unit: float,
        mechanism: Mechanism,
    ) -> Policy:
        p2 = p1 + price_unit * max(self.params.beta - p1, 0.0)
        search = (
            1.0 + search_unit * (self.config.s_bar - 1.0)
            if mechanism == "expanded_search"
            else 1.0
        )
        if mechanism == "expanded_search" and self.params.pickup_rate > 0:
            # Rings beyond this area contain no willing driver because even a
            # zero-base-cost winner would pay more than p2.  Truncating there
            # is without loss under nonnegative search cost and implements
            # the smallest-s tie break when committed reach is free.
            saturation = (1.0 + p2 / self.params.pickup_rate) ** 2
            search = min(search, saturation)
        regime = "core_arrivals" if mechanism == "fixed_arrivals" else mechanism
        return Policy(float(p1), float(p2), float(search), regime=regime)

    @staticmethod
    def _initial_grids(mechanism: Mechanism) -> tuple[list[float], list[float]]:
        price = [0.0, 0.05, 0.15, 0.30, 0.50, 0.75, 1.0]
        search = [0.0, 0.10, 0.30, 0.55, 0.80, 1.0]
        if mechanism in {"incumbent_only", "fixed_arrivals"}:
            return price, [0.0]
        return price, search

    def optimize_inner(
        self,
        p1: float,
        mechanism: Mechanism,
        *,
        refine_levels: int | None = None,
    ) -> InnerResult:
        """Optimize continuation policy conditional on one first price."""

        p1 = float(np.clip(p1, 0.0, 1.0))
        if p1 >= self.params.beta - 1e-12:
            return InnerResult(
                mechanism,
                p1,
                self._solve(self._policy(p1, 0.0, 0.0, mechanism)),
            )

        price_grid, search_grid = self._initial_grids(mechanism)
        candidates: list[tuple[float, float, PolicySolution]] = []

        def add(price_unit: float, search_unit: float) -> None:
            solution = self._solve(
                self._policy(p1, price_unit, search_unit, mechanism)
            )
            candidates.append((float(price_unit), float(search_unit), solution))

        for price_unit in price_grid:
            for search_unit in search_grid:
                add(price_unit, search_unit)

        def best_candidate() -> tuple[float, float, PolicySolution]:
            return max(candidates, key=lambda item: self._solution_key(item[2]))

        levels = (
            self.config.inner_refine_levels
            if refine_levels is None
            else refine_levels
        )
        price_width, search_width = 0.20, 0.22
        for _ in range(levels):
            price_center, search_center, _ = best_candidate()
            prices = np.linspace(
                max(0.0, price_center - price_width),
                min(1.0, price_center + price_width),
                5,
            )
            if mechanism == "expanded_search":
                searches = np.linspace(
                    max(0.0, search_center - search_width),
                    min(1.0, search_center + search_width),
                    5,
                )
            else:
                searches = np.array([0.0])
            for price_unit in prices:
                for search_unit in searches:
                    add(float(price_unit), float(search_unit))
            price_width *= 0.35
            search_width *= 0.35

        return InnerResult(mechanism, p1, best_candidate()[2])

    def _inactive_branch(self, mechanism: Mechanism) -> PolicySolution:
        """Optimize p1>=beta, where delayed service has zero positive mass."""

        lower = min(self.params.beta, 1.0)
        if lower >= 1.0 - 1e-12:
            return self._solve(self._policy(1.0, 0.0, 0.0, mechanism))
        optimum = minimize_scalar(
            lambda price: -self._outcome_value(
                self._solve(
                    self._policy(float(price), 0.0, 0.0, mechanism)
                ).selected
            ),
            bounds=(lower, 1.0),
            method="bounded",
            options={"xatol": 2e-6},
        )
        candidates = [
            self._solve(self._policy(lower, 0.0, 0.0, mechanism)),
            self._solve(self._policy(float(optimum.x), 0.0, 0.0, mechanism)),
            self._solve(self._policy(1.0, 0.0, 0.0, mechanism)),
        ]
        return max(candidates, key=self._solution_key)

    def _adversarial_candidates(
        self, mechanism: Mechanism
    ) -> tuple[tuple[PolicySolution, ...], int]:
        """Challenge the nested profile with an independent global search.

        The maintained computation first profiles p2,s at each fixed p1 and
        then optimizes p1.  Differential evolution is a separate adversarial
        pass over the equivalent normalized product domain.  Any better basin
        it finds is fed into the same dense cutoff-WPBE certification.  This
        is a numerical cross-check, not a mathematical proof of globality.
        """

        if self.config.adversarial_seeds == 0:
            return (), 0

        dimensions = 3 if mechanism == "expanded_search" else 2
        active_upper = min(self.params.beta, 1.0)
        starting_evaluations = self.evaluation_count
        candidates: list[PolicySolution] = []
        mechanism_offset = {
            "incumbent_only": 104729,
            "fixed_arrivals": 130363,
            "expanded_search": 155921,
        }[mechanism]
        base_seed = int(
            round(1000 * self.params.m)
            + 1009 * round(100 * self.params.beta)
            + 9176 * round(100 * self.params.delta)
            + mechanism_offset
        )

        def policy_from(vector: np.ndarray) -> Policy:
            p1 = active_upper * float(np.clip(vector[0], 0.0, 1.0))
            price_unit = float(np.clip(vector[1], 0.0, 1.0))
            search_unit = (
                float(np.clip(vector[2], 0.0, 1.0))
                if dimensions == 3
                else 0.0
            )
            return self._policy(p1, price_unit, search_unit, mechanism)

        def objective(vector: np.ndarray) -> float:
            solution = self._solve(policy_from(vector))
            return -self._outcome_value(solution.selected)

        for seed_index in range(self.config.adversarial_seeds):
            optimum = differential_evolution(
                objective,
                bounds=[(0.0, 1.0)] * dimensions,
                seed=base_seed + 7919 * seed_index,
                maxiter=self.config.adversarial_maxiter,
                popsize=self.config.adversarial_popsize,
                tol=self.config.adversarial_tol,
                atol=1e-7,
                polish=True,
                updating="immediate",
                workers=1,
            )
            candidates.append(self._solve(policy_from(optimum.x)))

        return tuple(candidates), self.evaluation_count - starting_evaluations

    def optimize(self, mechanism: Mechanism) -> MechanismResult:
        """Solve one outer equilibrium-constrained mechanism problem."""

        starting_evaluations = self.evaluation_count
        active_upper = min(self.params.beta, 1.0)
        p1_values = list(
            _chebyshev_lobatto(0.0, active_upper, self.config.p1_nodes)
        )
        profile: dict[float, InnerResult] = {}

        def evaluate(price: float, levels: int | None = None) -> None:
            key = round(float(price), 10)
            if key not in profile:
                profile[key] = self.optimize_inner(
                    float(price), mechanism, refine_levels=levels
                )

        for price in p1_values:
            evaluate(float(price))

        width = active_upper / max(self.config.p1_nodes - 1, 1)
        for _ in range(self.config.p1_refine_levels):
            best = max(
                profile.values(), key=lambda result: self._solution_key(result.solution)
            )
            local = np.linspace(
                max(0.0, best.p1 - 2.0 * width),
                min(active_upper, best.p1 + 2.0 * width),
                7,
            )
            for price in local:
                evaluate(float(price), max(1, self.config.inner_refine_levels - 1))
            width *= 0.35

        candidates = [result.solution for result in profile.values()]
        candidates.append(self._inactive_branch(mechanism))
        best_explored = max(candidates, key=self._solution_key)
        result = MechanismResult(
            mechanism=mechanism,
            environment=self.environment,
            solution=best_explored,
            profile=tuple(sorted(profile.values(), key=lambda item: item.p1)),
            exploration_evaluations=self.evaluation_count - starting_evaluations,
        )
        nested = self._certify(result)
        adversarial, adversarial_evaluations = self._adversarial_candidates(
            mechanism
        )
        if not adversarial:
            return nested
        audited = self._certify(nested, adversarial)
        return replace(
            audited,
            adversarial_seed_count=self.config.adversarial_seeds,
            adversarial_evaluations=adversarial_evaluations,
            adversarial_improvement=max(
                audited.design_value - nested.design_value, 0.0
            ),
        )

    def _feasible(self, policy: Policy, mechanism: Mechanism) -> bool:
        expected_regime = (
            "core_arrivals" if mechanism == "fixed_arrivals" else mechanism
        )
        if policy.regime != expected_regime:
            return False
        if mechanism in {"incumbent_only", "fixed_arrivals"}:
            return abs(policy.s - 1.0) <= 1e-10
        return 1.0 <= policy.s <= self.config.s_bar + 1e-10

    def _certify(
        self,
        target: MechanismResult,
        injected: tuple[PolicySolution, ...] = (),
    ) -> MechanismResult:
        """Dense-grid WPBE validation and candidate re-ranking."""

        explored = [
            solution
            for solution in self._cache.values()
            if self._feasible(solution.policy, target.mechanism)
        ]
        explored.sort(key=self._solution_key, reverse=True)
        candidates = [target.solution]
        candidates.extend(injected)
        candidates.extend(explored[: self.config.certify_top_k])

        unique: dict[tuple[float, float, float], PolicySolution] = {}
        for candidate in candidates:
            policy = candidate.policy
            key = (
                round(policy.p1, 10),
                round(policy.p2, 10),
                round(policy.s, 10),
            )
            unique[key] = candidate

        dense = [
            self._reselect(
                solve_policy(
                    candidate.policy,
                    self.params,
                    selection="conservative",
                    grid_size=self.config.final_cutoff_grid,
                    validate=True,
                )
            )
            for candidate in unique.values()
        ]
        dense.sort(key=self._solution_key, reverse=True)
        finalists = dense[: self.config.certify_finalists]
        certified = []
        for finalist in finalists:
            certificate = solve_policy_certified(
                finalist.policy,
                self.params,
                selection="conservative",
                initial_grid=self.config.final_cutoff_grid,
                max_grid=self.config.certification_max_grid,
            )
            certified.append(
                replace(certificate, solution=self._reselect(certificate.solution))
            )
        best_certificate = max(
            certified, key=lambda item: self._solution_key(item.solution)
        )
        best = best_certificate.solution
        return MechanismResult(
            mechanism=target.mechanism,
            environment=target.environment,
            solution=best,
            profile=target.profile,
            exploration_evaluations=target.exploration_evaluations,
            certification_stable=best_certificate.stable,
            certification_grids=best_certificate.grids,
            adversarial_seed_count=target.adversarial_seed_count,
            adversarial_evaluations=target.adversarial_evaluations,
            adversarial_improvement=target.adversarial_improvement,
        )

    def optimize_all(self) -> tuple[MechanismResult, MechanismResult, MechanismResult]:
        """Solve and certify the three nested mechanism classes."""

        incumbent = self.optimize("incumbent_only")
        fixed = self.optimize("fixed_arrivals")
        expanded = self.optimize("expanded_search")
        fixed_as_expanded = self._solve(
            Policy(fixed.p1, fixed.p2, 1.0, regime="expanded_search")
        )
        expanded = self._certify(expanded, (fixed_as_expanded,))
        return incumbent, fixed, expanded


def mechanism_record(result: MechanismResult) -> dict[str, float | int | str | bool]:
    record = outcome_record(result.solution)
    record.update(
        {
            "mechanism": result.mechanism,
            "design_value": result.design_value,
            "completion_value": result.environment.completion_value,
            "search_cost": result.environment.search_cost,
            "search_cost_basis": result.environment.search_cost_basis,
            "search_resource": result.search_resource,
            "exploration_evaluations": result.exploration_evaluations,
            "certification_stable": result.certification_stable,
            "certification_grids": ",".join(
                str(grid) for grid in result.certification_grids
            ),
            "adversarial_seed_count": result.adversarial_seed_count,
            "adversarial_evaluations": result.adversarial_evaluations,
            "adversarial_improvement": result.adversarial_improvement,
        }
    )
    return record

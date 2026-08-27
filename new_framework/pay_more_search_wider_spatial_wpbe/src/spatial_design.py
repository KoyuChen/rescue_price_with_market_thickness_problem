"""Outer mechanism design over inner cutoff-WPBE outcomes.

For each environment theta=(m,beta,delta), the platform solves three nested
problems under conservative equilibrium selection:

    baseline:        max_p              W(p,p,1)
    fixed rescue:    max_{p1<=p2}       W(p1,p2,1)
    expanded search: max_{p1<=p2,s>=1} W(p1,p2,s).

Every objective evaluation calls ``solve_policy`` and therefore re-enumerates
the induced cutoff-WPBE correspondence.  No cutoff, rider continuation share,
or terminal supply outcome is fixed in the outer design.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np
from scipy.optimize import minimize_scalar

from spatial_wpbe import (
    Params,
    Policy,
    PolicySolution,
    outcome_record,
    solve_policy,
    solve_policy_certified,
)


Mechanism = Literal["baseline", "fixed_rescue", "expanded_search"]


@dataclass(frozen=True)
class Environment:
    m: float
    beta: float
    delta: float
    pickup_rate: float = 0.25
    incumbent_retention: float = 1.0

    def params(self) -> Params:
        return Params(
            self.m,
            self.beta,
            self.delta,
            self.pickup_rate,
            self.incumbent_retention,
        )


@dataclass(frozen=True)
class SearchConfig:
    s_bar: float = 2.5
    cutoff_grid: int = 81
    final_cutoff_grid: int = 1001
    p1_nodes: int = 13
    p1_refine_levels: int = 3
    inner_refine_levels: int = 3
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
        self._cache: dict[tuple[float, float, float], PolicySolution] = {}
        self._evaluation_count = 0

    @property
    def evaluation_count(self) -> int:
        return self._evaluation_count

    @staticmethod
    def _solution_key(solution: PolicySolution) -> tuple[float, float, float, float]:
        policy = solution.policy
        return (
            solution.selected.completion,
            -policy.s,
            -(policy.p2 - policy.p1),
            -policy.p1,
        )

    def _solve(self, policy: Policy) -> PolicySolution:
        key = (round(policy.p1, 10), round(policy.p2, 10), round(policy.s, 10))
        if key not in self._cache:
            self._cache[key] = solve_policy(
                policy,
                self.params,
                selection="conservative",
                grid_size=self.config.cutoff_grid,
                validate=True,
            )
            self._evaluation_count += 1
        return self._cache[key]

    def _policy(self, p1: float, price_unit: float, search_unit: float) -> Policy:
        p2 = p1 + price_unit * max(self.params.beta - p1, 0.0)
        search = 1.0 + search_unit * (self.config.s_bar - 1.0)
        return Policy(float(p1), float(p2), float(search))

    @staticmethod
    def _initial_grids(mechanism: Mechanism) -> tuple[list[float], list[float]]:
        price = [0.0, 0.05, 0.15, 0.30, 0.50, 0.75, 1.0]
        search = [0.0, 0.10, 0.30, 0.55, 0.80, 1.0]
        if mechanism == "baseline":
            return [0.0], [0.0]
        if mechanism == "fixed_rescue":
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
        if mechanism == "baseline" or p1 >= self.params.beta - 1e-12:
            return InnerResult(mechanism, p1, self._solve(Policy(p1, p1, 1.0)))

        price_grid, search_grid = self._initial_grids(mechanism)
        candidates: list[tuple[float, float, PolicySolution]] = []

        def add(price_unit: float, search_unit: float) -> None:
            solution = self._solve(self._policy(p1, price_unit, search_unit))
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

    def _inactive_branch(self) -> PolicySolution:
        """Optimize p1>=beta, where delayed service has zero positive mass."""

        lower = min(self.params.beta, 1.0)
        if lower >= 1.0 - 1e-12:
            return self._solve(Policy(1.0, 1.0, 1.0))
        optimum = minimize_scalar(
            lambda price: -self._solve(
                Policy(float(price), float(price), 1.0)
            ).selected.completion,
            bounds=(lower, 1.0),
            method="bounded",
            options={"xatol": 2e-6},
        )
        candidates = [
            self._solve(Policy(lower, lower, 1.0)),
            self._solve(Policy(float(optimum.x), float(optimum.x), 1.0)),
            self._solve(Policy(1.0, 1.0, 1.0)),
        ]
        return max(candidates, key=self._solution_key)

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
        candidates.append(self._inactive_branch())
        best_explored = max(candidates, key=self._solution_key)
        result = MechanismResult(
            mechanism=mechanism,
            environment=self.environment,
            solution=best_explored,
            profile=tuple(sorted(profile.values(), key=lambda item: item.p1)),
            exploration_evaluations=self.evaluation_count - starting_evaluations,
        )
        return self._certify(result)

    def _feasible(self, policy: Policy, mechanism: Mechanism) -> bool:
        if mechanism == "baseline":
            return abs(policy.p2 - policy.p1) <= 1e-10 and abs(policy.s - 1.0) <= 1e-10
        if mechanism == "fixed_rescue":
            return abs(policy.s - 1.0) <= 1e-10
        return policy.s <= self.config.s_bar + 1e-10

    def _certify(
        self,
        target: MechanismResult,
        injected: tuple[MechanismResult, ...] = (),
    ) -> MechanismResult:
        """Dense-grid WPBE validation and global candidate re-ranking."""

        explored = [
            solution
            for solution in self._cache.values()
            if self._feasible(solution.policy, target.mechanism)
        ]
        explored.sort(key=self._solution_key, reverse=True)
        candidates = [target.solution]
        candidates.extend(result.solution for result in injected)
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
            solve_policy(
                candidate.policy,
                self.params,
                selection="conservative",
                grid_size=self.config.final_cutoff_grid,
                validate=True,
            )
            for candidate in unique.values()
        ]
        dense.sort(key=self._solution_key, reverse=True)
        finalists = dense[: self.config.certify_finalists]
        certified = [
            solve_policy_certified(
                finalist.policy,
                self.params,
                selection="conservative",
                initial_grid=self.config.final_cutoff_grid,
                max_grid=self.config.certification_max_grid,
            )
            for finalist in finalists
        ]
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
        )

    def optimize_all(self) -> tuple[MechanismResult, MechanismResult, MechanismResult]:
        """Solve and certify the three nested mechanism classes."""

        baseline = self.optimize("baseline")
        fixed = self.optimize("fixed_rescue")
        fixed = self._certify(fixed, (baseline,))
        expanded = self.optimize("expanded_search")
        expanded = self._certify(expanded, (baseline, fixed))
        return baseline, fixed, expanded


def mechanism_record(result: MechanismResult) -> dict[str, float | int | str | bool]:
    record = outcome_record(result.solution)
    record.update(
        {
            "mechanism": result.mechanism,
            "exploration_evaluations": result.exploration_evaluations,
            "certification_stable": result.certification_stable,
            "certification_grids": ",".join(
                str(grid) for grid in result.certification_grids
            ),
        }
    )
    return record

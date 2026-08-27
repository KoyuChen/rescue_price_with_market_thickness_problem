from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.integrate import quad


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spatial_design import (  # noqa: E402
    Environment,
    SearchConfig,
    SpatialMechanismSolver,
)
from spatial_wpbe import (  # noqa: E402
    Params,
    Policy,
    cutoff_residual,
    extra_pickup_cost,
    fresh_accept_intensity,
    fresh_pickup_cost_intensity,
    is_cutoff_best_response,
    solve_policy,
    solve_policy_certified,
    solve_terminal_market,
    uniform_cdf,
)


class SpatialThinningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.params = Params(m=2.0, beta=0.8, delta=0.75, pickup_rate=0.25)

    def test_core_has_time_homogeneous_fresh_arrivals(self):
        self.assertAlmostEqual(
            fresh_accept_intensity(0.6, 1.0, self.params), 2.0 * 0.6
        )
        terminal = solve_terminal_market(
            0.25, 0.6, 1.0, self.params, "core_arrivals"
        )
        self.assertAlmostEqual(terminal.potential_fresh_intensity, 2.0)
        self.assertAlmostEqual(terminal.fresh_accept_intensity, 1.2)
        self.assertAlmostEqual(terminal.incumbent_intensity, 0.7)

    def test_incumbent_retention_scales_pool_and_waiting_option(self):
        retained = Params(
            m=2.0,
            beta=0.8,
            delta=0.75,
            pickup_rate=0.25,
            incumbent_retention=0.4,
        )
        terminal = solve_terminal_market(
            0.25, 0.6, 1.0, retained, "core_arrivals"
        )
        self.assertAlmostEqual(terminal.incumbent_intensity, 0.4 * 0.7)

        policy = Policy(0.30, 0.50, 1.0)
        full_residual = cutoff_residual(0.22, policy, self.params)
        retained_residual = cutoff_residual(0.22, policy, retained)
        self.assertGreater(retained_residual, full_residual)

    def test_incumbent_retention_must_be_a_probability(self):
        with self.assertRaises(ValueError):
            Params(2.0, 0.8, 0.75, 0.25, 1.01)

    def test_closed_form_matches_radial_quadrature(self):
        payment, reach = 0.6, 2.25
        radius = math.sqrt(reach)
        density_measure = 2.0 * self.params.m
        numerical = quad(
            lambda r: density_measure
            * r
            * uniform_cdf(
                payment - self.params.pickup_rate * max(r - 1.0, 0.0)
            ),
            0.0,
            radius,
            epsabs=1e-12,
        )[0]
        self.assertAlmostEqual(
            fresh_accept_intensity(payment, reach, self.params), numerical, places=10
        )

        pickup_numerical = quad(
            lambda r: density_measure
            * r
            * extra_pickup_cost(r * r, self.params.pickup_rate)
            * uniform_cdf(
                payment - extra_pickup_cost(r * r, self.params.pickup_rate)
            ),
            0.0,
            radius,
            epsabs=1e-12,
        )[0]
        self.assertAlmostEqual(
            fresh_pickup_cost_intensity(payment, reach, self.params),
            pickup_numerical,
            places=10,
        )

    def test_outer_annulus_is_incremental_poisson_thinning(self):
        payment = 0.55
        core = fresh_accept_intensity(payment, 1.0, self.params)
        expanded = fresh_accept_intensity(payment, 2.0, self.params)
        direct_outer = quad(
            lambda u: self.params.m
            * uniform_cdf(
                payment - extra_pickup_cost(u, self.params.pickup_rate)
            ),
            1.0,
            2.0,
            epsabs=1e-12,
        )[0]
        self.assertAlmostEqual(expanded - core, direct_outer, places=10)
        self.assertGreater(expanded, core)

    def test_winner_only_cost_saturates_search_response(self):
        payment = 0.4
        saturation = (1.0 + payment / self.params.pickup_rate) ** 2
        at_saturation = fresh_accept_intensity(payment, saturation, self.params)
        beyond = fresh_accept_intensity(payment, saturation * 4.0, self.params)
        self.assertAlmostEqual(at_saturation, beyond, places=10)

    def test_zero_pickup_rate_reduces_to_homogeneous_thinning(self):
        params = Params(m=1.7, beta=0.8, delta=0.8, pickup_rate=0.0)
        self.assertAlmostEqual(
            fresh_accept_intensity(0.42, 2.3, params), 1.7 * 2.3 * 0.42
        )


class InnerWPBETests(unittest.TestCase):
    def setUp(self) -> None:
        self.params = Params(m=2.0, beta=0.8, delta=0.8, pickup_rate=0.25)

    def test_three_regimes_have_the_intended_terminal_supply(self):
        incumbent = solve_policy(
            Policy(0.30, 0.50, 1.0, regime="incumbent_only"),
            self.params,
            grid_size=201,
            validate=True,
        ).selected
        fixed = solve_policy(
            Policy(0.30, 0.50, 1.0, regime="core_arrivals"),
            self.params,
            grid_size=201,
            validate=True,
        ).selected
        expanded = solve_policy(
            Policy(0.30, 0.50, 2.0, regime="expanded_search"),
            self.params,
            grid_size=201,
            validate=True,
        ).selected
        self.assertEqual(incumbent.rescue.fresh_accept_intensity, 0.0)
        self.assertEqual(incumbent.expected_notifications, 0.0)
        self.assertGreater(fixed.rescue.fresh_accept_intensity, 0.0)
        self.assertGreater(expanded.rescue.fresh_accept_intensity, 0.0)
        self.assertGreater(
            expanded.rescue.fresh_accept_intensity,
            fixed.rescue.fresh_accept_intensity,
        )

    def test_expanded_at_one_is_exactly_core_arrivals(self):
        fixed = solve_policy(
            Policy(0.30, 0.50, 1.0, regime="core_arrivals"),
            self.params,
            grid_size=301,
            validate=True,
        )
        expanded = solve_policy(
            Policy(0.30, 0.50, 1.0, regime="expanded_search"),
            self.params,
            grid_size=301,
            validate=True,
        )
        self.assertEqual(fixed.equilibrium_count, expanded.equilibrium_count)
        self.assertAlmostEqual(
            fixed.selected.cutoff, expanded.selected.cutoff, places=10
        )
        self.assertAlmostEqual(
            fixed.selected.completion, expanded.selected.completion, places=12
        )

    def test_zero_retention_eliminates_waiting_option(self):
        params = Params(
            m=2.0,
            beta=0.8,
            delta=0.8,
            pickup_rate=0.25,
            incumbent_retention=0.0,
        )
        outcome = solve_policy(
            Policy(0.30, 0.55, 1.0, regime="incumbent_only"),
            params,
            grid_size=301,
            validate=True,
        ).selected
        self.assertAlmostEqual(outcome.cutoff, 0.30, places=8)
        self.assertEqual(outcome.rescue.incumbent_intensity, 0.0)

    def test_every_returned_cutoff_is_a_full_best_response(self):
        solution = solve_policy(
            Policy(0.28, 0.53, 2.2, regime="expanded_search"),
            self.params,
            grid_size=401,
            validate=True,
        )
        self.assertGreaterEqual(solution.equilibrium_count, 1)
        for equilibrium in solution.equilibria:
            self.assertTrue(
                is_cutoff_best_response(
                    equilibrium.cutoff, solution.policy, self.params
                )
            )
            self.assertLess(abs(equilibrium.residual), 1e-7)

    def test_rider_terminal_actions_are_counterfactual_not_added(self):
        outcome = solve_policy(
            Policy(0.30, 0.50, 2.0, regime="expanded_search"),
            self.params,
            grid_size=201,
            validate=True,
        ).selected
        self.assertAlmostEqual(
            outcome.repeat_mass + outcome.rescue_mass + outcome.abandon_mass,
            1.0,
            places=10,
        )
        calculated = (
            outcome.first_completion
            + outcome.repeat_completion
            + outcome.rescue_completion
        )
        self.assertAlmostEqual(outcome.completion, calculated, places=12)

    def test_cutoff_correspondence_is_stable_under_grid_doubling(self):
        certificate = solve_policy_certified(
            Policy(0.28, 0.53, 2.2, regime="expanded_search"),
            self.params,
            initial_grid=101,
            max_grid=401,
        )
        self.assertTrue(certificate.stable)
        self.assertEqual(certificate.grids, (101, 201, 401))
        self.assertTrue(all(len(roots) >= 1 for roots in certificate.root_sets))


class OuterMechanismDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        environment = Environment(
            1.5,
            0.8,
            0.8,
            pickup_rate=0.25,
            incumbent_retention=0.8,
            outer_contact_cost=0.01,
        )
        config = SearchConfig(
            s_bar=2.0,
            cutoff_grid=51,
            final_cutoff_grid=301,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            certify_top_k=4,
        )
        cls.results = SpatialMechanismSolver(environment, config).optimize_all()

    def test_regimes_and_domains_are_distinct(self):
        incumbent, fixed, expanded = self.results
        self.assertEqual(incumbent.solution.policy.regime, "incumbent_only")
        self.assertAlmostEqual(incumbent.s, 1.0)
        self.assertEqual(fixed.solution.policy.regime, "core_arrivals")
        self.assertAlmostEqual(fixed.s, 1.0)
        self.assertGreaterEqual(fixed.p2 + 1e-12, fixed.p1)
        self.assertEqual(expanded.solution.policy.regime, "expanded_search")
        self.assertGreaterEqual(expanded.s + 1e-12, 1.0)
        self.assertGreaterEqual(expanded.p2 + 1e-12, expanded.p1)

    def test_only_fixed_and_expanded_values_are_nested(self):
        _, fixed, expanded = self.results
        self.assertGreaterEqual(expanded.design_value + 2e-8, fixed.design_value)

    def test_each_reported_policy_is_dense_wpbe_validated(self):
        for result in self.results:
            selected = result.solution.selected
            self.assertTrue(
                is_cutoff_best_response(
                    selected.cutoff, result.solution.policy, result.environment.params()
                )
            )
            self.assertLess(abs(selected.residual), 1e-7)

    def test_search_cap_one_collapses_expanded_to_fixed(self):
        environment = Environment(1.0, 0.8, 0.8, pickup_rate=0.25)
        config = SearchConfig(
            s_bar=1.0,
            cutoff_grid=41,
            final_cutoff_grid=201,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            certify_top_k=3,
            certify_finalists=2,
            certification_max_grid=801,
        )
        _, fixed, expanded = SpatialMechanismSolver(environment, config).optimize_all()
        self.assertAlmostEqual(fixed.completion, expanded.completion, places=8)
        self.assertAlmostEqual(fixed.design_value, expanded.design_value, places=8)
        self.assertAlmostEqual(expanded.s, 1.0, places=10)

    def test_high_outer_contact_cost_can_make_no_expansion_optimal(self):
        environment = Environment(
            4.0,
            0.8,
            0.8,
            pickup_rate=0.25,
            incumbent_retention=0.8,
            outer_contact_cost=1.0,
        )
        config = SearchConfig(
            s_bar=3.0,
            cutoff_grid=41,
            final_cutoff_grid=201,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            certify_top_k=3,
            certify_finalists=2,
            certification_max_grid=801,
        )
        _, fixed, expanded = SpatialMechanismSolver(
            environment, config
        ).optimize_all()
        self.assertAlmostEqual(expanded.s, 1.0, places=10)
        self.assertAlmostEqual(expanded.design_value, fixed.design_value, places=7)

    def test_adversarial_search_closes_known_m4_policy_gap(self):
        environment = Environment(
            4.0,
            0.8,
            0.8,
            pickup_rate=0.25,
            incumbent_retention=0.8,
            outer_contact_cost=0.0125,
        )
        config = SearchConfig(
            s_bar=4.0,
            cutoff_grid=61,
            final_cutoff_grid=401,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            adversarial_seeds=1,
            adversarial_maxiter=16,
            adversarial_popsize=8,
            certify_top_k=5,
            certify_finalists=2,
            certification_max_grid=1601,
        )
        solver = SpatialMechanismSolver(environment, config)
        expanded = solver.optimize("expanded_search")
        known_policy = solve_policy(
            Policy(
                0.167495,
                0.242734,
                2.51646,
                regime="expanded_search",
            ),
            environment.params(),
            grid_size=1601,
            validate=True,
        )
        known_value = min(
            environment.completion_value * equilibrium.completion
            - environment.outer_contact_cost
            * equilibrium.expected_extra_notifications
            for equilibrium in known_policy.equilibria
        )
        self.assertGreaterEqual(expanded.design_value + 2e-6, known_value)
        self.assertEqual(expanded.adversarial_seed_count, 1)

    def test_reported_search_never_exceeds_physical_willingness_support(self):
        environment = Environment(
            2.0, 0.8, 0.8, pickup_rate=0.25, outer_contact_cost=0.0
        )
        solver = SpatialMechanismSolver(
            environment,
            SearchConfig(
                s_bar=10.0,
                cutoff_grid=41,
                final_cutoff_grid=201,
                p1_nodes=7,
                p1_refine_levels=1,
                inner_refine_levels=1,
                certify_top_k=3,
                certify_finalists=2,
                certification_max_grid=801,
            ),
        )
        policy = solver._policy(0.2, 0.25, 1.0, "expanded_search")
        support = (1.0 + policy.p2 / environment.pickup_rate) ** 2
        self.assertAlmostEqual(policy.s, support, places=10)


if __name__ == "__main__":
    unittest.main()

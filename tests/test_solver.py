from dataclasses import replace
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rescue_solver import core as engine
from rescue_solver.storage import source_identity
from rescue_solver.solver import (Settings, ValueIntegratedEvaluator, poisson_states, solve_menu,
                    best_response, price_grid, grid_summary, complementarity_diagnostics)
from rescue_solver.cli import create_model, clean_json
from rescue_solver.core import FixedSupportRescueModel


def toy(one=False):
    if one:
        return FixedSupportRescueModel(engine.ModelParams(route_draws=10), np.array([.02]),
            np.array([1.]), np.array([1.]), np.array([1.]))
    return FixedSupportRescueModel(engine.ModelParams(route_draws=10), np.array([.02, .2]),
        np.array([.5, .5]), np.array([0., .5, .95]), np.array([.2, .3, .5]))


def initial(model, p1=.3, p2=.5):
    e, h, r = model._initial_profile(p1, p2)
    return engine.Profile(e, h, r, np.unique([p1, p2]),
        dict(early_share=float(np.sum(model.type_mass * e)),
             hidden_share=float(np.sum(model.type_mass * h)), max_regret=0.))


class SolverTests(unittest.TestCase):
    def test_poisson_enumeration_mass_and_vectors(self):
        states, weight, tail = poisson_states([.2, 0., .3], 4, 100)
        self.assertEqual(len(states), math.comb(6, 2))
        self.assertTrue(np.all(states[:, 1] == 0))
        for row, w in zip(states, weight):
            self.assertAlmostEqual(w, math.exp(-.5) * .2**row[0] / math.factorial(row[0]) *
                                   .3**row[2] / math.factorial(row[2]), places=14)
        self.assertAlmostEqual(tail, 1 - math.exp(-.5) * sum(.5**k / math.factorial(k) for k in range(5)), places=14)
        self.assertAlmostEqual(float(weight.sum()) + tail, 1., places=14)

    def test_poisson_zero_and_state_guard(self):
        c, w, t = poisson_states([0., 0.], 0, 10)
        np.testing.assert_array_equal(c, [[0, 0]])
        self.assertEqual(w[0], 1); self.assertEqual(t, 0)
        with self.assertRaises(ValueError): poisson_states(np.ones(22), 12, 50000)

    def test_value_envelope_against_dense_uniform_integration(self):
        model = toy(); p = initial(model)
        ev = ValueIntegratedEvaluator(model, Settings())
        _, old, new = model._belief_objects(2, .3, p.q_values, p.sigma_e, p.sigma_h, p.retain)
        for counts in ([0, 0, 0], [1, 0, 0], [0, 2, 0], [1, 1, 2]):
            length, _ = ev.value_intervals(np.array([counts]), .3, p.q_values, old, new)
            n = 50000; v = (np.arange(n) + .5) / n
            actions, _, _ = model._rider_action(np.tile(counts, (n, 1)), v, .3, p.q_values, old, new)
            for a in range(3):
                self.assertAlmostEqual(float(length[0, a].sum()), float(np.mean(actions == a)), delta=2/n)
            self.assertLessEqual(length.sum(), 1 + 1e-12)

    def test_tiny_positive_value_region_not_silently_dropped(self):
        model = toy(one=True); price = model.par.beta * (1 - 1e-8)
        p = initial(model, price, price); p.sigma_e[:] = 0; p.sigma_h[:] = .3; p.retain[:] = 0
        integrated = ValueIntegratedEvaluator(model, Settings(mode='enumerate')).evaluate(1, price, price, p, 50, 1)
        self.assertGreater(float(integrated['prob_q_base'][0]), 9e-9)
        legacy = model._evaluate_profile(1, price, price, p.sigma_e, p.sigma_h, p.retain, 50000, 1)
        self.assertEqual(float(legacy['prob_q_base'][0]), 0.)

    def test_integrated_payoffs_against_independent_legacy_iid(self):
        model = toy(); p = initial(model)
        integrated = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=10)).evaluate(1, .3, .5, p, 1, 9)
        legacy = model._evaluate_profile(1, .3, .5, p.sigma_e, p.sigma_h, p.retain, 120000, 812)
        for key in ('p_immediate', 'prob_q_base', 'prob_q_early', 'u_e', 'u_h'):
            np.testing.assert_allclose(integrated[key], legacy[key], atol=.004, rtol=0)
        positive = (integrated['prob_q_early'] > .02)
        np.testing.assert_allclose(integrated['pi_old'][positive], legacy['pi_old'][positive], atol=.01, rtol=0)

    def test_completion_against_explicit_market_simulation(self):
        model = toy(); p = initial(model)
        integrated = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=10)).evaluate(1, .3, .5, p, 1, 9)
        out, _, _ = model.paired_evaluate(1, (.3, .5, p), (.3, .5, p), 80000, 18, 5000)
        self.assertAlmostEqual(integrated['completion'], out['completion'], delta=5*out['completion_se'])

    def test_sample_reproducibility_and_enum_seed_independence(self):
        model = toy(); p = initial(model)
        ev = ValueIntegratedEvaluator(model, Settings(train_counts=128))
        a = ev.evaluate(1, .3, .5, p, 128, 29)
        b = ev.evaluate(1, .3, .5, p, 128, 29)
        np.testing.assert_array_equal(a['u_e'], b['u_e'])
        other = ev.evaluate(1, .3, .5, p, 128, 39)
        self.assertNotEqual(a['completion'], other['completion'])
        ev = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=5))
        a = ev.evaluate(1, .3, .5, p, 1, 19); b = ev.evaluate(1, .3, .5, p, 2, 31)
        np.testing.assert_array_equal(a['pi_old'], b['pi_old'])

    def test_unobserved_posterior_has_full_uncertainty(self):
        model = toy(); p = initial(model)
        ev = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=3)).evaluate(1, .3, .5, p, 1, 1)
        absent = ev['prob_q_early'] == 0
        self.assertTrue(absent.any())
        np.testing.assert_array_equal(ev['pi_old_low'][absent], 0)
        np.testing.assert_array_equal(ev['pi_old_high'][absent], 1)

    def test_count_tail_not_renormalized_and_audit_blocks(self):
        model = toy(); p = initial(model)
        evaluator = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=0))
        audit = evaluator.audit(6, .3, .5, p, 1, 1)
        self.assertGreater(audit['count_tail'], .1)
        self.assertFalse(audit['bounded_regret_check_pass'])
        self.assertFalse(audit['wpbe_certified'])

    def test_zero_temperature_stage_required(self):
        with self.assertRaises(ValueError): Settings(schedule=((.001, 10, .2),)).validate()

    def test_pure_response_and_feasibility(self):
        model = toy(); p = initial(model)
        ev = dict(u_e=np.full_like(model.a, .1), u_h=np.full_like(model.a, .2),
                  retain_advantage=np.zeros_like(p.retain))
        a, r = best_response(model, p, ev, 0, 0)
        np.testing.assert_array_equal(a[1], 1)
        np.testing.assert_array_equal(a.sum(axis=0), 1)

    def test_solver_nonconvergence_not_success(self):
        model = toy(); s = Settings(mode='enumerate', count_cap=5, schedule=((0., 1, .01),), regret_tol=1e-8)
        _, result = solve_menu(model, 1, .3, .5, s)
        self.assertEqual(result['status'], 'not_converged')
        self.assertFalse(result['numerical_checks_passed'])

    def test_zero_price_equilibrium_smoke(self):
        model = toy(); s = Settings(mode='enumerate', count_cap=5, schedule=((0., 50, .5),))
        profile, result = solve_menu(model, 1, 0., 0., s)
        self.assertTrue(result['numerical_checks_passed'])
        self.assertEqual(result['status'], 'numerical_checks_passed')
        self.assertEqual(float(profile.sigma_e.sum()), 0)
        self.assertEqual(float(profile.sigma_h.sum()), 0)
        self.assertFalse(result['wpbe_certified'])

    def test_diagonal_identical_profiles_have_identically_zero_gain(self):
        model = toy(); p = initial(model, .3, .3)
        r, f, _ = model.paired_evaluate(1, (.3, .3, p), (.3, .3, p), 4000, 27)
        self.assertEqual(r['completion'], f['completion'])

    def test_grid_includes_endpoints_and_does_not_discard_failed_leader(self):
        grid = price_grid(.25)
        self.assertEqual(grid, [0, .25, .5, .75, 1])
        menus = [(0, 0), (0, 1), (1, 1)]
        rows = [dict(m=1, p1=a, p2=b, numerical_checks_passed=i!=1,
                     selection_completion=[0., .2, 0.][i]) for i, (a, b) in enumerate(menus)]
        out = grid_summary(rows, menus)
        self.assertEqual(out['raw_rescue_leader_index'], 1)
        self.assertFalse(out['numerical_grid_comparison_ready'])
        self.assertTrue(out['full_requested_grid_evaluated'])
        self.assertFalse(grid_summary(rows[:2], menus)['full_requested_grid_evaluated'])

    def test_route_generation_random_but_reproducible(self):
        config = dict(model=dict(route_draws=10000))
        a = create_model(config, 71); b = create_model(config, 71); c = create_model(config, 72)
        np.testing.assert_array_equal(a.s, b.s); np.testing.assert_array_equal(a.fs, b.fs)
        self.assertFalse(np.array_equal(a.s, c.s))
        self.assertTrue(np.all((a.s >= 0) & (a.s <= 1)))
        self.assertAlmostEqual(float(a.fs.sum()), 1)
        self.assertGreater(len(a.s), 2)

    def test_source_identity_includes_core_and_solver(self):
        self.assertIn('core.py', source_identity()['source_sha256'])
        self.assertIn('solver.py', source_identity()['source_sha256'])

    def test_positive_trade_solution_in_toy_model(self):
        model = FixedSupportRescueModel(engine.ModelParams(route_draws=10), np.array([.5]),
            np.array([1.]), np.array([1.]), np.array([1.]))
        settings = Settings(mode='enumerate', schedule=((.003, 30, .4), (0., 80, .25)))
        profile, result = solve_menu(model, 1, .4, .7, settings)
        self.assertTrue(result['numerical_checks_passed'])
        self.assertGreater(profile.sigma_h[0, 0], .98)
        self.assertGreater(result['audits'][0]['completion'], .16)
        self.assertFalse(result['wpbe_certified'])

    def test_complementarity_detects_mixing_on_bad_action(self):
        model = toy(one=True); p = initial(model)
        p.sigma_e[:] = .5; p.sigma_h[:] = 0; p.retain[:] = .5
        ev = dict(u_e=np.full_like(model.a, .1), u_h=np.zeros_like(model.a),
                  retain_advantage=np.full_like(p.retain, -.02))
        out = complementarity_diagnostics(model, .3, p, ev)
        self.assertAlmostEqual(out['initial_complementarity_residual'], .05)
        self.assertAlmostEqual(out['retention_complementarity_residual'], .01)

    def test_invalid_poisson_inputs(self):
        for lam in ([], [-1.], [float('nan')], [[1.]]):
            with self.assertRaises(ValueError): poisson_states(lam, 2, 100)

    def test_json_undefined_statistic_is_null(self):
        self.assertEqual(clean_json({'mean': float('nan'), 'other': [float('inf')]}),
                         {'mean': None, 'other': [None]})

    def test_no_claim_of_price_rank_from_close_noisy_scores(self):
        rows = [dict(m=1, p1=p, p2=p, numerical_checks_passed=True,
                     selection_completion=.1+p*.0001, selection_markets=1000) for p in [0., 1.]]
        out = grid_summary(rows, [(0., 0.), (1., 1.)])
        self.assertTrue(out['numerical_grid_comparison_ready'])
        self.assertFalse(out['sampling_rank_separated'])
        self.assertFalse(out['grid_optimality_certified'])

    def test_count_batching_preserves_joint_probabilities(self):
        model = toy(); p = initial(model)
        small = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=7, count_batch_size=13))
        large = ValueIntegratedEvaluator(model, Settings(mode='enumerate', count_cap=7, count_batch_size=1000))
        a = small.evaluate(3, .3, .5, p, 1, 1); b = large.evaluate(3, .3, .5, p, 1, 1)
        for key in ('u_e', 'u_h', 'p_immediate', 'prob_q_early', 'pi_old', 'completion'):
            np.testing.assert_allclose(a[key], b[key], atol=2e-14, rtol=0)

    def test_small_weighted_regret_cannot_hide_large_support_gap(self):
        model = toy(one=True)
        profile = initial(model)
        profile.sigma_e[:] = .998; profile.sigma_h[:] = .002; profile.retain[:] = 0
        ev = dict(u_e=np.array([[.1]]), u_h=np.array([[0.]]),
            p_immediate=np.array([.1/(.3-.02)]), prob_q_early=np.zeros((1,2)),
            retain_advantage=np.full((2,1,1), -.004),
            pi_old_low=np.zeros((1,2)), pi_old_high=np.zeros((1,2)),
            count_tail=0., rate_error_radius=0., count_states=1,
            completion=0., zero_old_history_count=2)
        with patch.object(model, '_initial_profile', return_value=(profile.sigma_e, profile.sigma_h, profile.retain)), \
             patch.object(ValueIntegratedEvaluator, 'evaluate', return_value=ev):
            _, out = solve_menu(model, 1, .3, .5,
                Settings(mode='enumerate', schedule=((0.,1,.01),)))
        self.assertLess(out['training_regrets']['max_regret'], .00075)
        self.assertGreater(out['training_regrets']['initial_support_gap_max'], .0015)
        self.assertFalse(out['numerical_checks_passed'])
        self.assertFalse(out['audits'][0]['bounded_support_check_pass'])
        self.assertEqual(out['status'], 'not_converged')


if __name__ == '__main__':
    unittest.main()

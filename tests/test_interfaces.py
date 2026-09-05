from contextlib import redirect_stdout, redirect_stderr
from dataclasses import replace
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

from rescue_solver import ModelParams, FixedSupportRescueModel, Settings, RescueModel
from rescue_solver.core import draw_routes
from rescue_solver.config import load_config, build_model_params
from rescue_solver.cli import main
from rescue_solver.storage import atomic_write_json, digest
from rescue_solver.diagnostics import shape_diagnostics, thickness_diagnostics


def run(*args):
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return main(list(args))


class InterfaceTests(unittest.TestCase):
    def config(self, root):
        target = root / 'config.json'
        atomic_write_json(target, {'model': {'route_draws': 2000,
            'cost_probability_edges': [0, .1, .4, 1], 'route_positive_quantile_edges': [0, .5, 1]}})
        return target

    def menu(self, root):
        cfg = self.config(root)
        out = root / 'run'
        args = ['menu', '--m', '1', '--p1', '.3', '--p2', '.5', '--smoke',
                '--config', str(cfg), '--route-seed', '27', '--seed', '101',
                '--selection-markets', '200', '--report-markets', '200', '--output', str(out)]
        self.assertEqual(run(*args), 2)
        return args, out

    def test_invalid_model_parameters(self):
        cases = [{'beta': 0}, {'beta': 1.1}, {'delta': -1}, {'kappa': float('nan')},
                 {'route_draws': True}, {'route_draws': 0}, {'seed': -1},
                 {'driver_length_low': 0}, {'same_direction_probability': 2},
                 {'cost_probability_edges': [0, .5, .4, 1]}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                ModelParams(**case)

    def test_invalid_fixed_support(self):
        for s, weights in [([.9, .2], [.5, .5]), ([.2, .9], [.2, .3]),
                           ([.2, float('nan')], [.5, .5])]:
            with self.assertRaises(ValueError):
                FixedSupportRescueModel(ModelParams(), np.array([.1]), np.array([1.]),
                                        np.array(s), np.array(weights))

    def test_raw_route_draws_obey_overlap_formula_and_seeds(self):
        p = ModelParams(route_draws=1000)
        a, b = draw_routes(p, 1000, 1), draw_routes(p, 1000, 1)
        for key in a:
            np.testing.assert_array_equal(a[key], b[key])
        common = np.maximum(0., np.minimum(1., a['origin']+a['length'])-np.maximum(0., a['origin']))
        np.testing.assert_array_equal(a['overlap'], a['same_direction']*2*common/(1+a['length']))
        self.assertFalse(np.array_equal(a['overlap'], draw_routes(p, 1000, 2)['overlap']))

    def test_all_zero_route_distribution_is_supported(self):
        m = RescueModel(ModelParams(route_draws=1000, same_direction_probability=0))
        np.testing.assert_array_equal(m.s, [0.]); np.testing.assert_array_equal(m.fs, [1.])

    def test_unknown_configuration_and_hidden_budgets_rejected(self):
        with self.assertRaises(ValueError): build_model_params({'unknown': 5})
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'config.json'
            atomic_write_json(p, {'model': {}, 'solvers': {}})
            with self.assertRaises(ValueError): load_config(p)

    def test_invalid_solver_seed_and_boolean_budget_rejected(self):
        for s in (Settings(seed=-1), Settings(train_counts=True)):
            with self.assertRaises(ValueError): s.validate()

    def test_nonfinite_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'data.json'
            with self.assertRaises(ValueError): atomic_write_json(p, {'x': float('nan')})
            self.assertFalse(p.exists())

    def test_routes_cli_outputs_reproducible_raw_od(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ('a', 'b'):
                self.assertEqual(run('routes', '--route-seed', '41', '--route-draws', '200',
                                     '--output', str(root/name)), 0)
            with np.load(root/'a/routes.npz') as a, np.load(root/'b/routes.npz') as b:
                np.testing.assert_array_equal(a['overlap'], b['overlap'])
            with self.assertRaises(FileExistsError):
                run('routes', '--output', str(root/'a'))

    def test_resume_preserves_policy_and_rejects_changed_seed(self):
        with tempfile.TemporaryDirectory() as d:
            args, out = self.menu(Path(d))
            item = out/'thickness_000/menu_00000'
            before = digest(item/'profile.npz')
            self.assertEqual(run(*args, '--resume'), 2)
            self.assertEqual(digest(item/'profile.npz'), before)
            with self.assertRaises(ValueError): run(*args, '--resume', '--seed', '102')

    def test_resume_rejects_tampered_profile(self):
        with tempfile.TemporaryDirectory() as d:
            args, out = self.menu(Path(d))
            item = out/'thickness_000/menu_00000'
            # Controlled test corruption in a temporary directory only.
            (item/'profile.npz').write_bytes(b'corrupted test fixture')
            with self.assertRaises(ValueError): run(*args, '--resume')

    def test_independent_audit_does_not_change_policy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); _, out = self.menu(root)
            item = out/'thickness_000/menu_00000'
            before = digest(item/'profile.npz')
            self.assertEqual(run('audit', '--menu-dir', str(item), '--audit-seed', '8891',
                                 '--audit-counts', '300', '--output', str(root/'audit.json')), 2)
            self.assertEqual(digest(item/'profile.npz'), before)
            audit = json.loads((root/'audit.json').read_text())
            self.assertFalse(audit['changes_policy']); self.assertFalse(audit['wpbe_certified'])

    def test_audit_rejects_reused_training_seed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); _, out = self.menu(root)
            with self.assertRaises(ValueError):
                run('audit', '--menu-dir', str(out/'thickness_000/menu_00000'),
                    '--audit-seed', '101', '--output', str(root/'audit.json'))

    def test_grid_end_to_end_keeps_all_unresolved_and_raw_shape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); cfg = self.config(root); out = root/'grid'
            rc = run('grid', '--m', '1', '3', '6', '--step', '1', '--smoke',
                     '--config', str(cfg), '--route-seed', '27', '--selection-markets', '100',
                     '--report-markets', '100', '--output', str(out))
            self.assertEqual(rc, 2)
            summary = json.loads((out/'summary.json').read_text())
            self.assertEqual(len(list(out.glob('thickness_*/menu_*/result.json'))), 9)
            for row in summary['results']:
                self.assertTrue(row['full_requested_grid_evaluated'])
                self.assertFalse(row['grid_optimality_certified'])
            self.assertFalse(summary['shape_diagnostic']['inputs_equilibrium_certified'])

    def test_shape_does_not_clip_or_force_a_peak(self):
        r = shape_diagnostics([1, 3, 6, 12], [0, .02, -.01, .01], [.001]*4)
        self.assertFalse(r['raw_grid_weakly_single_peaked'])
        self.assertTrue(r['negative_values_preserved'])
        self.assertFalse(r['continuous_single_peak_proved'])

    def test_parallel_grid_preserves_fixed_design_results(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); cfg = self.config(root)
            results = []
            for workers in (1, 2):
                out = root / f'grid_{workers}'
                cmd = [sys.executable, '-m', 'rescue_solver', 'grid', '--m', '1', '3',
                    '--step', '1', '--smoke', '--config', str(cfg), '--route-seed', '27',
                    '--selection-markets', '100', '--report-markets', '100',
                    '--workers', str(workers), '--output', str(out)]
                env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
                proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
                self.assertEqual(proc.returncode, 2, proc.stderr)
                results.append(json.loads((out/'summary.json').read_text()))
            self.assertEqual(results[0], results[1])

    def test_price_order_and_middle_peak_are_tested_not_imposed(self):
        rows = [dict(m=m, p1=p1, p2=p2, p_flat=p, V_estimate=v,
                    comparison={'completion_gain_se': .001})
                for m, p1, p2, p, v in ((1, .4, .5, .6, -.01),
                    (3, .3, .5, .4, .03), (6, .35, .45, .4, .01))]
        result = thickness_diagnostics(rows)
        self.assertEqual(result['violating_price_order_m'], [1.])
        self.assertFalse(result['prices_weakly_decrease']['p1'])
        self.assertTrue(result['interior_peak_exceeds_both_endpoints_under_MC_only'])
        self.assertFalse(result['optimized_middle_peak_verified'])
        self.assertEqual(result['all_point_contrasts_family_size'], 3)

    def test_noisy_interior_peak_is_not_significant(self):
        rows = [dict(m=m, p1=.3, p2=.5, p_flat=.4, V_estimate=v,
                    comparison={'completion_gain_se': .01}) for m, v in ((1, .01), (3, .02), (6, .019))]
        result = thickness_diagnostics(rows)
        self.assertTrue(result['observed_peak_is_interior'])
        self.assertFalse(result['interior_peak_exceeds_both_endpoints_under_MC_only'])


if __name__ == '__main__':
    unittest.main()

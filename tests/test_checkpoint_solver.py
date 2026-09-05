import tempfile
import unittest
from pathlib import Path
import numpy as np
from rescue_solver.core import FixedSupportRescueModel, ModelParams
from rescue_solver.solver import Settings
from rescue_solver.cli import clean_json
from research_solver.high_precision import solve_high
from checkpoint_solver import solve_checkpointed


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.model = FixedSupportRescueModel(ModelParams(route_draws=10),
            np.array([.1, .4]), np.array([.5, .5]), np.array([0., 1.]), np.array([.3, .7]))
        self.settings = Settings(train_counts=80, audit_counts=200,
            schedule=((.02, 2, .35), (.004, 2, .25), (0., 3, .1)))

    def test_interruptions_match_original(self):
        for stop in ('iteration', 'temperature_finished', 'audit_finished'):
            with self.subTest(stop=stop), tempfile.TemporaryDirectory() as d:
                expected, result = solve_high(self.model, 3, .3, .5, self.settings)
                def interrupt(row):
                    if row['stage'] == stop: raise RuntimeError('simulated interruption')
                path = Path(d)/'state.npz'
                with self.assertRaisesRegex(RuntimeError, 'simulated'):
                    solve_checkpointed(self.model, 3, .3, .5, self.settings, path, {}, interrupt)
                actual, resumed = solve_checkpointed(self.model, 3, .3, .5, self.settings, path, {})
                for field in ('sigma_e', 'sigma_h', 'retain', 'q_values'):
                    np.testing.assert_array_equal(getattr(expected, field), getattr(actual, field))
                self.assertEqual(clean_json(result), clean_json(resumed))

    def test_changed_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'state.npz'
            solve_checkpointed(self.model, 3, .3, .5, self.settings, path, {'v': 1})
            with self.assertRaisesRegex(ValueError, 'fingerprint'):
                solve_checkpointed(self.model, 3, .3, .5, self.settings, path, {'v': 2})


if __name__ == '__main__': unittest.main()

from itertools import product
import unittest
import tempfile
from pathlib import Path
import numpy as np
from rescue_solver.core import ModelParams, FixedSupportRescueModel
from rescue_solver.solver import Settings
from research_solver.evaluator import JointPayoffEvaluator
from zero_retention_envelope import zero_retention_certificates
from zero_retention_checkpoint_solver import solve_checkpointed
from rescue_solver.cli import clean_json


class ZeroRetentionTests(unittest.TestCase):
    def setUp(self):
        self.model = FixedSupportRescueModel(ModelParams(route_draws=10),
            np.array([.1,.4]), np.array([.5,.5]),
            np.array([0.,.3,.9]), np.array([.4,.3,.3]))
        self.q = np.array([.15,.20])
        self.old = np.array([[.4,.2,0.], [0.,0.,0.]])
        self.new = np.array([[.03,.08,.25], [.03,.08,.25]])

    def test_all_counts_against_independent_original_integrator(self):
        proof, records = zero_retention_certificates(self.model,.15,self.q,self.old,self.new)
        self.assertTrue(proof[:,1].all(), records)
        counts = np.array(list(product(range(5), repeat=3)))
        counts = np.concatenate([counts, np.array([[50,200,7],[0,0,1000]])])
        evaluator = JointPayoffEvaluator(self.model,Settings())
        for s,iq in np.argwhere(proof):
            tagged = counts.copy(); tagged[:,s] += 1
            lengths,_ = evaluator.value_intervals(tagged,.15,self.q,self.old,self.new)
            self.assertLess(float(lengths[:,iq+1,:].max()),1e-11)

    def test_arbitrarily_small_positive_retention_is_not_ignored(self):
        for s in range(3):
            old = self.old.copy(); old[1,s] = 1e-250
            proof,_ = zero_retention_certificates(self.model,.15,self.q,old,self.new)
            self.assertFalse(proof.any())

    def test_profitable_high_continuation_is_not_excluded(self):
        new = np.zeros_like(self.new); new[1,-1] = 20.
        proof,_ = zero_retention_certificates(self.model,.15,self.q,self.old,new)
        self.assertFalse(proof[0,1])

    def test_flat_menu_has_no_added_certificate(self):
        proof,records = zero_retention_certificates(self.model,.15,self.q[:1],self.old[:1],self.new[:1])
        self.assertFalse(proof.any()); self.assertEqual(records,[])

    def test_new_solver_restart_and_source_guard(self):
        settings = Settings(train_counts=50,audit_counts=100,
            schedule=((.02,2,.35),(0.,3,.1)))
        with tempfile.TemporaryDirectory() as d:
            expected,result = solve_checkpointed(self.model,1,.15,.20,settings,Path(d)/'full.npz',{})
            for stage in ('iteration','temperature_finished','audit_finished'):
                path = Path(d)/(stage+'.npz')
                def interrupt(row):
                    if row['stage'] == stage: raise RuntimeError('interrupt')
                with self.assertRaisesRegex(RuntimeError,'interrupt'):
                    solve_checkpointed(self.model,1,.15,.20,settings,path,{},interrupt)
                actual,resumed = solve_checkpointed(self.model,1,.15,.20,settings,path,{})
                for field in ('sigma_e','sigma_h','retain','q_values'):
                    np.testing.assert_array_equal(getattr(expected,field),getattr(actual,field))
                self.assertEqual(clean_json(result),clean_json(resumed))
                with self.assertRaisesRegex(ValueError,'fingerprint'):
                    solve_checkpointed(self.model,1,.15,.20,settings,path,{'changed':True})


if __name__ == '__main__': unittest.main()

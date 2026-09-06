import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import numpy as np
import test_rare_history_enumeration as fixtures
from rare_history_evaluator import RareHistoryEvaluator,interval_retention_bounds
from rare_history_checkpoint_solver import solve_checkpointed
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator
from rescue_solver.solver import Settings
from rescue_solver.cli import clean_json


class RareEvaluatorTests(unittest.TestCase):
    def setUp(self):
        f=fixtures.RareHistoryEnumerationTests();f.setUp()
        self.model=f.model;self.profile=f.profile

    def test_interval_encloses_all_retention_choices_and_margin_signs(self):
        r=np.array([0.,.25,.5,.75,1.]);margin=np.array([-.1,0.,.1,.3,-.3])
        upper,support=interval_retention_bounds(r,margin,.004,.2,.4)
        for pi in np.linspace(.2,.4,101):
            advantage=pi*margin-.004
            actual=np.maximum((1-r)*np.maximum(advantage,0),r*np.maximum(-advantage,0))
            np.testing.assert_array_less(actual-1e-14,upper)
            actual_support=np.maximum(np.where(r<.999,np.maximum(advantage,0),0),
                                      np.where(r>.001,np.maximum(-advantage,0),0))
            np.testing.assert_array_less(actual_support-1e-14,support)

    def test_no_resolution_preserves_original_audit(self):
        settings=Settings(train_counts=50,audit_counts=100)
        old=ZeroRetentionEnvelopeEvaluator(self.model,settings)
        new=RareHistoryEvaluator(self.model,settings)
        def unresolved(*a):return {'resolved':False}
        with patch.object(new,'_resolve_rare',side_effect=unresolved):
            a=old.audit(1.,.15,.25,self.profile,100,73)
            b=new.audit(1.,.15,.25,self.profile,100,73)
        for key in ('full_plan_regret_upper','initial_support_gap_upper',
                    'retention_regret_upper','retention_support_gap_upper',
                    'max_regret_upper','bounded_checks_pass','unresolved_histories'):
            self.assertEqual(a[key],b[key],key)

    def test_bounded_positive_history_is_not_marked_offpath(self):
        new=RareHistoryEvaluator(self.model,Settings())
        ev=ZeroRetentionEnvelopeEvaluator(self.model,Settings()).evaluate(1.,.15,.25,self.profile,50,73)
        ev['offpath_certified'][0,1]=False;ev['unknown_old_history'][0,1]=True
        record=dict(resolved=True,kind='bounded_posterior',route_index=0,price_index=1,
                    posterior={'conditional_win_probability_estimate':.3})
        new._apply_rare_record(ev,self.profile,.15,record)
        self.assertFalse(ev['offpath_certified'][0,1]);self.assertFalse(ev['unknown_old_history'][0,1])
        np.testing.assert_allclose(ev['retain_advantage'][1,:,0],
            .3*(self.model.par.delta*.15-self.model.a[:,0])-self.model.par.omega_old)

    def test_restart_exact_policy_and_source_guard(self):
        settings=Settings(train_counts=50,audit_counts=100,schedule=((.02,2,.35),(0.,3,.1)))
        with tempfile.TemporaryDirectory() as d:
            expected,result=solve_checkpointed(self.model,1,.15,.25,settings,Path(d)/'full.npz',{})
            for stage in ('iteration','temperature_finished','audit_finished'):
                path=Path(d)/(stage+'.npz')
                def interrupt(row):
                    if row['stage']==stage:raise RuntimeError('interrupt')
                with self.assertRaisesRegex(RuntimeError,'interrupt'):
                    solve_checkpointed(self.model,1,.15,.25,settings,path,{},interrupt)
                actual,resumed=solve_checkpointed(self.model,1,.15,.25,settings,path,{})
                for field in ('sigma_e','sigma_h','retain','q_values'):
                    np.testing.assert_array_equal(getattr(expected,field),getattr(actual,field))
                self.assertEqual(clean_json(result),clean_json(resumed))
                with self.assertRaisesRegex(ValueError,'fingerprint'):
                    solve_checkpointed(self.model,1,.15,.25,settings,path,{'changed':True})

    def test_audit_uses_whole_interval_and_preserves_other_failures(self):
        model=SimpleNamespace(C=2,S=1,a=np.array([[.1],[.2]]),
            par=SimpleNamespace(delta=1.,omega_old=.004),
            _belief_objects=lambda *a:(None,None,np.zeros((1,1))))
        evaluator=RareHistoryEvaluator(model,Settings())
        profile=SimpleNamespace(q_values=np.array([.3]),retain=np.ones((1,2,1)),
                                sigma_e=None,sigma_h=None)
        record=dict(route_index=0,price_index=0,kind='bounded_posterior',resolved=True,
            posterior=dict(conditional_win_probability_lower=.3,
                           conditional_win_probability_upper=.4,
                           conditional_win_probability_estimate=.35))
        evaluator._rare_records={(0,0):record}
        evaluator.latest_rare_evaluation=dict(offpath_certified=np.zeros((1,1),bool),
            unknown_old_history=np.ones((1,1),bool),pi_old=np.zeros((1,1)),
            pi_old_report=[[None]],retain_advantage=np.zeros((1,2,1)),
            zero_retention_envelope_certificates=[])
        conditional=[dict(mean=np.zeros((1,2)),covariance=np.zeros((1,2,2)),
                          log_probability_factor=0.,count_states=1)]
        def base(*a):return dict(offpath_certified=[[False]],full_plan_regret_upper=.01,
            initial_support_gap_upper=.02,retention_regret_upper=99.)
        with patch('research_solver.evaluator.JointPayoffEvaluator.audit',side_effect=base), \
             patch('research_solver.posterior.old_win_zero_certificates',return_value=np.zeros((1,1),bool)), \
             patch('research_solver.conditional.old_conditional_moments',return_value=conditional):
            result=evaluator.audit(1.,.3,.3,profile,100,3)
            self.assertEqual(result['unresolved_histories'],[])
            self.assertEqual(result['retention_regret_upper'],0.)
            self.assertFalse(result['bounded_checks_pass'])
            self.assertEqual(result['full_plan_regret_upper'],.01)
            profile.retain[:]=0.
            result=evaluator.audit(1.,.3,.3,profile,100,3)
            self.assertAlmostEqual(result['retention_regret_upper'],.076)
            self.assertAlmostEqual(result['retention_support_gap_upper'],.076)

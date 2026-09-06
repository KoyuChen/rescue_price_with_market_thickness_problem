import math
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from bounded_rare_posterior import _poisson_total_tail,compressed_old_posterior
from rare_posterior_evaluator import RarePosteriorEvaluator,retention_interval_bounds
from strict_multi_route_envelope import _threshold_check,multi_route_count_exclusion
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator
from rescue_solver.core import ModelParams,Profile
from rescue_solver.solver import Settings,poisson_states


class RarePosteriorIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.model=VectorizedTieModel(ModelParams(route_draws=10),
            np.array([.01,.1,.3]),np.array([.3,.4,.3]),
            np.array([0.,.3,.9]),np.array([.4,.3,.3]))
        self.profile=Profile(np.full((3,3),.2),np.full((3,3),.2),
            np.zeros((2,3,3)),np.array([.15,.25]),{})
        self.profile.retain[:,0,0]=.5
        self.evaluator=RarePosteriorEvaluator(self.model,Settings(count_batch_size=32))

    def test_interval_retention_bounds_cover_both_margin_signs(self):
        low=np.full((3,2),.1);high=np.full((3,2),.8)
        self.profile.retain[:]=.4
        regret,support=retention_interval_bounds(self.model,.15,self.profile,low,high)
        for pi in np.linspace(.1,.8,21):
            adv=pi*(self.model.par.delta*.15-self.model.a)-self.model.par.omega_old
            r=self.profile.retain
            self.assertTrue(np.all(np.maximum(adv,0)-r*adv<=regret+1e-15))
            self.assertTrue(np.all(abs(adv)<=support+1e-15))

    def test_tail_bound_below_mean_cannot_claim_tiny_probability(self):
        self.assertEqual(_poisson_total_tail(100.,2),1.)
        self.assertGreater(_poisson_total_tail(.012,18),0.)
        from scipy.stats import poisson
        for mean,cap in [(1.,1),(.012,18),(.15,12),(20.,25)]:
            self.assertGreaterEqual(_poisson_total_tail(mean,cap),poisson.sf(cap,mean)*(1-1e-12))

    def test_budget_exhaustion_is_not_a_zero_history_certificate(self):
        with self.assertRaisesRegex(ValueError,'budget'):
            compressed_old_posterior(self.evaluator,1.,.15,self.profile,1,0,30,max_states=1)

    def test_compressed_joint_measures_match_full_enumeration(self):
        m=.4;p1=.15;iq=1;tag=0;cap=8
        model=self.model;profile=self.profile
        row=compressed_old_posterior(self.evaluator,m,p1,profile,iq,tag,cap)
        lam,old,new=model._belief_objects(m,p1,profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain)
        counts,weight,tail=poisson_states(lam,cap,10000)
        tagged=counts.copy();tagged[:,tag]+=1
        lengths,mid=self.evaluator.value_intervals(tagged,p1,profile.q_values,old,new)
        den=weight@lengths[:,iq+1,:].sum(axis=1)
        share=model._tag_selection_probability(counts,np.ones(len(counts)),p1,.25,float(model.s[tag]),'old',old[iq],new[iq])
        acceptable=model.par.beta*mid-(p1+model.beta_detour[tag])>1e-12
        num=weight@(share*(lengths[:,iq+1,:]@acceptable))
        factor=row['conditioned_zero_probability_factor']
        for actual,key in [(den,'conditional_event_measure'),(num,'tagged_win_measure')]:
            self.assertLessEqual(actual,row[key+'_upper']*factor+1e-14)
            self.assertGreaterEqual(actual+tail+1e-14,row[key+'_lower']*factor)

    def test_zero_coordinate_does_not_invent_better_immediate_route(self):
        old=np.array([[.9,.9,0.],[.2,.3,0.]])
        new=np.zeros((2,3));new[0,2]=2.
        a=_threshold_check(self.model,.15,np.array([.15,.8]),old,new,0,0,0,0,1)
        b=_threshold_check(self.model,.15,np.array([.15,.8]),old,new,0,1,0,0,1)
        self.assertEqual(a['passed'],b['passed'])
        self.assertAlmostEqual(a['minimum_active_margin'],b['minimum_active_margin'])

    def test_positive_short_interval_is_never_declared_offpath(self):
        model=self.model;ev=self.evaluator
        old=np.array([[.9,.9,0.],[.2,.3,0.]])
        new=np.zeros((2,3));new[0,2]=2.
        def threshold(*args,**kwargs):return dict(passed=True) if args[7]==1 else dict(passed=False)
        def intervals(*args,**kwargs):
            x=np.zeros((1,3,1));x[0,2,0]=1e-14;return x,np.array([.5])
        with patch('strict_multi_route_envelope._threshold_check',side_effect=threshold),patch.object(ev,'value_intervals',side_effect=intervals):
            result=multi_route_count_exclusion(ev,.15,np.array([.15,.8]),old,new,0,0,1)
        self.assertFalse(result['passed'])

    def test_flat_menu_matches_original_audit(self):
        e,h,r=self.model._initial_profile(.4,.4)
        profile=Profile(e,h,r,np.array([.4]),{})
        settings=Settings(count_batch_size=32)
        a=ZeroRetentionEnvelopeEvaluator(self.model,settings).audit(1.,.4,.4,profile,200,901)
        b=RarePosteriorEvaluator(self.model,settings).audit(1.,.4,.4,profile,200,901)
        for k in ['full_plan_regret_upper','initial_support_gap_upper','retention_regret_upper','retention_support_gap_upper']:
            self.assertAlmostEqual(a[k],b[k],places=12)
        self.assertEqual(a['bounded_checks_pass'],b['bounded_checks_pass'])

    def test_posterior_cache_invalidates_when_profile_beliefs_change(self):
        ev=self.evaluator.evaluate(1.,.15,.25,self.profile,30,17)
        self.evaluator._posterior(1.,.15,self.profile,0,1,ev)
        key=self.evaluator._posterior_key
        self.profile.sigma_h*=.9
        ev=self.evaluator.evaluate(1.,.15,.25,self.profile,30,17)
        self.evaluator._posterior(1.,.15,self.profile,0,1,ev)
        self.assertNotEqual(key,self.evaluator._posterior_key)

    def test_onpath_interval_updates_policy_without_offpath_belief(self):
        ev=ZeroRetentionEnvelopeEvaluator(self.model,Settings()).evaluate(1.,.15,.25,self.profile,30,17)
        ev['offpath_certified'][1,1]=False;ev['old_win_certified_zero'][1,1]=False
        ev['unknown_old_history'][1,1]=True;ev['prob_q_early'][1,1]=0.
        row=dict(resolved=True,structurally_off_path=False,price_index=1,tag_route=1,
            conditional_win_probability_lower=.3,conditional_win_probability_upper=.3000000001,
            conditional_win_probability_estimate=.3,conditioned_zero_probability_factor=.5,
            conditional_event_measure_lower=1e-20,tagged_win_measure_lower=3e-21)
        with patch.object(ZeroRetentionEnvelopeEvaluator,'evaluate',return_value=ev),patch.object(self.evaluator,'_posterior',return_value=row):
            result=self.evaluator.evaluate(1.,.15,.25,self.profile,30,17)
        self.assertFalse(result['offpath_certified'][1,1])
        self.assertFalse(result['unknown_old_history'][1,1])
        self.assertAlmostEqual(result['prob_q_early'][1,1],5e-21,places=30)
        np.testing.assert_allclose(result['retain_advantage'][1,:,1],
            .3*(self.model.par.delta*.15-self.model.a[:,1])-self.model.par.omega_old)
        self.assertEqual(result['rare_posterior_records'][0]['price_index'],1)

    def test_restart_recovers_identical_training_and_audits(self):
        from rare_posterior_checkpoint_solver import solve_checkpointed
        settings=Settings(train_counts=30,audit_counts=50,count_batch_size=32,
            schedule=((.004,2,.25),(0.,3,.1)))
        with tempfile.TemporaryDirectory() as d:
            a,ra=solve_checkpointed(self.model,1.,.4,.4,settings,Path(d)/'full.npz',{})
            class Interrupted(Exception):pass
            def stop(row):
                if row.get('stage')=='iteration':raise Interrupted()
            with self.assertRaises(Interrupted):
                solve_checkpointed(self.model,1.,.4,.4,settings,Path(d)/'resume.npz',{},stop)
            b,rb=solve_checkpointed(self.model,1.,.4,.4,settings,Path(d)/'resume.npz',{})
            for k in ['sigma_e','sigma_h','retain']:np.testing.assert_array_equal(getattr(a,k),getattr(b,k))
            self.assertEqual(ra['audits'],rb['audits'])
            with self.assertRaisesRegex(ValueError,'fingerprint'):
                solve_checkpointed(self.model,1.,.4,.4,settings,Path(d)/'resume.npz',{'changed':True})


if __name__=='__main__':unittest.main()

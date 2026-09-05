from dataclasses import replace
import unittest
import numpy as np
from rescue_solver.core import ModelParams, FixedSupportRescueModel, Profile
from rescue_solver.solver import Settings, ValueIntegratedEvaluator
from research_solver.evaluator import JointPayoffEvaluator, offpath_certificates, bernstein_radius
from research_solver.solve import solve, polish_support
from research_solver.analytic import all_early_profile, no_hidden_completion
from research_solver.posterior import supported_hidden_offpath, old_win_zero_certificates
from research_solver.conditional import old_conditional_moments
from research_solver.supported import SupportedHistoryEvaluator
from research_solver.certified import CertifiedPayoffEvaluator
from research_solver.types import lift_profile


def toy():
    return FixedSupportRescueModel(ModelParams(route_draws=10), np.array([.02, .2]),
        np.array([.5, .5]), np.array([0., .5, .95]), np.array([.2, .3, .5]))


def initial(model, p1=.3, p2=.5):
    e,h,r=model._initial_profile(p1,p2)
    return Profile(e,h,r,np.unique([p1,p2]),{})


class ResearchTests(unittest.TestCase):
    def test_feature_mean_matches_original_integrator(self):
        model=toy(); profile=initial(model)
        settings=Settings(mode='enumerate',count_cap=6)
        old=ValueIntegratedEvaluator(model,settings).evaluate(1,.3,.5,profile,10,91)
        new=JointPayoffEvaluator(model,settings).evaluate(1,.3,.5,profile,10,91)
        for key in ('p_immediate','prob_q_early','u_e','u_h','completion','old_joint'):
            np.testing.assert_allclose(new[key],old[key],atol=1e-13,rtol=0)

    def test_offpath_certificate_is_not_zero_sample_inference(self):
        model=toy(); q=np.array([.3,.5]); new=np.ones((2,3))*.01
        proof=offpath_certificates(model,.3,q,new)
        self.assertFalse(proof[0,0]); self.assertTrue(proof[-1,1])
        self.assertTrue(offpath_certificates(model,.3,q,new*0).all())
        profile=initial(model)
        ev=JointPayoffEvaluator(model,Settings()).evaluate(1,.3,.5,profile,1,12)
        for s,q in np.argwhere(ev['unknown_old_history']):
            self.assertIsNone(ev['pi_old_report'][s][q])

    def test_no_hidden_flat_belief_has_no_fake_half_win(self):
        model=toy(); p=initial(model,.4,.4)
        p.sigma_e[:]=model.a<=.4; p.sigma_h[:]=0; p.retain[:]=0
        ev=JointPayoffEvaluator(model,Settings()).evaluate(1,.4,.4,p,100,12)
        self.assertTrue(ev['offpath_certified'].all())
        np.testing.assert_array_equal(ev['pi_old'],0)
        np.testing.assert_array_equal(ev['retain_advantage'],-model.par.omega_old)
        self.assertEqual(ev['unknown_feasible_history_count'],0)

    def test_multiplicity_covariance_equals_unmerged(self):
        model=toy(); p=initial(model); evaluator=JointPayoffEvaluator(model,Settings())
        n=12; lam,old,new=model._belief_objects(1,.3,p.q_values,p.sigma_e,p.sigma_h,p.retain)
        counts=np.random.default_rng(41).poisson(lam,size=(n,model.S))
        evaluator.collect_moments=True
        evaluator.first=np.zeros((model.S,7)); evaluator.second=np.zeros((model.S,7,7))
        evaluator._weighted_rates(counts,np.ones(n)/n,.3,p,old,new)
        a,b=evaluator.first.copy(),evaluator.second.copy()
        c,mult=np.unique(counts,axis=0,return_counts=True)
        evaluator.first[:]=0; evaluator.second[:]=0
        evaluator._weighted_rates(c,mult/n,.3,p,old,new)
        np.testing.assert_allclose(evaluator.first,a,atol=1e-15)
        np.testing.assert_allclose(evaluator.second,b,atol=1e-15)

    def test_bernstein_zero_width_and_variance(self):
        self.assertEqual(bernstein_radius(0,0,100,10),0)
        self.assertAlmostEqual(bernstein_radius(0,1,100,10),70/297)
        with self.assertRaises(ValueError): bernstein_radius(0,1,1,10)

    def test_exact_flat_branch_passes_and_bad_retention_fails(self):
        model=toy(); p=initial(model,.4,.4)
        p.sigma_e[:]=model.a<=.4; p.sigma_h[:]=0; p.retain[:]=0
        evaluator=JointPayoffEvaluator(model,Settings())
        audit=evaluator.audit(1,.4,.4,p,100000,12)
        self.assertTrue(audit['bounded_checks_pass'],audit)
        self.assertFalse(audit['wpbe_certified'])
        p.retain[:]=1
        audit=evaluator.audit(1,.4,.4,p,100000,12)
        self.assertFalse(audit['bounded_checks_pass'])
        self.assertAlmostEqual(audit['retention_regret_upper'],model.par.omega_old)

    def test_audit_catches_profitable_hidden_deviation(self):
        model=toy(); p=initial(model)
        p.sigma_e[:]=0; p.sigma_h[:]=.9; p.retain[:]=0
        audit=JointPayoffEvaluator(model,Settings()).audit(1,.3,.5,p,10000,92)
        self.assertFalse(audit['bounded_checks_pass'])
        self.assertGreater(audit['full_plan_regret_upper'],.001)

    def test_projection_removes_only_tiny_strictly_inferior_mass(self):
        model=toy(); p=initial(model)
        p.sigma_e[:]=.9; p.sigma_h[:]=.00001
        ev=dict(u_e=np.ones_like(model.a)*.1,u_h=np.ones_like(model.a)*-.005,
                retain_advantage=np.ones_like(p.retain)*-.004)
        polish_support(model,p,ev)
        np.testing.assert_array_equal(p.sigma_h,0)
        self.assertTrue(np.all(p.sigma_e<1))

    def test_zero_price_solve(self):
        model=toy(); settings=Settings(train_counts=100,audit_counts=1000,
            schedule=((.001,10,.5),(0.,40,.5)))
        _,result=solve(model,1,0.,0.,settings)
        self.assertTrue(result['numerical_checks_passed'],result)

    def test_independent_analytic_branch_matches_integrator(self):
        model=toy(); p=all_early_profile(model,.4,.6)
        settings=Settings(mode='enumerate',count_cap=12)
        ev=JointPayoffEvaluator(model,settings).evaluate(1,.4,.6,p,10,19)
        self.assertAlmostEqual(ev['completion'],no_hidden_completion(model,1,.4),places=10)
        self.assertAlmostEqual(ev['prob_q_base'].sum(),0,places=12)

    def test_continuous_cost_one_route_closed_form(self):
        model=FixedSupportRescueModel(ModelParams(route_draws=10),np.array([.5]),
                                     np.array([1.]),np.array([1.]),np.array([1.]))
        self.assertAlmostEqual(no_hidden_completion(model,3,.4,True),.6*(1-np.exp(-1.2)))

    def test_actual_hidden_support_proof_is_stronger_but_not_probability_cutoff(self):
        model=toy(); q=np.array([.3,.5]); new=np.zeros((2,3)); new[:,0]=.1
        proof=supported_hidden_offpath(model,.3,q,new)
        self.assertTrue(proof.all())
        new[0,-1]=1e-250
        self.assertFalse(supported_hidden_offpath(model,.3,q,new)[0,0])

    def test_hidden_support_proof_matches_all_toy_counts(self):
        model=toy(); q=np.array([.3,.5]); new=np.zeros((2,3)); new[:,0]=.1
        r=np.full((2,3),.5)
        from itertools import product
        counts=np.array(list(product(range(4),repeat=3)))
        evaluator=JointPayoffEvaluator(model,Settings())
        for s in range(3):
            tagged=counts.copy();tagged[:,s]+=1
            lengths,_=evaluator.value_intervals(tagged,.3,q,r,new)
            np.testing.assert_allclose(lengths[:,1:,:],0,atol=1e-12)

    def test_conditional_moments_recover_unconditional_joint_rates(self):
        model=toy();p=initial(model)
        evaluator=JointPayoffEvaluator(model,Settings(mode='enumerate',count_cap=12))
        exact=evaluator.evaluate(1,.3,.5,p,2,0)
        conditional=old_conditional_moments(evaluator,1,.3,p,100000,913)
        for iq,row in enumerate(conditional):
            np.testing.assert_allclose(row['mean'][:,0]*row['probability_factor'],
                                       exact['prob_q_early'][:,iq],atol=.001)
            self.assertTrue(np.all(np.diagonal(row['covariance'],axis1=1,axis2=2)>=-1e-14))
        self.assertTrue(any(r['probability_factor']<1 for r in conditional))

    def test_supported_evaluator_keeps_existing_joint_payoffs(self):
        model=toy();p=initial(model)
        settings=Settings(mode='enumerate',count_cap=10)
        a=JointPayoffEvaluator(model,settings).evaluate(1,.3,.5,p,10,19)
        b=SupportedHistoryEvaluator(model,settings).evaluate(1,.3,.5,p,10,19)
        for key in ('u_e','u_h','completion','old_joint'):
            np.testing.assert_allclose(a[key],b[key],atol=1e-13)
        self.assertLessEqual(b['unknown_feasible_history_count'],a['unknown_feasible_history_count'])

    def test_zero_win_proof_allows_positive_history_probability(self):
        model=toy();p=initial(model)
        p.sigma_h[:]=.01;p.retain[:]=.4
        evaluator=JointPayoffEvaluator(model,Settings(mode='enumerate',count_cap=8))
        ev=evaluator.evaluate(1,.3,.5,p,2,13)
        proof=old_win_zero_certificates(model,.3,p.q_values,ev['lambda_new'])
        self.assertTrue(np.any(proof&(ev['prob_q_early']>0)))
        np.testing.assert_allclose(ev['pi_old'][proof & (ev['prob_q_early']>0)],0,atol=1e-13)

    def test_zero_win_proof_for_all_small_count_vectors(self):
        from itertools import product
        model=toy();p=initial(model)
        evaluator=JointPayoffEvaluator(model,Settings())
        rng=np.random.default_rng(103)
        counts=np.array(list(product(range(3),repeat=3)))
        for _ in range(8):
            new=rng.uniform(0,.2,size=(2,3));old=rng.uniform(0,1,size=(2,3))
            proof=old_win_zero_certificates(model,.3,p.q_values,new)
            for s in range(3):
                tagged=counts.copy();tagged[:,s]+=1
                lengths,mid=evaluator.value_intervals(tagged,.3,p.q_values,old,new)
                acceptable=model.par.beta*mid-(.3+model.beta_detour[s])>1e-12
                for iq in range(2):
                    if proof[s,iq]:
                        np.testing.assert_allclose(lengths[:,iq+1,:] @ acceptable,0,atol=1e-12)

    def test_certified_audit_checks_retaining_at_zero_win_histories(self):
        model=toy();p=initial(model,.4,.4)
        p.sigma_e[:]=model.a<=.4;p.sigma_h[:]=0;p.retain[:]=0
        evaluator=CertifiedPayoffEvaluator(model,Settings())
        good=evaluator.audit(1,.4,.4,p,100000,701)
        self.assertTrue(good['bounded_checks_pass'])
        self.assertTrue(np.all(good['old_win_certified_zero']))
        p.retain[:]=.5
        bad=evaluator.audit(1,.4,.4,p,100000,701)
        self.assertFalse(bad['bounded_checks_pass'])
        self.assertAlmostEqual(bad['retention_regret_upper'],.002)
        self.assertAlmostEqual(bad['retention_support_gap_upper'],.004)

    def test_certified_audit_preserves_initial_incentive_failure(self):
        model=toy();p=initial(model)
        p.sigma_e[:]=0;p.sigma_h[:]=.9;p.retain[:]=0
        audit=CertifiedPayoffEvaluator(model,Settings()).audit(1,.3,.5,p,10000,191)
        self.assertFalse(audit['bounded_checks_pass'])
        self.assertGreater(audit['full_plan_regret_upper'],.001)

    def test_certified_audit_conditional_path_is_exercised(self):
        model=toy();p=initial(model)
        audit=CertifiedPayoffEvaluator(model,Settings()).audit(12,.3,.5,p,1000,712)
        self.assertGreater(len(audit['conditional_retention_audit']),0)
        self.assertFalse(audit['bounded_checks_pass'])

    def test_cost_lift_preserves_feasibility_at_new_cell_boundaries(self):
        old=toy();p=initial(old)
        edges=np.array([0,.1,1.])
        target=FixedSupportRescueModel(ModelParams(route_draws=10),np.array([.01,.29,.31,.51,.9]),
            np.ones(5)/5,old.s,old.fs)
        out=lift_profile(target,edges,p,.3,.5)
        self.assertTrue(np.all(out.sigma_e[target.a>.3]==0))
        self.assertTrue(np.all(out.sigma_h[target.a>.5]==0))
        self.assertTrue(np.all(out.retain[:,target.par.delta*.3-target.a<=0]==0))
        self.assertTrue(np.all(out.sigma_e+out.sigma_h<=1))


if __name__=='__main__': unittest.main()

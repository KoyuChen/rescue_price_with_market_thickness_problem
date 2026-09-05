import unittest
import tempfile
from pathlib import Path
import numpy as np
from rescue_solver.core import ModelParams, FixedSupportRescueModel, Profile
from rescue_solver.solver import Settings
from history_envelope import EnvelopeHistoryEvaluator
from accelerated_evaluator import VectorizedTieModel, CachedEnvelopeEvaluator


class AccelerationTests(unittest.TestCase):
    def models(self):
        par=ModelParams(route_draws=10)
        args=(par,np.array([.03,.2,.6]),np.array([.2,.4,.4]),
              np.array([0.,.2,.6,.99]),np.array([.3,.2,.3,.2]))
        old=FixedSupportRescueModel(*args);new=VectorizedTieModel(*args)
        x,w=np.polynomial.legendre.leggauss(64)
        for m in (old,new):m.tie_t=(x+1)/2;m.tie_w=w/2
        return old,new

    def test_tie_share_all_masks_and_boundary_retentions(self):
        old,new=self.models();rng=np.random.default_rng(17)
        counts=rng.integers(0,100,(31,4))
        for mask_id in range(16):
            mask=np.array([bool(mask_id&(1<<j)) for j in range(4)])
            for r in (np.zeros(4),np.ones(4),rng.random(4)):
                for lam in (0.,1e-15,.7,15.):
                    np.testing.assert_allclose(new._tie_factor(counts,mask,r,lam),
                        old._tie_factor(counts,mask,r,lam),atol=2e-15,rtol=2e-14)

    def test_envelope_cache_invalidates_for_prices_and_beliefs(self):
        old,new=self.models();settings=Settings()
        a=EnvelopeHistoryEvaluator(old,settings);b=CachedEnvelopeEvaluator(new,settings)
        rng=np.random.default_rng(63);counts=rng.poisson(2.,(45,4))
        for q in (np.array([.3,.5]),np.array([.37]),np.array([.3,.5])):
            for _ in range(4):
                r=rng.random((len(q),4));lam=rng.random((len(q),4))
                x,mid=a.value_intervals(counts,float(q[0]),q,r,lam)
                y,mid2=b.value_intervals(counts,float(q[0]),q,r,lam)
                np.testing.assert_array_equal(mid,mid2)
                np.testing.assert_allclose(x,y,atol=2e-11,rtol=0)

    def test_full_payoffs_and_audit_remain_equivalent(self):
        old,new=self.models();rng=np.random.default_rng(28)
        p=Profile(rng.random((3,4))*.4,rng.random((3,4))*.4,
                  rng.random((2,3,4)),np.array([.3,.5]),{})
        settings=Settings(count_batch_size=64)
        a=EnvelopeHistoryEvaluator(old,settings);b=CachedEnvelopeEvaluator(new,settings)
        x=a.evaluate(3,.3,.5,p,2000,401);y=b.evaluate(3,.3,.5,p,2000,401)
        for k in ('u_e','u_h','prob_q_early','pi_old','old_joint','completion'):
            np.testing.assert_allclose(x[k],y[k],atol=2e-11,rtol=0)
        x=a.audit(3,.3,.5,p,2000,809);y=b.audit(3,.3,.5,p,2000,809)
        for k in ('full_plan_regret_upper','retention_regret_upper',
                  'initial_support_gap_upper','retention_support_gap_upper'):
            self.assertAlmostEqual(x[k],y[k],places=10)
        self.assertEqual(x['bounded_checks_pass'],y['bounded_checks_pass'])
        self.assertEqual(x['unresolved_histories'],y['unresolved_histories'])

    def test_checkpointed_updates_match_on_flat_menu(self):
        from checkpoint_solver import solve_checkpointed as original_solve
        from accelerated_checkpoint_solver import solve_checkpointed as fast_solve
        old,new=self.models()
        settings=Settings(train_counts=100,audit_counts=500,count_batch_size=64,
                          schedule=((.004,4,.25),(0.,8,.1)))
        with tempfile.TemporaryDirectory() as directory:
            a,ra=original_solve(old,1.,.4,.4,settings,Path(directory)/'old.npz',{})
            b,rb=fast_solve(new,1.,.4,.4,settings,Path(directory)/'new.npz',{})
        for key in ('sigma_e','sigma_h','retain'):
            np.testing.assert_allclose(getattr(a,key),getattr(b,key),atol=2e-11,rtol=0)
        self.assertEqual(ra['numerical_checks_passed'],rb['numerical_checks_passed'])


if __name__=='__main__':unittest.main()

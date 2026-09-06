import unittest
import numpy as np
from rescue_solver.core import ModelParams,FixedSupportRescueModel,Profile
from rescue_solver.solver import Settings
from research_solver.evaluator import JointPayoffEvaluator
from rare_history_enumeration import compressed_old_posterior


class RareHistoryEnumerationTests(unittest.TestCase):
    def setUp(self):
        self.model=FixedSupportRescueModel(ModelParams(route_draws=10),
            np.array([.1,.4]),np.array([.5,.5]),
            np.array([0.,.3,.9]),np.array([.4,.3,.3]))
        self.profile=Profile(np.full((2,3),.2),np.full((2,3),.2),
            np.zeros((2,2,3)),np.array([.15,.25]),{})
        # Keep route 0 explicit at both prices; route 1 is marginalized;
        # route 2 makes the high continuation structurally impossible.
        self.profile.retain[:,0,0]=.5
        self.evaluator=JointPayoffEvaluator(self.model,Settings())

    def test_compressed_states_preserve_integrand(self):
        result=compressed_old_posterior(self.evaluator,1.,.15,self.profile,1,0,12)
        self.assertIn(0,result['relevant_routes'])
        self.assertNotIn(1,result['relevant_routes'])
        # Tail is retained and the posterior interval contains its estimate.
        self.assertGreaterEqual(result['explicit_count_tail'],0.)
        estimate=result['conditional_win_probability_estimate']
        if estimate is not None:
            self.assertLessEqual(result['conditional_win_probability_lower'],estimate)
            self.assertLessEqual(estimate,result['conditional_win_probability_upper'])

    def test_tiny_retention_is_kept_explicit(self):
        self.profile.retain[0,0,1]=1e-250
        result=compressed_old_posterior(self.evaluator,1.,.15,self.profile,1,0,12)
        self.assertIn(1,result['relevant_routes'])

    def test_larger_cap_nests_posterior_interval(self):
        a=compressed_old_posterior(self.evaluator,1.,.15,self.profile,1,0,5)
        b=compressed_old_posterior(self.evaluator,1.,.15,self.profile,1,0,12)
        self.assertLessEqual(b['explicit_count_tail'],a['explicit_count_tail'])
        self.assertGreaterEqual(b['conditional_win_probability_lower']+1e-15,
                                a['conditional_win_probability_lower'])
        self.assertLessEqual(b['conditional_win_probability_upper'],
                             a['conditional_win_probability_upper']+1e-15)
        self.assertGreater(b['explicit_count_tail'],0.)


if __name__=='__main__':unittest.main()

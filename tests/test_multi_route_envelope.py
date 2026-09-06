import unittest
import numpy as np
from rescue_solver.core import ModelParams,FixedSupportRescueModel
from rescue_solver.solver import Settings
from research_solver.evaluator import JointPayoffEvaluator
from multi_route_envelope import multi_route_count_exclusion


class MultiRouteEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.model=FixedSupportRescueModel(ModelParams(route_draws=10),
            np.array([.1,.4]),np.array([.5,.5]),
            np.array([0.,.3,.9]),np.array([.4,.3,.3]))
        self.evaluator=JointPayoffEvaluator(self.model,Settings())
        self.q=np.array([.15,.8]);self.old=np.array([[.9,.9,0.],[.2,.3,0.]])
        self.new=np.zeros((2,3));self.new[0,2]=2.

    def test_multiple_positive_routes_are_covered(self):
        result=multi_route_count_exclusion(self.evaluator,.15,self.q,self.old,self.new,0,0,1)
        self.assertTrue(result['passed'],result)
        self.assertEqual(result['active_target_retention_routes'],[0,1])
        self.assertTrue(result['all_count_vectors_covered'])

    def test_profitable_target_is_not_excluded(self):
        q=np.array([.15,.20]);old=self.old.copy();old[1]=[.9,.9,0.]
        new=np.zeros_like(self.new);new[1,2]=20.
        result=multi_route_count_exclusion(self.evaluator,.15,q,old,new,0,0,1,max_threshold=20)
        self.assertFalse(result['passed'])

    def test_tiny_positive_retention_is_not_dropped(self):
        old=self.old.copy();old[0,2]=1.;old[1,2]=1e-250
        result=multi_route_count_exclusion(self.evaluator,.15,self.q,old,self.new,0,0,1)
        self.assertIn(2,result['active_target_retention_routes'])


if __name__=='__main__':unittest.main()

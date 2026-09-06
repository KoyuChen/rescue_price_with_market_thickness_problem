import math
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
from rare_history_enumeration_v2 import _poisson_total_tail, _poisson_vector_weight, compressed_old_posterior
from multi_route_envelope_v2 import _threshold_check, multi_route_count_exclusion
import test_rare_history_enumeration as fixtures


class RareHistoryV2Tests(unittest.TestCase):
    def test_tail_below_mean_is_not_a_small_right_tail(self):
        for mean, cap in [(20.,0),(100.,20),(2.,0),(1.,0)]:
            self.assertEqual(_poisson_total_tail(mean,cap),1.)

    def test_tail_above_mean_bounds_direct_series(self):
        for mean, cap in [(.3,12),(6.,8),(20.,25),(1.,0)]:
            actual=math.fsum(math.exp(-mean+k*math.log(mean)-math.lgamma(k+1))
                            for k in range(cap+1,300))
            self.assertGreaterEqual(_poisson_total_tail(mean,cap)+1e-16,actual)
            self.assertLessEqual(_poisson_total_tail(mean,cap),1.)

    def test_zero_intensity_coordinates(self):
        self.assertAlmostEqual(_poisson_vector_weight((0,2),np.array([0.,.5])),
                               math.exp(-.5)*.5**2/2)
        self.assertEqual(_poisson_vector_weight((1,0),np.array([0.,.5])),0.)

    def test_explicit_budget_fails_closed(self):
        fixture=fixtures.RareHistoryEnumerationTests();fixture.setUp()
        with self.assertRaisesRegex(ValueError,'budget exceeded'):
            compressed_old_posterior(fixture.evaluator,1.,.15,fixture.profile,1,0,12,max_states=1)

    def test_zero_count_does_not_invent_better_route(self):
        class Model:
            S=2;s=np.array([0.,1.]);beta_detour=np.array([.5,0.])
            par=SimpleNamespace(ell=.5,beta=.8)
            def _expected_terminal_value(self,counts,v,p1,q,old,new):
                return np.maximum(v-.3,0.)*.5 if q>.2 else np.zeros(len(v))
        model=Model();old=np.array([[0.,0.],[0.,1.]])
        result=_threshold_check(model,.1,np.array([.1,.25]),old,np.zeros_like(old),0,1,0,0,1)
        self.assertFalse(result['passed'])

    def test_positive_tiny_interval_is_not_excluded(self):
        evaluator=SimpleNamespace(model=SimpleNamespace(S=1),
            value_intervals=lambda *a:(np.array([[[0.],[0.],[5e-13]]]),None))
        def check(*args):return {'passed':args[7]==1}
        with patch('multi_route_envelope_v2._threshold_check',side_effect=check):
            result=multi_route_count_exclusion(evaluator,.1,np.array([.1,.2]),
                np.ones((2,1)),np.zeros((2,1)),0,0,1)
        self.assertFalse(result['passed']);self.assertEqual(result['maximum_target_interval'],5e-13)

    def test_rectangle_budget_fails_closed(self):
        evaluator=SimpleNamespace(model=SimpleNamespace(S=2))
        with patch('multi_route_envelope_v2._threshold_check',
                   side_effect=lambda *a:{'passed':a[7]==10}):
            result=multi_route_count_exclusion(evaluator,.1,np.array([.1,.2]),
                np.ones((2,2)),np.zeros((2,2)),0,0,1,max_states=20)
        self.assertFalse(result['passed']);self.assertEqual(result['reason'],'finite_rectangle_budget_exceeded')
        self.assertFalse(result['all_count_vectors_covered'])

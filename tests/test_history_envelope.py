from itertools import product
import unittest
import numpy as np
from rescue_solver.core import ModelParams, FixedSupportRescueModel
from rescue_solver.solver import Settings
from research_solver.evaluator import JointPayoffEvaluator
from history_envelope import count_envelope_certificates, envelope_check


class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.model=FixedSupportRescueModel(ModelParams(route_draws=10),
            np.array([.1,.4]),np.array([.5,.5]),
            np.array([0.,.3,.9]),np.array([.4,.3,.3]))
        self.q=np.array([.365,.535])

    def test_exclusion_agrees_with_rider_envelope_for_other_counts(self):
        # High continuation is expensive and weak, while lower continuation
        # has substantial hidden supply and greater incumbent retention.
        old=np.array([[.5,.8,0.],[.3,0.,0.]])
        new=np.array([[.03,.08,.25],[.04,.09,.26]])
        proof,records=count_envelope_certificates(self.model,.365,self.q,old,new)
        self.assertTrue(proof[0,1],records)
        counts=np.array(list(product(range(5),repeat=3)))
        evaluator=JointPayoffEvaluator(self.model,Settings())
        for s,iq in np.argwhere(proof):
            tagged=counts.copy();tagged[:,s]+=1
            lengths,_=evaluator.value_intervals(tagged,.365,self.q,old,new)
            self.assertLess(float(lengths[:,iq+1,:].max()),1e-11)
        # Independently exercise large counts covered by the tail argument.
        for k in (20,50,200):
            self.assertTrue(envelope_check(self.model,.365,self.q,old,new,0,0,1,k)['passed'])

    def test_positive_retention_on_second_route_is_never_dropped(self):
        old=np.array([[.5,.8,0.],[.3,1e-250,0.]])
        new=np.array([[.03,.08,.25],[.04,.09,.26]])
        proof,_=count_envelope_certificates(self.model,.365,self.q,old,new)
        self.assertFalse(proof.any())

    def test_profitable_high_price_branch_is_not_excluded(self):
        old=np.zeros((2,3));new=np.zeros((2,3))
        new[1,-1]=20.
        proof,_=count_envelope_certificates(self.model,.365,self.q,old,new)
        self.assertFalse(proof[0,1])
        counts=np.array([[1,0,0]])
        lengths,_=JointPayoffEvaluator(self.model,Settings()).value_intervals(
            counts,.365,self.q,old,new)
        self.assertGreater(float(lengths[:,2,:].sum()),0.)


if __name__=='__main__':unittest.main()

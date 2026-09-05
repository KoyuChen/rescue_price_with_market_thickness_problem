"""Stronger exact zero-history certificates; same joint-payoff audit."""
import numpy as np
from .evaluator import JointPayoffEvaluator
from .posterior import supported_hidden_offpath


class SupportedHistoryEvaluator(JointPayoffEvaluator):
    def evaluate(self,m,p1,p2,profile,n,seed):
        ev=super().evaluate(m,p1,p2,profile,n,seed)
        certified=supported_hidden_offpath(self.model,p1,profile.q_values,ev['lambda_new'])
        if np.any(ev['prob_q_early'][certified]>1e-10):
            raise ArithmeticError('Supported hidden-route proof contradicts rider integration')
        unknown=(ev['prob_q_early']==0)&~certified
        pi=ev['pi_old'].copy();pi[certified]=0
        ev['pi_old']=pi
        ev['retain_advantage']=pi.T[:,None,:]*(self.model.par.delta*p1-self.model.a)-self.model.par.omega_old
        ev['retain_advantage']=np.where(unknown.T[:,None,:],0.,ev['retain_advantage'])
        ev['offpath_certified']=certified;ev['unknown_old_history']=unknown
        feasible=np.any(self.model.a<=p1+1e-12,axis=0)
        ev['unknown_feasible_history_count']=int(np.sum(unknown&feasible[:,None]))
        ev['pi_old_report']=[[None if unknown[s,q] else float(pi[s,q])
                             for q in range(len(profile.q_values))] for s in range(self.model.S)]
        return ev

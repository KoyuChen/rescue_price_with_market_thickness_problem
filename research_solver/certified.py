"""Count-law audit with zero-win proofs and conditional Poisson integration."""
from dataclasses import replace
import math
import numpy as np
from rescue_solver.diagnostics import regret_diagnostics
from .supported import SupportedHistoryEvaluator
from .posterior import old_win_zero_certificates
from .conditional import old_conditional_moments
from .evaluator import bernstein_radius


class CertifiedPayoffEvaluator(SupportedHistoryEvaluator):
    def evaluate(self,m,p1,p2,profile,n,seed):
        ev=super().evaluate(m,p1,p2,profile,n,seed)
        zero=old_win_zero_certificates(self.model,p1,profile.q_values,ev['lambda_new'])
        observed=ev['prob_q_early']>0
        if np.any(ev['pi_old'][zero & observed]>1e-9):
            raise ArithmeticError('Zero-win proof contradicts integrated old win rate')
        ev['old_win_certified_zero']=zero
        ev['pi_old'][zero]=0
        ev['retain_advantage']=np.where(zero.T[:,None,:],-self.model.par.omega_old,ev['retain_advantage'])
        ev['unknown_old_history'] &= ~zero
        feasible=np.any(self.model.a<=p1+1e-12,axis=0)
        ev['unknown_feasible_history_count']=int(np.sum(ev['unknown_old_history']&feasible[:,None]))
        for s,iq in np.argwhere(zero): ev['pi_old_report'][s][iq]=0.
        return ev

    def audit(self,m,p1,p2,profile,n,seed):
        # Half of alpha for initial full-plan/support comparisons, half for
        # the independent conditional retention audit. No training on either.
        original=self.settings
        self.settings=replace(original,alpha=original.alpha/2)
        try:
            base=super().audit(m,p1,p2,profile,n,seed)
        finally:
            self.settings=original
        model=self.model;Q=len(profile.q_values)
        _,_,new=model._belief_objects(m,p1,profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain)
        zero=old_win_zero_certificates(model,p1,profile.q_values,new)
        exact=zero | np.asarray(base['offpath_certified'])
        feasible=model.a<=p1+1e-12
        needs=np.any(~exact & np.any(feasible,axis=0)[:,None])
        conditional=old_conditional_moments(self,m,p1,profile,n,seed+3000017) if needs else None
        family=model.S*Q*(2*model.C+1)
        logarithm=math.log(2*family/(original.alpha/2))
        retention_upper=retention_support_upper=0.
        unresolved=[];history=[]
        margin=model.par.delta*p1-model.a
        for iq in range(Q):
            r=profile.retain[iq]
            ret=r*model.par.omega_old
            sup=np.where(r>1e-3,model.par.omega_old,0.)
            active=feasible & ~exact[:,iq][None,:]
            if np.any(active):
                row=conditional[iq];mu=row['mean'];cov=row['covariance']
                dl=np.maximum(0.,mu[:,0]-bernstein_radius(cov[:,0,0],1.,n,logarithm))
                jm=mu[:,1]*margin-mu[:,0]*model.par.omega_old
                var=margin**2*cov[:,1,1]+model.par.omega_old**2*cov[:,0,0]-2*margin*model.par.omega_old*cov[:,0,1]
                radius=bernstein_radius(var,abs(margin)+model.par.omega_old,n,logarithm)
                jl=np.maximum(jm-radius,np.minimum(-model.par.omega_old,margin-model.par.omega_old))
                ju=np.minimum(jm+radius,np.maximum(0.,margin-model.par.omega_old))
                nr=np.maximum((1-r)*np.maximum(ju,0),r*np.maximum(-jl,0))
                ns=np.maximum(np.where(r<1-1e-3,np.maximum(ju,0),0),np.where(r>1e-3,np.maximum(-jl,0),0))
                # Universal pi in [0,1] also provides a valid fallback bound,
                # not a made-up posterior. Retaining must pass for that range.
                al=np.minimum(margin,0)-model.par.omega_old
                ah=np.maximum(margin,0)-model.par.omega_old
                universal_r=np.maximum((1-r)*np.maximum(ah,0),r*np.maximum(-al,0))
                universal_s=np.maximum(np.where(r<1-1e-3,np.maximum(ah,0),0),np.where(r>1e-3,np.maximum(-al,0),0))
                cr=np.minimum(universal_r,np.divide(nr,dl,out=universal_r.copy(),where=dl>0))
                cs=np.minimum(universal_s,np.divide(ns,dl,out=universal_s.copy(),where=dl>0))
                ret=np.where(active,cr,ret);sup=np.where(active,cs,sup)
                bad=active & (dl[None,:]<=0) & ((ret>original.regret_tol)|(sup>original.support_tol))
                unresolved += [dict(q=float(profile.q_values[iq]),cost_index=int(c),route_index=int(s),
                    conditional_event_mean=float(mu[s,0])) for c,s in np.argwhere(bad)]
                history.append(dict(q=float(profile.q_values[iq]),conditional_event_mean=mu[:,0].tolist(),
                    conditional_event_lower=dl.tolist(),log_probability_factor=row['log_probability_factor'],
                    seed=seed+3000017+iq*104729,count_draws=n,count_states=row['count_states']))
            retention_upper=max(retention_upper,float(np.max(np.where(feasible,ret,0))))
            retention_support_upper=max(retention_support_upper,float(np.max(np.where(feasible,sup,0))))
        base.update(method='direct_payoff_Bernstein_with_structural_zero_wins_and_conditional_counts',
            alpha=original.alpha,conditional_retention_audit=history,
            old_win_certified_zero=zero.tolist(),unresolved_histories=unresolved,
            original_unconditional_retention_upper=base['retention_regret_upper'],
            retention_regret_upper=retention_upper,retention_support_gap_upper=retention_support_upper)
        maximum=max(base['full_plan_regret_upper'],retention_upper)
        base['max_regret_upper']=None if unresolved else maximum
        base['bounded_checks_pass']=bool(not unresolved and maximum<=original.regret_tol and
            max(base['initial_support_gap_upper'],retention_support_upper)<=original.support_tol)
        return base

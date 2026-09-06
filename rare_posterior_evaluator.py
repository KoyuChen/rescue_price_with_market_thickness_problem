"""Count-tail posterior intervals in training and held-out retention audits.

On-path rare events never receive off-path beliefs. Every profile update
invalidates the posterior cache; audit draws remain unused by training.
Budget exhaustion leaves a history unresolved instead of weakening a gate.
"""
from dataclasses import replace
import math
import numpy as np
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator
from bounded_rare_posterior import compressed_old_posterior
from strict_multi_route_envelope import multi_route_count_exclusion
from research_solver.evaluator import JointPayoffEvaluator, bernstein_radius
from research_solver.conditional import old_conditional_moments
from research_solver.posterior import supported_hidden_offpath


def retention_interval_bounds(model, p1, profile, low, high):
    margin=model.par.delta*p1-model.a
    x=low.T[:,None,:]*margin-model.par.omega_old
    y=high.T[:,None,:]*margin-model.par.omega_old
    a,b=np.minimum(x,y),np.maximum(x,y)
    r=profile.retain
    regret=np.maximum((1-r)*np.maximum(b,0.),r*np.maximum(-a,0.))
    support=np.maximum(np.where(r<1-1e-3,np.maximum(b,0.),0.),
                       np.where(r>1e-3,np.maximum(-a,0.),0.))
    return regret,support


class RarePosteriorEvaluator(ZeroRetentionEnvelopeEvaluator):
    posterior_caps=(12,18,24,32)
    posterior_max_states=100000
    posterior_max_dimensions=8
    # Trigger is only an integration choice, never a probability cutoff.
    rare_event_trigger=.01
    posterior_payoff_width=1e-9

    def _posterior(self,m,p1,profile,tag,iq,ev):
        old,new=ev['old_r'],ev['lambda_new']
        key=(float(m),float(p1),profile.q_values.tobytes(),
             ev['lambda_early'].tobytes(),old.tobytes(),new.tobytes())
        if getattr(self,'_posterior_key',None)!=key:
            self._posterior_key=key;self._posterior_cache={}
        pair=(tag,iq)
        if pair in self._posterior_cache:return self._posterior_cache[pair]
        if iq>0:
            proof=multi_route_count_exclusion(self,p1,profile.q_values,
                old,new,tag,0,iq,max_states=self.posterior_max_states)
            if proof['passed']:
                row=dict(resolved=True,structurally_off_path=True,
                         multi_route_count_exclusion=proof)
                self._posterior_cache[pair]=row
                return row
        forbidden=supported_hidden_offpath(self.model,p1,profile.q_values,new)[:,iq]
        dims=int(np.sum(~forbidden & (ev['lambda_early']>0.) & np.any(old>0.,axis=0)))
        if dims>self.posterior_max_dimensions:
            row=dict(resolved=False,reason='positive_retention_dimension_budget',dimensions=dims)
            self._posterior_cache[pair]=row
            return row
        row=None
        for cap in self.posterior_caps:
            if math.comb(cap+dims,dims)>self.posterior_max_states:break
            row=compressed_old_posterior(self,m,p1,profile,iq,tag,cap,
                batch_size=256,max_states=self.posterior_max_states)
            positive=row['conditional_event_measure_lower']>0.
            width=row['conditional_win_probability_upper']-row['conditional_win_probability_lower']
            margin=float(np.max(abs(self.model.par.delta*p1-self.model.a[:,tag])))
            if positive and width*margin<=self.posterior_payoff_width:
                row=dict(row,resolved=True,structurally_off_path=False);break
        if row is None or not row.get('resolved'):
            row=dict(resolved=False,reason='posterior_budget_or_width',last_enclosure=row)
        self._posterior_cache[pair]=row
        return row

    def evaluate(self,m,p1,p2,profile,n,seed):
        ev=super().evaluate(m,p1,p2,profile,n,seed)
        model=self.model;feasible=np.any(model.a<=p1+1e-12,axis=0)
        exact=ev['offpath_certified']|ev['old_win_certified_zero']
        rare=(ev['prob_q_early']<self.rare_event_trigger)&~exact&feasible[:,None]
        mask=np.zeros_like(exact);records=[];low=np.zeros_like(ev['pi_old']);high=np.ones_like(low)
        for tag,iq in np.argwhere(rare):
            tag,iq=int(tag),int(iq)
            row=self._posterior(m,p1,profile,tag,iq,ev)
            records.append(dict(row,tag_route=tag,price_index=iq))
            if not row['resolved']:continue
            mask[tag,iq]=True;ev['unknown_old_history'][tag,iq]=False
            if row['structurally_off_path']:
                if ev['prob_q_early'][tag,iq]>0.:
                    raise ArithmeticError('All-count exclusion contradicts observed history')
                ev['offpath_certified'][tag,iq]=True
                pi=lo=hi=0.;den=num=0.
            else:
                lo=row['conditional_win_probability_lower'];hi=row['conditional_win_probability_upper']
                pi=row['conditional_win_probability_estimate']
                factor=row['conditioned_zero_probability_factor']
                den=row['conditional_event_measure_lower']*factor
                num=row['tagged_win_measure_lower']*factor
            low[tag,iq],high[tag,iq]=lo,hi
            ev['pi_old'][tag,iq]=pi;ev['pi_old_report'][tag][iq]=pi
            ev['pi_old_low'][tag,iq]=lo;ev['pi_old_high'][tag,iq]=hi
            ev['prob_q_early'][tag,iq]=den
            margin=model.par.delta*p1-model.a[:,tag]
            ev['retain_advantage'][iq,:,tag]=pi*margin-model.par.omega_old
            ev['old_joint'][iq,:,tag]=num*margin-den*model.par.omega_old
        ev['u_e']=ev['p_immediate'][None,:]*(p1-model.a)+np.maximum(ev['old_joint'],0.).sum(axis=0)
        ev['u_e']=np.where(model.a<=p1+1e-12,ev['u_e'],-1e6)
        ev['unknown_feasible_history_count']=int(np.sum(ev['unknown_old_history']&feasible[:,None]))
        ev.update(rare_posterior_records=records,rare_posterior_mask=mask,
                  rare_posterior_low=low,rare_posterior_high=high)
        self.latest_rare_evaluation=ev
        return ev

    def audit(self,m,p1,p2,profile,n,seed):
        original=self.settings
        self.settings=replace(original,alpha=original.alpha/2)
        try:base=JointPayoffEvaluator.audit(self,m,p1,p2,profile,n,seed)
        finally:self.settings=original
        ev=self.latest_rare_evaluation;model=self.model;Q=len(profile.q_values)
        exact=ev['offpath_certified']|ev['old_win_certified_zero']
        rare=ev['rare_posterior_mask']&~exact
        feasible=model.a<=p1+1e-12
        remaining=~exact&~rare&np.any(feasible,axis=0)[:,None]
        conditional=old_conditional_moments(self,m,p1,profile,n,seed+3000017) if np.any(remaining) else None
        # The same half-alpha allocation as the original conditional audit.
        logarithm=math.log(2*model.S*Q*(2*model.C+1)/(original.alpha/2))
        rr,rs=retention_interval_bounds(model,p1,profile,
            ev['rare_posterior_low'],ev['rare_posterior_high'])
        margin=model.par.delta*p1-model.a
        retention_upper=support_upper=0.;unresolved=[];history=[]
        for iq in range(Q):
            r=profile.retain[iq]
            ret=r*model.par.omega_old;sup=np.where(r>1e-3,model.par.omega_old,0.)
            ret=np.where(rare[:,iq][None,:],rr[iq],ret)
            sup=np.where(rare[:,iq][None,:],rs[iq],sup)
            active=feasible&remaining[:,iq][None,:]
            if np.any(active):
                row=conditional[iq];mu,cov=row['mean'],row['covariance']
                dl=np.maximum(0.,mu[:,0]-bernstein_radius(cov[:,0,0],1.,n,logarithm))
                jm=mu[:,1]*margin-mu[:,0]*model.par.omega_old
                var=margin**2*cov[:,1,1]+model.par.omega_old**2*cov[:,0,0]-2*margin*model.par.omega_old*cov[:,0,1]
                radius=bernstein_radius(var,abs(margin)+model.par.omega_old,n,logarithm)
                jl=np.maximum(jm-radius,np.minimum(-model.par.omega_old,margin-model.par.omega_old))
                ju=np.minimum(jm+radius,np.maximum(0.,margin-model.par.omega_old))
                nr=np.maximum((1-r)*np.maximum(ju,0.),r*np.maximum(-jl,0.))
                ns=np.maximum(np.where(r<1-1e-3,np.maximum(ju,0.),0.),np.where(r>1e-3,np.maximum(-jl,0.),0.))
                al=np.minimum(margin,0.)-model.par.omega_old
                ah=np.maximum(margin,0.)-model.par.omega_old
                ur=np.maximum((1-r)*np.maximum(ah,0.),r*np.maximum(-al,0.))
                us=np.maximum(np.where(r<1-1e-3,np.maximum(ah,0.),0.),np.where(r>1e-3,np.maximum(-al,0.),0.))
                ret=np.where(active,np.minimum(ur,np.divide(nr,dl,out=ur.copy(),where=dl>0)),ret)
                sup=np.where(active,np.minimum(us,np.divide(ns,dl,out=us.copy(),where=dl>0)),sup)
                bad=active&(dl[None,:]<=0)&((ret>original.regret_tol)|(sup>original.support_tol))
                unresolved.extend(dict(q=float(profile.q_values[iq]),cost_index=int(c),route_index=int(s),
                    conditional_event_mean=float(mu[s,0])) for c,s in np.argwhere(bad))
                history.append(dict(q=float(profile.q_values[iq]),conditional_event_mean=mu[:,0].tolist(),
                    conditional_event_lower=dl.tolist(),log_probability_factor=row['log_probability_factor'],
                    count_draws=n,count_states=row['count_states'],seed=seed+3000017+iq*104729))
            retention_upper=max(retention_upper,float(np.max(np.where(feasible,ret,0.))))
            support_upper=max(support_upper,float(np.max(np.where(feasible,sup,0.))))
        maximum=max(base['full_plan_regret_upper'],retention_upper)
        base.update(alpha=original.alpha,method='joint_payoff_Bernstein_and_conditional_counts_and_bounded_rare_posteriors',
            conditional_retention_audit=history,rare_posterior_records=ev['rare_posterior_records'],
            old_win_certified_zero=ev['old_win_certified_zero'].tolist(),
            retention_regret_upper=retention_upper,retention_support_gap_upper=support_upper,
            unresolved_histories=unresolved,max_regret_upper=None if unresolved else maximum,
            bounded_checks_pass=bool(not unresolved and maximum<=original.regret_tol and
                max(base['initial_support_gap_upper'],support_upper)<=original.support_tol),
            all_count_tails_retained=True,exact_arithmetic_certificate=False)
        return base

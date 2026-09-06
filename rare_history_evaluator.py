"""Independent evaluator: tail-bounded rare posteriors enter retention updates.

No probability-mass cutoff or replacement of an unresolved conditional history
by an off-path belief. Budget failures remain unresolved. Floating evaluation
is used, as in the original evaluator; this is not exact-arithmetic proof.
"""
import hashlib
import numpy as np
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator
from rare_history_enumeration_v2 import compressed_old_posterior
from multi_route_envelope_v2 import multi_route_count_exclusion


def interval_retention_bounds(retain, margin, omega, lower, upper):
    """Worst regret/support violation over the ENTIRE posterior interval."""
    a=margin*lower-omega;b=margin*upper-omega
    lo=np.minimum(a,b);hi=np.maximum(a,b)
    regret=np.maximum((1-retain)*np.maximum(hi,0.),retain*np.maximum(-lo,0.))
    support=np.maximum(np.where(retain<1-1e-3,np.maximum(hi,0.),0.),
                       np.where(retain>1e-3,np.maximum(-lo,0.),0.))
    return regret,support


class RareHistoryEvaluator(ZeroRetentionEnvelopeEvaluator):
    count_caps=(4,8,12,16,18,20,24,32,48,64)
    max_states=100000
    posterior_width=1e-8

    def _reset_rare_cache(self,m,p1,profile):
        h=hashlib.sha256(repr((m,p1)).encode())
        for a in (profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain):
            h.update(np.ascontiguousarray(a).tobytes())
        key=h.hexdigest()
        if getattr(self,'_rare_key',None)!=key:
            self._rare_key=key;self._rare_records={}

    def _resolve_rare(self,m,p1,profile,ev,tag,iq):
        key=(int(tag),int(iq))
        if key in self._rare_records:return self._rare_records[key]
        attempts=[]
        for low in range(iq):
            exclusion=multi_route_count_exclusion(self,p1,profile.q_values,
                ev['old_r'],ev['lambda_new'],tag,low,iq,max_states=self.max_states)
            if exclusion['passed']:
                record=dict(route_index=tag,price_index=iq,kind='all_count_exclusion',
                            resolved=True,exclusion=exclusion)
                self._rare_records[key]=record;return record
        for cap in self.count_caps:
            try:
                result=compressed_old_posterior(self,m,p1,profile,iq,tag,cap,
                                                max_states=self.max_states)
            except ValueError as error:
                if 'budget exceeded' not in str(error):raise
                attempts.append(dict(cap=cap,reason=str(error)));break
            attempts.append(dict(cap=cap,states=result['explicit_count_states'],
                event_lower=result['conditional_event_measure_lower'],
                posterior_width=result['conditional_win_probability_upper']-
                                result['conditional_win_probability_lower']))
            if (result['conditional_event_measure_lower']>0. and
                    attempts[-1]['posterior_width']<=self.posterior_width):
                record=dict(route_index=tag,price_index=iq,kind='bounded_posterior',
                            resolved=True,posterior=result,attempts=attempts)
                self._rare_records[key]=record;return record
        record=dict(route_index=tag,price_index=iq,kind='unresolved',
                    resolved=False,attempts=attempts)
        self._rare_records[key]=record;return record

    def _apply_rare_record(self,ev,profile,p1,record):
        if not record['resolved']:return
        tag=record['route_index'];iq=record['price_index']
        if record['kind']=='all_count_exclusion':
            if ev['prob_q_early'][tag,iq]>0.:
                raise ArithmeticError('All-count exclusion contradicts observed history')
            ev['offpath_certified'][tag,iq]=True;pi=0.
        else:
            pi=record['posterior']['conditional_win_probability_estimate']
        ev['unknown_old_history'][tag,iq]=False
        ev['pi_old'][tag,iq]=pi;ev['pi_old_report'][tag][iq]=pi
        ev['retain_advantage'][iq,:,tag]=pi*(self.model.par.delta*p1-self.model.a[:,tag])-self.model.par.omega_old

    def evaluate(self,m,p1,p2,profile,n,seed):
        ev=super().evaluate(m,p1,p2,profile,n,seed)
        self._reset_rare_cache(m,p1,profile)
        feasible=np.any(self.model.a<=p1+1e-12,axis=0)
        for tag,iq in np.argwhere(ev['unknown_old_history'] & feasible[:,None]):
            record=self._resolve_rare(m,p1,profile,ev,int(tag),int(iq))
            self._apply_rare_record(ev,profile,p1,record)
        ev['unknown_feasible_history_count']=int(np.sum(ev['unknown_old_history'] & feasible[:,None]))
        ev['rare_history_resolution']=list(self._rare_records.values())
        self.latest_rare_evaluation=ev
        return ev

    def audit(self,m,p1,p2,profile,n,seed):
        from dataclasses import replace
        import math
        from research_solver.evaluator import JointPayoffEvaluator, bernstein_radius
        from research_solver.posterior import old_win_zero_certificates
        from research_solver.conditional import old_conditional_moments
        # Half of alpha for initial full-plan/support comparisons, half for
        # the independent conditional retention audit. No training on either.
        original=self.settings
        self.settings=replace(original,alpha=original.alpha/2)
        try:
            base=JointPayoffEvaluator.audit(self,m,p1,p2,profile,n,seed)
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
        ev=self.latest_rare_evaluation
        if conditional is not None:
            for iq,row in enumerate(conditional):
                mu=row['mean'];cov=row['covariance']
                dl=np.maximum(0.,mu[:,0]-bernstein_radius(cov[:,0,0],1.,n,logarithm))
                candidates=(dl<=0.) & ~exact[:,iq] & np.any(feasible,axis=0)
                for tag in np.flatnonzero(candidates):
                    record=self._resolve_rare(m,p1,profile,ev,int(tag),iq)
                    self._apply_rare_record(ev,profile,p1,record)
        base['offpath_certified']=ev['offpath_certified'].tolist()
        exact=zero | ev['offpath_certified']
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
                deterministic=np.zeros(model.S,dtype=bool)
                for (tag,j),record in self._rare_records.items():
                    if j != iq or not record['resolved'] or record['kind']!='bounded_posterior':
                        continue
                    posterior=record['posterior']
                    cr[:,tag],cs[:,tag]=interval_retention_bounds(r[:,tag],margin[:,tag],
                        model.par.omega_old,posterior['conditional_win_probability_lower'],
                        posterior['conditional_win_probability_upper'])
                    deterministic[tag]=True
                ret=np.where(active,cr,ret);sup=np.where(active,cs,sup)
                bad=active & ~deterministic[None,:] & (dl[None,:]<=0) & ((ret>original.regret_tol)|(sup>original.support_tol))
                unresolved += [dict(q=float(profile.q_values[iq]),cost_index=int(c),route_index=int(s),
                    conditional_event_mean=float(mu[s,0])) for c,s in np.argwhere(bad)]
                history.append(dict(q=float(profile.q_values[iq]),conditional_event_mean=mu[:,0].tolist(),
                    conditional_event_lower=dl.tolist(),log_probability_factor=row['log_probability_factor'],
                    seed=seed+3000017+iq*104729,count_draws=n,count_states=row['count_states']))
            retention_upper=max(retention_upper,float(np.max(np.where(feasible,ret,0))))
            retention_support_upper=max(retention_support_upper,float(np.max(np.where(feasible,sup,0))))
        base.update(method='direct_payoff_Bernstein_conditional_counts_and_tail_bounded_rare_posteriors',
            rare_history_resolution=list(self._rare_records.values()),
            zero_retention_envelope_certificates=ev['zero_retention_envelope_certificates'],
            alpha=original.alpha,conditional_retention_audit=history,
            old_win_certified_zero=zero.tolist(),unresolved_histories=unresolved,
            original_unconditional_retention_upper=base['retention_regret_upper'],
            retention_regret_upper=retention_upper,retention_support_gap_upper=retention_support_upper)
        maximum=max(base['full_plan_regret_upper'],retention_upper)
        base['max_regret_upper']=None if unresolved else maximum
        base['bounded_checks_pass']=bool(not unresolved and maximum<=original.regret_tol and
            max(base['initial_support_gap_upper'],retention_support_upper)<=original.support_tol)
        return base

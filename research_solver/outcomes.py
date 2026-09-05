"""Variance-reduced, fixed-policy cost-grid comparisons (not price selection)."""
import math
import numpy as np
from rescue_solver.solver import ValueIntegratedEvaluator,Settings
from .evaluator import bernstein_radius


def completion_rates(model,m,p1,profile,counts):
    _,old,new=model._belief_objects(m,p1,profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain)
    evaluator=ValueIntegratedEvaluator(model,Settings())
    lengths,mid=evaluator.value_intervals(counts,p1,profile.q_values,old,new)
    completion=lengths[:,0,:].sum(axis=1)
    for iq,q in enumerate(profile.q_values):
        accept_old=model.par.beta*mid[:,None]-(p1+model.beta_detour)>1e-12
        accept_new=model.par.beta*mid[:,None]-(q+model.beta_detour)>1e-12
        log_none=counts @ (np.log(np.clip(1-old[iq],1e-14,1))*accept_old).T
        log_none-=accept_new @ new[iq]
        completion+=np.sum(lengths[:,iq+1,:]*(-np.expm1(log_none)),axis=1)
    return completion


def paired_count_comparison(model_a,model_b,m,menu_a,menu_b,n,seed,alpha=.05,draw_batch=10000):
    """Couple Poisson early counts via common min-intensity and independent excess.

    Each marginal has its exact intended count law. Rider value and hidden
    uncertainty are integrated out. This is NOT the raw-market paired
    simulator and does not replace the promised final raw-market report.
    """
    if n<2 or draw_batch<1 or not 0<alpha<1:raise ValueError('Invalid budget or alpha')
    if not np.array_equal(model_a.s,model_b.s) or not np.array_equal(model_a.fs,model_b.fs):
        raise ValueError('Cost-grid comparison requires identical route support')
    p_a,policy_a=menu_a;p_b,policy_b=menu_b
    la,_,_=model_a._belief_objects(m,p_a,policy_a.q_values,policy_a.sigma_e,policy_a.sigma_h,policy_a.retain)
    lb,_,_=model_b._belief_objects(m,p_b,policy_b.q_values,policy_b.sigma_e,policy_b.sigma_h,policy_b.retain)
    common=np.minimum(la,lb);rng=np.random.default_rng(seed)
    sums=np.zeros(4)
    for start in range(0,n,draw_batch):
        size=min(draw_batch,n-start)
        base=rng.poisson(common,size=(size,model_a.S))
        ca=base+rng.poisson(la-common,size=base.shape)
        cb=base+rng.poisson(lb-common,size=base.shape)
        states,mult=np.unique(np.column_stack([ca,cb]),axis=0,return_counts=True)
        for offset in range(0,len(states),256):
            st=states[offset:offset+256];w=mult[offset:offset+256]
            a=completion_rates(model_a,m,p_a,policy_a,st[:,:model_a.S])
            b=completion_rates(model_b,m,p_b,policy_b,st[:,model_a.S:])
            diff=a-b
            sums+=np.array([w @ a,w @ b,w @ diff,w @ (diff*diff)])
    mean=sums[2]/n;variance=max(0.,(sums[3]-n*mean*mean)/(n-1))
    se=math.sqrt(variance/n)
    radius=float(bernstein_radius(variance,2.,n,math.log(4/alpha)))
    return dict(completion_a=float(sums[0]/n),completion_b=float(sums[1]/n),
        difference_a_minus_b=float(mean),difference_se=se,
        normal_95_interval=[mean-1.96*se,mean+1.96*se],
        two_sided_Bernstein_interval=[mean-radius,mean+radius],alpha=alpha,
        count_pairs=n,seed=seed,draw_batch=draw_batch,
        method='Coupled early-count laws; rider values and hidden outcomes integrated',
        raw_market_report=False,price_optimized=False,wpbe_certified=False)

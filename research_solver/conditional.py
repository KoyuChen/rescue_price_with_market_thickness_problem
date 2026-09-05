"""Rao-Blackwell conditioning for rare old-driver information sets.

For a continuation price q, ANY early rival whose own immediate offer
dominates even the best hidden offer makes q impossible. Conditional on q,
all these independent Poisson counts must be zero. Integrate their zero
probability analytically and sample only the remaining counts. The common
factor cancels from Bayes' numerator and denominator. No event truncation.
"""
import math
import numpy as np
from .posterior import supported_hidden_offpath


def old_conditional_moments(evaluator,m,p1,profile,n,seed):
    if n<2:
        raise ValueError('At least two IID conditional draws required')
    model=evaluator.model; Q=len(profile.q_values)
    lam,old,new=model._belief_objects(m,p1,profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain)
    certified=supported_hidden_offpath(model,p1,profile.q_values,new)
    records=[]
    for iq,q in enumerate(profile.q_values):
        forbidden=certified[:,iq]
        reduced=lam.copy();reduced[forbidden]=0
        log_factor=-float(lam[forbidden].sum())
        draws=np.random.default_rng(seed+iq*104729).poisson(reduced,size=(n,model.S))
        counts,multiplicity=np.unique(draws,axis=0,return_counts=True)
        weights=multiplicity/n
        first=np.zeros((model.S,2));second=np.zeros((model.S,2,2))
        for start in range(0,len(counts),evaluator.settings.count_batch_size):
            c=counts[start:start+evaluator.settings.count_batch_size]
            w=weights[start:start+len(c)]
            for s in np.flatnonzero(~forbidden):
                tagged=c.copy();tagged[:,s]+=1
                lengths,mid=evaluator.value_intervals(tagged,p1,profile.q_values,old,new)
                d=lengths[:,iq+1,:].sum(axis=1)
                acceptable=model.par.beta*mid-(p1+model.beta_detour[s])>1e-12
                share=model._tag_selection_probability(c,np.ones(len(c)),p1,float(q),
                    float(model.s[s]),'old',old[iq],new[iq])
                b=share*(lengths[:,iq+1,:] @ acceptable)
                f=np.column_stack([d,b])
                first[s]+=w @ f
                second[s]+=np.einsum('n,nf,ng->fg',w,f,f)
        covariance=(second-np.einsum('sf,sg->sfg',first,first))*n/(n-1)
        records.append(dict(mean=first,covariance=covariance,log_probability_factor=log_factor,
            probability_factor=math.exp(log_factor),certified_offpath=forbidden,
            count_states=len(counts),count_draws=n))
    return records

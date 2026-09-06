"""Deterministic posterior bounds for rare on-support continuation histories.

The conditioning event may be far rarer than ordinary Monte Carlo can see.
Counts are compressed without changing the model: routes with positive old
retention at ANY rider action remain explicit; zero-retention routes matter
only through the best immediate fit and are integrated by their maximum; and
routes structurally incompatible with the target continuation are conditioned
to zero. Explicit-count Poisson tails remain as posterior interval error.
"""
import itertools
import math
import numpy as np
from research_solver.posterior import supported_hidden_offpath


def _compositions(total, dimensions):
    if dimensions == 0:
        if total == 0: yield ()
        return
    for bars in itertools.combinations(range(total+dimensions-1),dimensions-1):
        points=(-1,)+bars+(total+dimensions-1,)
        yield tuple(points[i+1]-points[i]-1 for i in range(dimensions))


def _poisson_total_tail(mean, cap):
    """Strict analytic upper bound; does not vanish by 1-CDF cancellation."""
    if mean == 0.: return 0.
    first=math.exp(-mean+(cap+1)*math.log(mean)-math.lgamma(cap+2))
    ratio=mean/(cap+2)
    if ratio >= 1.:
        # This routine is intended for a cap above the small explicit mean.
        # A Chernoff upper bound stays valid for accidental lower caps.
        bound=math.exp(-mean)*(math.e*mean/(cap+1))**(cap+1)
    else:
        bound=first/(1.-ratio)
    return float(np.nextafter(min(1.,bound),np.inf))


def compressed_old_posterior(evaluator,m,p1,profile,price_index,tag_route,
                             total_cap=20,batch_size=2048):
    model=evaluator.model; q_values=np.asarray(profile.q_values)
    if not 0 <= price_index < len(q_values) or not 0 <= tag_route < model.S:
        raise ValueError('Invalid price or route index')
    if total_cap < 0 or batch_size < 1:
        raise ValueError('Invalid enumeration budget')
    lam,old,new=model._belief_objects(m,p1,q_values,
        profile.sigma_e,profile.sigma_h,profile.retain)
    old=np.asarray(old);new=np.asarray(new)
    forbidden=supported_hidden_offpath(model,p1,q_values,new)[:,price_index]
    if forbidden[tag_route]:
        raise ValueError('Tagged history is already structurally off path')
    possible=~forbidden
    # Exact comparisons only. Arbitrarily small positive retention stays explicit.
    relevant=possible & np.any(old > 0.,axis=0)
    omitted=possible & ~relevant
    R=np.flatnonzero(relevant);O=np.flatnonzero(omitted)

    # Marginalize all omitted counts. Their continuation retention is exactly
    # zero, so only their highest occupied route can affect immediate utility.
    categories=[(None,math.exp(-float(lam[O].sum())))]
    for j in O:
        if lam[j] > 0:
            higher=O[O>j]
            probability=-math.expm1(-float(lam[j]))*math.exp(-float(lam[higher].sum()))
            categories.append((int(j),probability))
    category_mass=math.fsum(p for _,p in categories)
    if abs(category_mass-1.) > 5e-13:
        raise ArithmeticError('Maximum-route marginalization lost probability')

    log_lam=np.log(lam[R]) if len(R) else np.empty(0)
    log_base=-float(lam[R].sum())
    denominator=numerator=enumerated_mass=0.;states=0;buffer=[]
    def inspect(items):
        nonlocal denominator,numerator,enumerated_mass,states
        vectors=np.asarray([x[0] for x in items],dtype=int)
        rw=np.asarray([x[1] for x in items])
        base=np.zeros((len(items),model.S),dtype=int);base[:,R]=vectors
        enumerated_mass+=float(rw.sum());states+=len(items)
        for maximum,probability in categories:
            counts=base.copy()
            if maximum is not None: counts[:,maximum]=1
            tagged=counts.copy();tagged[:,tag_route]+=1
            lengths,mid=evaluator.value_intervals(tagged,p1,q_values,old,new)
            d=lengths[:,price_index+1,:].sum(axis=1)
            acceptable=model.par.beta*mid-(p1+model.beta_detour[tag_route])>1e-12
            share=model._tag_selection_probability(counts,np.ones(len(counts)),p1,
                float(q_values[price_index]),float(model.s[tag_route]),'old',
                old[price_index],new[price_index])
            b=share*(lengths[:,price_index+1,:]@acceptable)
            weight=rw*probability
            denominator+=float(weight@d);numerator+=float(weight@b)
    for total in range(total_cap+1):
        for vector in _compositions(total,len(R)):
            if len(R):
                logp=log_base+float(np.asarray(vector)@log_lam)-math.fsum(
                    math.lgamma(k+1) for k in vector)
                weight=math.exp(logp)
            else: weight=1.
            buffer.append((vector,weight))
            if len(buffer)==batch_size:inspect(buffer);buffer=[]
    if buffer:inspect(buffer)
    tail=_poisson_total_tail(float(lam[R].sum()),total_cap)
    if denominator <= 0:
        lower=0.;upper=1. if tail>0 else 0.;estimate=None
    else:
        estimate=numerator/denominator
        lower=numerator/(denominator+tail)
        upper=(numerator+tail)/(denominator+tail)
    factor=math.exp(-float(lam[forbidden].sum()))
    return dict(price_index=int(price_index),q=float(q_values[price_index]),
        tag_route=int(tag_route),relevant_routes=R.tolist(),
        marginalized_zero_retention_routes=O.tolist(),
        structurally_zero_routes=np.flatnonzero(forbidden).tolist(),
        explicit_count_cap=int(total_cap),explicit_count_states=int(states),
        explicit_count_mass=float(enumerated_mass),explicit_count_tail=float(tail),
        conditioned_zero_probability_factor=float(factor),
        conditional_event_measure_lower=float(denominator),
        conditional_event_measure_upper=float(denominator+tail),
        tagged_win_measure_lower=float(numerator),
        tagged_win_measure_upper=float(numerator+tail),
        conditional_win_probability_estimate=None if estimate is None else float(estimate),
        conditional_win_probability_lower=float(max(0.,lower)),
        conditional_win_probability_upper=float(min(1.,upper)),
        floating_point_verified=True,exact_arithmetic_certificate=False,
        count_tail_discarded=False)

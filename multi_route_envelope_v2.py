"""All-count exclusion when several early routes retain at the target price.

For the target continuation, replace its random retained early supply by a
certain offer on the best route with positive retention: this is an upper
bound. For each such route find a rival-count threshold at which immediate or
a lower continuation dominates that upper bound. Monotonicity then covers all
larger counts. The remaining finite rectangle is checked explicitly.
"""
import itertools
import numpy as np


def _threshold_check(model,p1,q_values,old,new,tag,coordinate,count,low,high,
                     safety_margin=1e-10):
    active=np.flatnonzero(np.asarray(old[high])>0.)
    if not len(active):return dict(passed=False,reason='no_positive_target_retention')
    best=int(active[np.argmin(model.beta_detour[active])])
    base=np.zeros((1,model.S),dtype=int);base[0,tag]+=1;base[0,coordinate]+=count
    occupied_best=tag if count == 0 else max(tag,coordinate)
    immediate_threshold=p1+model.par.ell*(1-model.s[occupied_best])
    go=p1+model.beta_detour;gl=q_values[low]+model.beta_detour
    gh=q_values[high]+model.beta_detour
    edges=np.unique(np.clip(np.r_[0.,1.,immediate_threshold,go/model.par.beta,
        gl/model.par.beta,gh/model.par.beta],0.,1.))
    retention=np.zeros(model.S);retention[best]=1.
    upper_counts=np.zeros((1,model.S),dtype=int);upper_counts[0,best]=1
    def values(v):
        v=np.asarray(v);counts=np.repeat(base,len(v),axis=0)
        upper=np.repeat(upper_counts,len(v),axis=0)
        immediate=np.maximum(v-immediate_threshold,0.)
        lower=model._expected_terminal_value(counts,v,p1,float(q_values[low]),old[low],new[low])
        target=model._expected_terminal_value(upper,v,p1,float(q_values[high]),retention,new[high])
        return immediate,lower,target
    immediate,lower,_=values(edges);difference=immediate-lower;crossings=[]
    for j in range(len(edges)-1):
        if difference[j]*difference[j+1]<0:
            crossings.append(edges[j]-difference[j]*(edges[j+1]-edges[j])/
                             (difference[j+1]-difference[j]))
    points=np.unique(np.r_[edges,crossings]);immediate,lower,target=values(points)
    gap=np.maximum(immediate,lower)-target;positive=target>1e-12
    passed=bool(np.all(gap>=0.) and np.all(gap[positive]>safety_margin))
    return dict(passed=passed,coordinate_route=int(coordinate),rival_count=int(count),
        certain_best_target_route=best,minimum_active_margin=float(gap[positive].min())
        if positive.any() else None,points=len(points),competitor_crossings=len(crossings))


def multi_route_count_exclusion(evaluator,p1,q_values,old,new,tag,low,high,
                                max_threshold=100,safety_margin=1e-10,max_states=250000):
    model=evaluator.model;active=np.flatnonzero(np.asarray(old[high])>0.)
    if not len(active):return dict(passed=False,reason='no_positive_target_retention')
    thresholds={};checks=[]
    for route in active:
        found=None
        for k in range(max_threshold+1):
            row=_threshold_check(model,p1,q_values,old,new,tag,int(route),k,low,high,safety_margin)
            if row['passed']:found=k;checks.append(row);break
        if found is None:
            return dict(passed=False,reason='threshold_not_found',active_routes=active.tolist(),
                active_target_retention_routes=active.tolist(),
                failed_route=int(route),max_threshold=int(max_threshold),threshold_checks=checks)
        thresholds[int(route)]=int(found)
    sizes=[thresholds[int(r)] for r in active]
    states=int(np.prod(sizes,dtype=object))
    if states > max_states:
        return dict(passed=False,reason='finite_rectangle_budget_exceeded',
                    required_states=states,max_states=max_states,
                    all_count_vectors_covered=False,threshold_checks=checks)
    maximum=0.;witness=None
    for vector in itertools.product(*[range(k) for k in sizes]):
        counts=np.zeros((1,model.S),dtype=int);counts[0,active]=vector;counts[0,tag]+=1
        lengths,_=evaluator.value_intervals(counts,p1,q_values,old,new)
        measure=float(lengths[0,high+1,:].sum())
        if measure>maximum:maximum=measure;witness=list(vector)
    return dict(passed=bool(maximum == 0.),tag_route=int(tag),
        comparator_price_index=int(low),target_price_index=int(high),
        active_target_retention_routes=active.tolist(),coordinate_thresholds=thresholds,
        threshold_checks=checks,finite_rectangle_states=states,
        maximum_target_interval=maximum,witness_counts=witness,
        all_other_routes_monotone_competitor_only=True,
        all_count_vectors_covered=True,floating_point_verified_with_margin=True,
        exact_arithmetic_certificate=False,enumeration_version=2)

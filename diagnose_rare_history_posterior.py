#!/usr/bin/env python3
"""Deterministic low-route enumeration for rare thick-market high histories."""
import json,math
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel,CachedEnvelopeEvaluator
from rescue_solver.config import build_model_params
from rescue_solver.core import Profile
from rescue_solver.solver import Settings

root=Path('runs/thick_checkpointed_20260905')
request=json.loads((root/'request.json').read_text())
with np.load(root/'support.npz',allow_pickle=False) as z:
    model=VectorizedTieModel(build_model_params(request['model']),
        *[z[k] for k in ('c','fc','s','fs')])
x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
evaluator=CachedEnvelopeEvaluator(model,Settings(train_counts=2,audit_counts=2))
rows=[]

for m,p1,p2,tags in ((6,.30,.49,(0,1)),(12,.23,.46,(1,)),(24,.17,.36,(3,))):
    with np.load(root/f'm{m}/menu_00000/checkpoint.npz',allow_pickle=False) as z:
        profile=Profile(z['sigma_e'].copy(),z['sigma_h'].copy(),z['retain'].copy(),z['q_values'].copy(),{})
    lam,old,new=model._belief_objects(m,p1,profile.q_values,profile.sigma_e,profile.sigma_h,profile.retain)
    for tag in tags:
        routes=np.arange(tag+1); grids=np.indices((21,)*len(routes)).reshape(len(routes),-1).T
        den=num=mass=0.; positive=0
        for start in range(0,len(grids),4096):
            g=grids[start:start+4096];counts=np.zeros((len(g),model.S),dtype=np.int16);counts[:,routes]=g
            logp=np.sum(g*np.log(lam[routes]+1e-300)-np.vectorize(math.lgamma)(g+1),axis=1)-lam[routes].sum()
            weight=np.exp(logp);tagged=counts.copy();tagged[:,tag]+=1
            lengths,mid=evaluator.value_intervals(tagged,p1,profile.q_values,old,new)
            d=lengths[:,2,:].sum(axis=1)
            share=model._tag_selection_probability(counts,np.ones(len(counts)),p1,p2,float(model.s[tag]),'old',old[1],new[1])
            acceptable=model.par.beta*mid-(p1+model.beta_detour[tag])>1e-12
            b=share*(lengths[:,2,:]@acceptable)
            den+=weight@d;num+=weight@b;mass+=weight.sum();positive+=int(np.sum(d>0))
        pi=num/den if den else None
        cutoff=model.par.delta*p1-model.par.omega_old/pi if pi else None
        row=dict(m=m,tag_route=tag,routes_enumerated=routes.tolist(),max_each=20,
            probability_mass=mass,positive_states=positive,event_measure=den,
            tagged_win_measure=num,conditional_win_probability=pi,
            generalized_cost_retention_cutoff=cutoff,
            scope='Reduced-route diagnostic; not yet a certified full-count posterior')
        rows.append(row);print(json.dumps(row),flush=True)

(root/'rare_history_posterior_diagnostic.json').write_text(json.dumps(dict(rows=rows),indent=2)+'\n')

#!/usr/bin/env python3
"""Enumerate low rival-count states behind unresolved thick-market histories.

Read-only diagnostic: active runs and checkpoints are never modified. Counts on
routes already proved to make the high continuation impossible are fixed at
zero. All weak compositions up to --total are checked on the remaining routes.
"""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel, CachedEnvelopeEvaluator
from research_solver.posterior import supported_hidden_offpath
from rescue_solver.config import build_model_params
from rescue_solver.core import Profile
from rescue_solver.solver import Settings


def compositions(total, dimensions):
    for bars in itertools.combinations(range(total + dimensions - 1), dimensions - 1):
        points = (-1,) + bars + (total + dimensions - 1,)
        yield tuple(points[i + 1] - points[i] - 1 for i in range(dimensions))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default='runs/thick_checkpointed_20260905')
    ap.add_argument('--total', type=int, default=10)
    ap.add_argument('--batch', type=int, default=2048)
    args = ap.parse_args(); root = Path(args.root)
    request = json.loads((root/'request.json').read_text())
    with np.load(root/'support.npz', allow_pickle=False) as z:
        model = VectorizedTieModel(build_model_params(request['model']),
            *[z[k] for k in ('c','fc','s','fs')])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    evaluator=CachedEnvelopeEvaluator(model,Settings(train_counts=2,audit_counts=2))
    cases=((6,.30,.49),(12,.23,.46),(24,.17,.36))
    rows=[]
    for m,p1,p2 in cases:
        with np.load(root/f'm{m}/menu_00000/checkpoint.npz',allow_pickle=False) as z:
            profile=Profile(z['sigma_e'].copy(),z['sigma_h'].copy(),
                z['retain'].copy(),z['q_values'].copy(),{})
        lam,old,new=model._belief_objects(m,p1,profile.q_values,
            profile.sigma_e,profile.sigma_h,profile.retain)
        possible=np.flatnonzero(~supported_hidden_offpath(model,p1,profile.q_values,new)[:,1])
        unknown=[0,1] if m==6 else ([1] if m==12 else [3])
        for tag in unknown:
            checked=0;positive=[];maximum=0.;argmax=None;buffer=[]
            def inspect(chunk):
                nonlocal checked,maximum,argmax
                counts=np.zeros((len(chunk),model.S),dtype=np.int16)
                counts[:,possible]=np.asarray(chunk,dtype=np.int16)
                counts[:,tag]+=1
                lengths,_=evaluator.value_intervals(counts,p1,profile.q_values,old,new)
                high=lengths[:,2,:].sum(axis=1);checked+=len(chunk)
                j=int(np.argmax(high))
                if high[j]>maximum: maximum=float(high[j]);argmax=chunk[j]
                for i in np.flatnonzero(high>0):
                    if len(positive)<10:positive.append(dict(counts=chunk[int(i)],length=float(high[i])))
            for total in range(args.total+1):
                for c in compositions(total,len(possible)):
                    buffer.append(c)
                    if len(buffer)==args.batch:inspect(buffer);buffer=[]
            if buffer:inspect(buffer)
            row=dict(m=m,tag_route=tag,possible_routes=possible.tolist(),max_total=args.total,
                states_checked=checked,positive_states=positive,maximum_high_interval=maximum,
                argmax_counts=argmax)
            rows.append(row);print(json.dumps(row),flush=True)
    out=root/'thick_history_support_diagnostic.json'
    out.write_text(json.dumps(dict(rows=rows),indent=2)+'\n')

if __name__=='__main__':main()

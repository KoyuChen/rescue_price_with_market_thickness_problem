#!/usr/bin/env python3
"""Freeze active thick profiles and bound rare on-support posteriors exactly.

Read-only with respect to the active run. The snapshot, support and request are
copied to a separate output before calculation. This is posterior evidence for
frozen profiles, not an equilibrium audit or a completed outer-price result.
"""
import argparse
import datetime
import fcntl
import json
from pathlib import Path
import shutil
import numpy as np
from accelerated_evaluator import VectorizedTieModel,CachedEnvelopeEvaluator
from rare_history_enumeration import compressed_old_posterior
from multi_route_envelope import multi_route_count_exclusion
from rescue_solver.config import build_model_params
from rescue_solver.core import Profile
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json,digest
from run_research import check_source,source_identity

CASES=((6,.30,.49),(12,.23,.46),(24,.17,.36))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',default='runs/thick_checkpointed_20260905')
    ap.add_argument('--output',required=True)
    ap.add_argument('--count-cap-m6',type=int,default=12)
    ap.add_argument('--count-cap-m12',type=int,default=18)
    ap.add_argument('--count-cap-m24',type=int,default=12)
    args=ap.parse_args();source=Path(args.source).resolve();output=Path(args.output).resolve()
    if output==source or source in output.parents:ap.error('Output must be outside active run')
    output.mkdir(parents=True,exist_ok=True)
    with (output/'runner.lock').open('a+') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Certification already running')
        request=json.loads((source/'request.json').read_text());check_source(request['source_identity'])
        for name in ('request.json','support.npz'):
            target=output/name
            if target.exists():
                if digest(target)!=digest(source/name):raise ValueError('Frozen input mismatch')
            else:shutil.copy2(source/name,target)
        snapshots={}
        for m,_,_ in CASES:
            src=source/f'm{m}/menu_00000/checkpoint.npz';target=output/f'm{m}_checkpoint.npz'
            if not target.exists():shutil.copy2(src,target)
            snapshots[str(m)]=dict(source=str(src),source_sha256=digest(src),
                frozen_sha256=digest(target))
            if snapshots[str(m)]['source_sha256'] != snapshots[str(m)]['frozen_sha256']:
                # The source may advance after copy; the frozen copy remains valid,
                # but never mislabel it as the later active checkpoint.
                snapshots[str(m)]['source_advanced_during_copy']=True
        identity=source_identity()
        for name in ('accelerated_evaluator.py','history_envelope.py',
                     'rare_history_enumeration.py','multi_route_envelope.py',
                     'certify_thick_rare_histories.py'):
            identity['sha256'][name]=digest(Path(__file__).resolve().parent/name)
        base_request=dict(source=str(source),source_request_sha256=digest(output/'request.json'),
            support_sha256=digest(output/'support.npz'),snapshots=snapshots,
            count_caps={'6':args.count_cap_m6,'12':args.count_cap_m12,
                        '24':args.count_cap_m24},source_identity=identity,
            scope='Frozen-profile posterior bounds; not equilibrium or outer-price acceptance')
        if (output/'certification_request.json').exists():
            run_request=json.loads((output/'certification_request.json').read_text())
            if {k:v for k,v in run_request.items() if k!='observed_utc'} != base_request:
                raise ValueError('Certification request changed')
        else:
            run_request=dict(observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**base_request)
            atomic_write_json(output/'certification_request.json',run_request)
        with np.load(output/'support.npz',allow_pickle=False) as z:
            model=VectorizedTieModel(build_model_params(request['model']),
                *[z[k] for k in ('c','fc','s','fs')])
        x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
        evaluator=CachedEnvelopeEvaluator(model,Settings(train_counts=50000,audit_counts=1000000))
        rows=[]
        for m,p1,p2 in CASES:
            with np.load(output/f'm{m}_checkpoint.npz',allow_pickle=False) as z:
                profile=Profile(z['sigma_e'].copy(),z['sigma_h'].copy(),
                    z['retain'].copy(),z['q_values'].copy(),{})
            ev=evaluator.evaluate(m,p1,p2,profile,50000,2026090609+m)
            for tag,iq in np.argwhere(ev['unknown_old_history']):
                if not np.any(model.a[:,tag]<=p1+1e-12):continue
                exclusion=multi_route_count_exclusion(evaluator,p1,profile.q_values,
                    ev['old_r'],ev['lambda_new'],int(tag),0,int(iq)) if iq>0 else {'passed':False}
                if exclusion['passed']:
                    row=dict(m=m,p1=p1,p2=p2,price_index=int(iq),
                        q=float(profile.q_values[iq]),tag_route=int(tag),
                        structurally_off_path=True,multi_route_count_exclusion=exclusion)
                    rows.append(row);print(json.dumps(row),flush=True);continue
                cap=run_request['count_caps'][str(m)]
                row=compressed_old_posterior(evaluator,m,p1,profile,int(iq),int(tag),cap)
                pi=row['conditional_win_probability_estimate']
                margin=None if pi is None or pi==0 else model.par.delta*p1-model.par.omega_old/pi
                row.update(m=m,p1=p1,p2=p2,
                    generalized_cost_retention_cutoff_estimate=None if margin is None else float(margin))
                rows.append(row);print(json.dumps(row),flush=True)
        atomic_write_json(output/'posterior_bounds.json',dict(rows=rows,
            all_count_tails_retained=True,active_run_modified=False,
            equilibrium_audit_completed=False,outer_price_optimized=False))


if __name__=='__main__':main()

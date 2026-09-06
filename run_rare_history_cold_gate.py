#!/usr/bin/env python3
"""Independent cold-homotopy repair of thick validation menus, not price search.

Original active outputs are never edited. Frozen legacy checkpoints are saved
only as diagnostic evidence, never used to initialize the repaired profiles.
Repeat the identical command only after checking processes and runner.lock.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import asdict
import datetime
import fcntl
import json
import math
import os
from pathlib import Path
import shutil
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from rare_history_checkpoint_solver import solve_checkpointed
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json,digest,save_profile
from rescue_solver.cli import clean_json
from run_research import source_identity,check_source

ROOT=Path(__file__).resolve().parent
MENUS={6:(.30,.49),12:(.23,.46),24:(.17,.36)}
DEPENDENCIES=('accelerated_evaluator.py','history_envelope.py','zero_retention_envelope.py',
    'rare_history_enumeration_v2.py','multi_route_envelope_v2.py','rare_history_evaluator.py',
    'rare_history_checkpoint_solver.py','run_rare_history_cold_gate.py')

def worker(task):
    output,m,request=task;output=Path(output);d=output/f'm{m}';d.mkdir(exist_ok=True)
    check_source(request['source_identity'])
    if digest(output/'support.npz')!=request['support_sha256']:raise ValueError('Support changed')
    with np.load(output/'support.npz',allow_pickle=False) as z:
        model=VectorizedTieModel(build_model_params(request['model']),*[z[k] for k in ('c','fc','s','fs')])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    settings=Settings(**request['settings'][str(m)])
    def log(row):
        event=clean_json(dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),m=m,**row))
        with (d/'progress.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
        print(json.dumps({k:v for k,v in event.items() if k!='rare_history_resolution'}),flush=True)
    log(dict(stage='worker_started',pid=os.getpid(),cold_rule='common_homotopy'))
    target=d/'result.json'
    if target.exists():
        result=json.loads(target.read_text())
        if result['source_identity']!=request['source_identity'] or digest(d/'profile.npz')!=result['profile_sha256']:
            raise ValueError('Completed result provenance changed')
    else:
        profile,result=solve_checkpointed(model,m,*MENUS[m],settings,d/'checkpoint.npz',
                                         request['source_identity'],log)
        check_source(request['source_identity'])
        save_profile(d/'profile.npz',profile)
        result.update(source_identity=request['source_identity'],profile_sha256=digest(d/'profile.npz'),
            cost_points=model.C,route_points=model.S,tie_quadrature_order=64,
            support_sha256=request['support_sha256'],original_run=request['source_run'],
            diagnostic_snapshot_sha256=request['diagnostic_snapshot_sha256'][str(m)],
            original_checkpoint_used_for_initialization=False,fixed_menu_only=True)
        atomic_write_json(target,clean_json(result))
    row=dict(m=m,p1=result['p1'],p2=result['p2'],passed=result['numerical_checks_passed'],
             unknown=result['unknown_training_histories'],result=str(target))
    log(dict(stage='gate_finished',**{k:v for k,v in row.items() if k!='m'}));return row

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-run',default='runs/thick_checkpointed_20260905')
    ap.add_argument('--output',required=True)
    ap.add_argument('--m',nargs='+',type=int,choices=sorted(MENUS),default=[6,12,24])
    ap.add_argument('--workers',type=int,default=3)
    args=ap.parse_args();source=Path(args.source_run).resolve();out=Path(args.output).resolve()
    if args.workers<1 or len(set(args.m))!=len(args.m):ap.error('Invalid workers or duplicate thicknesses')
    if source==out or source in out.parents:ap.error('Independent output required')
    out.mkdir(parents=True,exist_ok=True)
    with (out/'runner.lock').open('a+') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Repair gate already running')
        if (out/'request.json').exists():
            request=json.loads((out/'request.json').read_text())
            if request['source_run']!=str(source) or request['m']!=args.m:raise ValueError('Request changed')
        else:
            prior=json.loads((source/'request.json').read_text());check_source(prior['source_identity'])
            if digest(source/'support.npz')!=prior['support_sha256']:raise ValueError('Source support mismatch')
            identity=source_identity()
            for name in DEPENDENCIES:identity['sha256'][name]=digest(ROOT/name)
            shutil.copy2(source/'support.npz',out/'support.npz')
            shutil.copy2(source/'request.json',out/'original_request.json')
            snapshots={};settings={}
            for m in args.m:
                dst=out/f'm{m}_original_diagnostic_checkpoint.npz'
                shutil.copy2(source/f'm{m}/menu_00000/checkpoint.npz',dst);snapshots[str(m)]=digest(dst)
                seed=int(np.random.SeedSequence([prior['seed'],m,0,0]).generate_state(1,dtype=np.uint64)[0])
                settings[str(m)]=asdict(Settings(train_counts=50000,audit_counts=1000000,count_batch_size=64,
                    seed=seed,alpha=.05*6/(math.pi**2*len(prior['m'])*2),
                    schedule=((.02,40,.35),(.004,60,.25),(.0005,100,.15),(0.,500,.1))))
            request=clean_json(dict(m=args.m,source_run=str(source),model=prior['model'],
                support_sha256=digest(out/'support.npz'),source_identity=identity,settings=settings,
                diagnostic_snapshot_sha256=snapshots,original_request_sha256=digest(out/'original_request.json'),
                common_cold_homotopy=True,original_checkpoint_used_for_initialization=False,
                outer_price_optimized=False,active_run_modified=False))
            atomic_write_json(out/'request.json',request)
        check_source(request['source_identity'])
        atomic_write_json(out/'supervisor.json',dict(pid=os.getpid(),status='running'))
        rows=[]
        with ProcessPoolExecutor(max_workers=min(args.workers,len(args.m))) as pool:
            jobs=[pool.submit(worker,(str(out),m,request)) for m in args.m]
            for job in as_completed(jobs):
                rows.append(job.result());atomic_write_json(out/'progress_summary.json',dict(rows=rows))
        atomic_write_json(out/'summary.json',dict(rows=rows,all_gates_passed=all(r['passed'] for r in rows),
            outer_price_optimized=False,active_run_modified=False))
        atomic_write_json(out/'supervisor.json',dict(pid=os.getpid(),status='finished'))

if __name__=='__main__':main()

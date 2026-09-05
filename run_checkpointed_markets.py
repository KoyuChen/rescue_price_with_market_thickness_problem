#!/usr/bin/env python3
"""Independent restartable runner. Never overwrites the original run or sources.

Use the same command to resume this output. An exclusive advisory lock rejects
duplicate supervisors; policies, completed audits and menu results are reused
only with identical source/input hashes. Lost pre-checkpoint work must restart.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
import fcntl
import json
import math
import os
from pathlib import Path
import shutil
import numpy as np
from rescue_solver.core import FixedSupportRescueModel
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, save_profile, load_profile, digest
from rescue_solver.cli import clean_json
from run_research import check_source
from run_thick_markets import BENCHMARKS, global_menus, local_menus
from checkpoint_solver import solve_checkpointed

ROOT = Path(__file__).resolve().parent


def worker(task):
    root, m, request = task; root = Path(root); directory = root/f'm{m:g}'
    directory.mkdir(exist_ok=True)
    check_source(request['source_identity'])
    if digest(root/'support.npz') != request['support_sha256']:
        raise ValueError('Support checksum mismatch')
    with np.load(root/'support.npz', allow_pickle=False) as d:
        model = FixedSupportRescueModel(build_model_params(request['model']),
                                       d['c'], d['fc'], d['s'], d['fs'])
    x, w = np.polynomial.legendre.leggauss(64); model.tie_t=(x+1)/2; model.tie_w=w/2
    def log(data):
        event = clean_json(dict(data, m=m))
        print(json.dumps(event), flush=True)
        with (directory/'progress.jsonl').open('a') as f: f.write(json.dumps(event)+'\n')
    log(dict(stage='worker_started', pid=os.getpid()))
    rows=[]; done={}
    def evaluate_menu(p1, p2, stage):
        if (p1,p2) in done: return done[(p1,p2)]
        ordinal=len(rows); menu_dir=directory/f'menu_{ordinal:05d}'; menu_dir.mkdir(exist_ok=True)
        alpha=.05*6/(math.pi**2*len(request['m'])*2*(ordinal+1)**2)
        settings=Settings(train_counts=50000,audit_counts=1000000,count_batch_size=64,
            seed=int(np.random.SeedSequence([request['seed'],int(m),ordinal,0]).generate_state(1,dtype=np.uint64)[0]),
            alpha=alpha,schedule=((.02,40,.35),(.004,60,.25),(.0005,100,.15),(0.,500,.1)))
        check_source(request['source_identity'])
        if (menu_dir/'result.json').exists():
            result=json.loads((menu_dir/'result.json').read_text())
            if (result['m'],result['p1'],result['p2'],result['phase']) != (m,p1,p2,stage):
                raise ValueError('Stored menu order mismatch')
            if result['source_identity'] != request['source_identity'] or result['settings'] != clean_json(asdict(settings)):
                raise ValueError('Stored menu provenance mismatch')
            if digest(menu_dir/'profile.npz') != result['profile_sha256']:
                raise ValueError('Stored profile checksum mismatch')
        else:
            log(dict(stage='menu_started',phase=stage,ordinal=ordinal,p1=p1,p2=p2,
                     resume=(menu_dir/'checkpoint.npz').exists()))
            profile,result=solve_checkpointed(model,m,p1,p2,settings,menu_dir/'checkpoint.npz',
                request['source_identity'],lambda r:log(dict(p1=p1,p2=p2,**r)))
            check_source(request['source_identity'])
            save_profile(menu_dir/'profile.npz',profile)
            result.update(source_identity=request['source_identity'],profile_sha256=digest(menu_dir/'profile.npz'),
                          cost_points=model.C,route_points=model.S,phase=stage)
            atomic_write_json(menu_dir/'result.json',clean_json(result))
            log(dict(stage='menu_finished',p1=p1,p2=p2,passed=result['numerical_checks_passed']))
        row=dict(m=m,p1=p1,p2=p2,passed=result['numerical_checks_passed'],directory=str(menu_dir),
                 score=None,profile_sha256=result['profile_sha256'])
        if (menu_dir/'selection.json').exists():
            selection=json.loads((menu_dir/'selection.json').read_text())
            if selection['profile_sha256'] != row['profile_sha256']: raise ValueError('Selection checksum mismatch')
            row['score']=selection['score']
        rows.append(row); done[(p1,p2)]=row
        return row
    for menu in BENCHMARKS[m]: evaluate_menu(*menu,'validation_gate')
    if not all(r['passed'] for r in rows):
        summary=dict(m=m,status='gate_blocked',rows=rows,price_search_started=False,
            reason='Unresolved inner incentives; preserve failed candidates and diagnose.',wpbe_certified=False)
        atomic_write_json(directory/'summary.json',summary); log(summary); return summary
    def score_rows():
        for ordinal,row in enumerate(rows):
            if row['score'] is not None: continue
            p=load_profile(Path(row['directory'])/'profile.npz'); case=(row['p1'],row['p2'],p)
            seed=int(np.random.SeedSequence([request['seed'],int(m),ordinal,1]).generate_state(1,dtype=np.uint64)[0])
            out,_,_=model.paired_evaluate(m,case,case,2000000,seed)
            row['score']=out['completion']
            atomic_write_json(Path(row['directory'])/'selection.json',dict(markets=2000000,score=row['score'],
                seed=seed,profile_sha256=row['profile_sha256'],independent_of_training_and_audit=True))
        atomic_write_json(directory/'candidates.json',rows)
    for p1,p2 in global_menus(): evaluate_menu(p1,p2,'global')
    score_rows()
    for step,radius,top in ((.02,.08,5),(.01,.03,4),(.005,.01,3),(.0025,.005,3)):
        leaders=sorted(rows,key=lambda r:(-r['score'],r['p1'],r['p2']))[:top]
        for p1,p2 in local_menus(leaders,step,radius): evaluate_menu(p1,p2,f'refine_{step}')
        score_rows()
    rescue=max(rows,key=lambda r:r['score']); flat=max((r for r in rows if r['p1']==r['p2']),key=lambda r:r['score'])
    summary=dict(m=m,status='price_search_finished',rescue=rescue,flat=flat,
        all_candidates_passed=all(r['passed'] for r in rows),price_search_started=True,
        candidate_count=len(rows),wpbe_certified=False,continuous_global_optimum_proved=False,
        type_route_convergence_verified=False,optimized_V_certified=False)
    if rescue['passed'] and flat['passed']:
        a=(rescue['p1'],rescue['p2'],load_profile(Path(rescue['directory'])/'profile.npz'))
        b=(flat['p1'],flat['p2'],load_profile(Path(flat['directory'])/'profile.npz'))
        r,f,comparison=model.paired_evaluate(m,a,b,10000000,request['seed']+900000003+int(m)*100003)
        summary.update(rescue_outcome=r,flat_outcome=f,comparison=comparison,report_markets=10000000)
    atomic_write_json(directory/'summary.json',clean_json(summary)); return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-run',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.workers<1: parser.error('Positive worker count required')
    source=Path(args.source_run).resolve(); root=Path(args.output).resolve()
    if source==root: parser.error('Original run must remain immutable')
    root.mkdir(parents=True,exist_ok=True)
    with (root/'runner.lock').open('a+') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise SystemExit('Output already has an active supervisor; not starting')
        if (root/'request.json').exists():
            request=json.loads((root/'request.json').read_text())
            if request['interrupted_source_run']!=str(source): raise ValueError('Source run mismatch')
        else:
            request=json.loads((source/'request.json').read_text())
            check_source(request['source_identity'])
            if digest(source/'support.npz')!=request['support_sha256']: raise ValueError('Original support checksum mismatch')
            request['interrupted_source_run']=str(source)
            request['recovery_note']='Original four processes disappeared before any policy checkpoint. Cold restart with per-update checkpoints; not an exact resume of old iterations.'
            for name in ('checkpoint_solver.py','run_checkpointed_markets.py'):
                request['source_identity']['sha256'][name]=digest(ROOT/name)
            shutil.copyfile(source/'support.npz',root/'support.npz')
            atomic_write_json(root/'request.json',request)
        check_source(request['source_identity'])
        results=[]; pending=[]
        for m in request['m']:
            path=root/f'm{m:g}'/'summary.json'
            if path.exists(): results.append(json.loads(path.read_text()))
            else: pending.append(m)
        atomic_write_json(root/'supervisor.json',dict(pid=os.getpid(),pending=pending,completed=[r['m'] for r in results]))
        with ProcessPoolExecutor(max_workers=min(args.workers,max(1,len(pending)))) as pool:
            futures=[pool.submit(worker,(str(root),m,request)) for m in pending]
            for future in as_completed(futures):
                results.append(future.result())
                atomic_write_json(root/'progress_summary.json',clean_json(dict(completed=results)))
        atomic_write_json(root/'summary.json',clean_json(dict(results=results,wpbe_certified=False)))


if __name__=='__main__': main()

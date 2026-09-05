#!/usr/bin/env python3
"""m=3 global price search after the reactivated fixed-menu validation gate.

Common homotopy cold starts for EVERY searched menu. Fixed-menu warm-refinement
results are gate evidence only, not reused as outer-search branch selections.
"""
import argparse
from dataclasses import asdict
import fcntl
import json
import math
import os
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel as FixedSupportRescueModel
from accelerated_checkpoint_solver import solve_checkpointed
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, save_profile, load_profile, digest
from rescue_solver.cli import clean_json
from run_research import check_source, source_identity
from run_thick_markets import global_menus, local_menus

ROOT=Path(__file__).resolve().parent
BENCHMARKS={3.:((.365,.535),(.37,.37))}

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
    parser.add_argument('--gate-root',required=True)
    parser.add_argument('--model-request',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seed',type=int,default=2026090619)
    args=parser.parse_args()
    gate=Path(args.gate_root).resolve();root=Path(args.output).resolve()
    if root==gate or gate in root.parents:parser.error('Use a separate search output')
    evidence={}
    for name in ('m3_rescue','m3_flat'):
        directory=gate/name
        result=json.loads((directory/'result.json').read_text())
        check_source(result['source_identity'])
        if not result['numerical_checks_passed'] or result['m']!=3.:
            raise ValueError('The m=3 gate has not passed')
        if digest(directory/'profile.npz')!=result['profile_sha256']:
            raise ValueError('Gate profile checksum mismatch')
        evidence[name]=dict(result_sha256=digest(directory/'result.json'),
            profile_sha256=result['profile_sha256'],status=result['status'])
    support=json.loads((gate/'m3_rescue/support.json').read_text())
    if support!=json.loads((gate/'m3_flat/support.json').read_text()):
        raise ValueError('Gate supports do not match')
    params=json.loads(Path(args.model_request).read_text())['config']['model']
    params=dict(params,cost_probability_edges=[0.]+np.cumsum(support['fc']).tolist())
    params['cost_probability_edges'][-1]=1.
    root.mkdir(parents=True,exist_ok=True)
    with (root/'runner.lock').open('a+') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Search already running')
        identity=source_identity()
        for name in ('run_accelerated_m3_search.py','accelerated_checkpoint_solver.py',
                     'accelerated_evaluator.py','history_envelope.py','run_thick_markets.py'):
            identity['sha256'][name]=digest(ROOT/name)
        request=clean_json(dict(m=[3.],model=params,seed=args.seed,
            source_identity=identity,gate_evidence=evidence,
            gate_root=str(gate),cost_points=len(support['c']),route_points=len(support['s']),
            cold_start_rule='Common homotopy on the full search support for every price menu',
            rescue_global_step=.05,flat_global_step=.0025,
            fixed_menu_gate_is_not_an_outer_optimum=True))
        if (root/'request.json').exists():
            stored=json.loads((root/'request.json').read_text())
            if {k:v for k,v in stored.items() if k!='support_sha256'}!=request:
                raise ValueError('Search source or input mismatch')
            request=stored
            if digest(root/'support.npz')!=request['support_sha256']:
                raise ValueError('Stored support mismatch')
        else:
            np.savez_compressed(root/'support.npz',**{k:np.array(v) for k,v in support.items()})
            request['support_sha256']=digest(root/'support.npz')
            atomic_write_json(root/'request.json',request)
        atomic_write_json(root/'supervisor.json',dict(pid=os.getpid(),status='running',m=3.))
        result=worker((str(root),3.,request))
        atomic_write_json(root/'summary.json',clean_json(result))
        atomic_write_json(root/'supervisor.json',dict(pid=os.getpid(),status='finished',m=3.))


if __name__=='__main__':main()

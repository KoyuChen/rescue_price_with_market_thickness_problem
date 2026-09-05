#!/usr/bin/env python3
"""Research validation gate. No price search may treat fixed test menus as optima."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace
import json
from pathlib import Path
import platform
import time
import numpy as np
from rescue_solver.cli import create_model, clean_json
from rescue_solver.config import load_config
from rescue_solver.storage import digest, atomic_write_json, save_profile
from research_solver.solve import RESEARCH_SETTINGS, solve

ROOT = Path(__file__).resolve().parent
GATE_MENUS = ((1.,.45,.45),(1.,.425,.49),(3.,.37,.37),(3.,.365,.535))


def source_identity():
    paths = [ROOT/'run_research.py']
    for directory in ('rescue_solver','research_solver'):
        paths += sorted((ROOT/directory).rglob('*.py'))
    return dict(sha256={str(p.relative_to(ROOT)):digest(p) for p in paths},
                python=platform.python_version(),numpy=np.__version__)


def check_source(identity):
    for path, expected in identity['sha256'].items():
        if digest(ROOT/path)!=expected:
            raise RuntimeError('Source changed during calculation: '+path)


def gate_worker(task):
    m,p1,p2,config,output,route_seed,seed,identity=task
    model=create_model(config,route_seed)
    x,w=np.polynomial.legendre.leggauss(32)
    model.tie_t=(x+1)/2; model.tie_w=w/2
    directory=Path(output)/f'm{m:g}_p{p1:.3f}_{p2:.3f}'
    directory.mkdir(parents=True,exist_ok=False)
    settings=replace(RESEARCH_SETTINGS,seed=seed,alpha=.05/8)
    def progress(row):
        event=dict(m=m,p1=p1,p2=p2,**row)
        print(json.dumps(clean_json(event),allow_nan=False),flush=True)
        with (directory/'progress.jsonl').open('a') as f:
            f.write(json.dumps(clean_json(event),allow_nan=False)+'\n')
    started=time.monotonic()
    profile,result=solve(model,m,p1,p2,settings,progress)
    check_source(identity)
    save_profile(directory/'profile.npz',profile)
    profile_data={k:getattr(profile,k).tolist() for k in ('sigma_e','sigma_h','retain','q_values')}
    profile_data['meta']=profile.meta
    atomic_write_json(directory/'profile.json',clean_json(profile_data))
    result.update(elapsed_seconds=time.monotonic()-started,source_identity=identity,
        profile_sha256=digest(directory/'profile.npz'),route_seed=route_seed,
        cost_points=model.C,route_points=model.S,tie_quadrature_order=32,
        fixed_menu_validation=True,not_a_price_search_result=True)
    atomic_write_json(directory/'result.json',clean_json(result))
    print(json.dumps(dict(stage='menu_finished',m=m,p1=p1,p2=p2,status=result['status']),allow_nan=False),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--config',default=str(ROOT/'configs/research.json'))
    parser.add_argument('--route-seed',type=int,default=20260904)
    parser.add_argument('--seed',type=int,default=2026090601)
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    if args.workers<1 or args.route_seed<0 or args.seed<0:
        parser.error('Positive worker count and nonnegative seeds required')
    output=Path(args.output).resolve(); output.mkdir(parents=True,exist_ok=False)
    config=load_config(args.config); identity=source_identity()
    model=create_model(config,args.route_seed)
    atomic_write_json(output/'request.json',dict(stage='fixed_menu_validation_gate',
        menus=GATE_MENUS,target_thicknesses=[1,3,6,12,24,48],config=config,
        settings=asdict(replace(RESEARCH_SETTINGS,seed=args.seed)),route_seed=args.route_seed,
        source_identity=identity,workers=args.workers,
        next_search=dict(rescue_global_step=.05,refine_steps=[.02,.01,.005],
            flat_global_step=.005,rerank_markets=500000,report_markets=2000000),
        gate_is_not_type_or_price_convergence_certificate=True))
    atomic_write_json(output/'support.json',{k:getattr(model,k).tolist() for k in ('c','fc','s','fs')})
    tasks=[(*menu,config,str(output),args.route_seed,args.seed,identity) for menu in GATE_MENUS]
    with ProcessPoolExecutor(max_workers=min(args.workers,4)) as pool:
        results=list(pool.map(gate_worker,tasks))
    ready=all(r['numerical_checks_passed'] for r in results)
    summary=dict(stage='gate_finished',fixed_menu_gate_passed=ready,
        high_precision_search_started=False,optimized_prices_available=False,
        rows=[dict(m=r['m'],p1=r['p1'],p2=r['p2'],status=r['status'],
            audit_full_plan_upper=[a['full_plan_regret_upper'] for a in r['audits']],
            audit_retention_upper=[a['retention_regret_upper'] for a in r['audits']],
            unresolved_histories=[len(a['unresolved_histories']) for a in r['audits']]) for r in results],
        next_action='Check support/quadrature robustness and run price search' if ready else
                    'Repair remaining diagnosed failures before expanding thickness',
        wpbe_certified=False)
    atomic_write_json(output/'summary.json',summary)
    print(json.dumps(summary,allow_nan=False),flush=True)
    return 0 if ready else 2


if __name__=='__main__': raise SystemExit(main())

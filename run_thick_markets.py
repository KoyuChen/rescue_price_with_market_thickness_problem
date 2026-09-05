#!/usr/bin/env python3
"""Parallel thick-market gates followed by high-precision price search.

Every thickness has its own gate. A failed gate blocks that thickness's
price search, not the independently running other thicknesses.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace,asdict
import json
import math
from pathlib import Path
import numpy as np
from rescue_solver.core import RescueModel,FixedSupportRescueModel
from rescue_solver.config import load_config,build_model_params
from rescue_solver.solver import Settings,price_grid
from rescue_solver.storage import atomic_write_json,save_profile,load_profile,digest
from rescue_solver.cli import clean_json
from research_solver.high_precision import solve_high
from run_research import source_identity,check_source

BENCHMARKS={6:((.300,.490),(.350,.350)),12:((.230,.460),(.270,.270)),
            24:((.170,.360),(.215,.215)),48:((.150,.350),(.170,.170))}


def refined_route_edges(edges,target_points):
    edges=list(edges)
    while len(edges)<target_points:
        i=int(np.argmax(np.diff(edges)));edges.insert(i+1,(edges[i]+edges[i+1])/2)
    return tuple(edges)


def global_menus():
    rescue=price_grid(.05)
    return sorted({(a,b) for a in rescue for b in rescue if a<=b} |
                  {(p,p) for p in price_grid(.0025)})


def local_menus(leaders,step,radius):
    out=set()
    for row in leaders:
        values=[]
        for p in (row['p1'],row['p2']):
            lo=max(0,math.ceil((p-radius-1e-12)/step));hi=min(round(1/step),math.floor((p+radius+1e-12)/step))
            values.append([round(i*step,12) for i in range(lo,hi+1)])
        out.update((a,b) for a in values[0] for b in values[1] if a<=b)
    return sorted(out)


def worker(task):
    root,m,request=task;root=Path(root);directory=root/f'm{m:g}'
    directory.mkdir(exist_ok=False)
    with np.load(root/'support.npz',allow_pickle=False) as d:
        model=FixedSupportRescueModel(build_model_params(request['model']),d['c'],d['fc'],d['s'],d['fs'])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    def log(data):
        event=dict(m=m,**data)
        print(json.dumps(clean_json(event)),flush=True)
        with (directory/'progress.jsonl').open('a') as f:f.write(json.dumps(clean_json(event))+'\n')
    rows=[];done={}
    def evaluate_menu(p1,p2,stage):
        key=(p1,p2)
        if key in done:return done[key]
        ordinal=len(rows);menu_dir=directory/f'menu_{ordinal:05d}';menu_dir.mkdir()
        # Summable alpha across every menu, both audit replicates and thicknesses.
        alpha=.05*6/(math.pi**2*len(request['m'])*2*(ordinal+1)**2)
        settings=Settings(train_counts=50000,audit_counts=1000000,count_batch_size=64,
            seed=int(np.random.SeedSequence([request['seed'],int(m),ordinal,0]).generate_state(1,dtype=np.uint64)[0]),alpha=alpha,
            schedule=((.02,40,.35),(.004,60,.25),(.0005,100,.15),(0.,500,.1)))
        log(dict(stage='menu_started',phase=stage,ordinal=ordinal,p1=p1,p2=p2,
            cost_points=model.C,route_points=model.S,train_counts=50000,audit_counts=1000000))
        profile,result=solve_high(model,m,p1,p2,settings,lambda r:log(dict(p1=p1,p2=p2,**r)))
        check_source(request['source_identity'])
        save_profile(menu_dir/'profile.npz',profile)
        result.update(source_identity=request['source_identity'],profile_sha256=digest(menu_dir/'profile.npz'),
            cost_points=model.C,route_points=model.S,phase=stage)
        atomic_write_json(menu_dir/'result.json',clean_json(result))
        row=dict(m=m,p1=p1,p2=p2,passed=result['numerical_checks_passed'],directory=str(menu_dir),
            score=None,profile_sha256=result['profile_sha256'])
        rows.append(row);done[key]=row
        log(dict(stage='menu_finished',p1=p1,p2=p2,passed=row['passed']))
        return row
    # Prices below are independent test inputs, not claimed optimal prices.
    for menu in BENCHMARKS[m]:evaluate_menu(*menu,'validation_gate')
    if not all(r['passed'] for r in rows):
        summary=dict(m=m,status='gate_blocked',rows=rows,price_search_started=False,
            reason='Unresolved inner incentives; do not expand this thickness price search.',wpbe_certified=False)
        atomic_write_json(directory/'summary.json',summary);log(summary);return summary
    if request['phase']=='validation':
        summary=dict(m=m,status='fixed_menu_gate_passed',rows=rows,price_search_started=False,wpbe_certified=False)
        atomic_write_json(directory/'summary.json',summary);return summary
    def score_rows():
        for ordinal,row in enumerate(rows):
            if row['score'] is not None:continue
            p=load_profile(Path(row['directory'])/'profile.npz')
            case=(row['p1'],row['p2'],p)
            selection_seed=int(np.random.SeedSequence([request['seed'],int(m),ordinal,1]).generate_state(1,dtype=np.uint64)[0])
            out,_,_=model.paired_evaluate(m,case,case,2000000,selection_seed)
            row['score']=out['completion']
            atomic_write_json(Path(row['directory'])/'selection.json',dict(markets=2000000,score=row['score'],
                seed=selection_seed,profile_sha256=row['profile_sha256'],independent_of_training_and_audit=True))
        atomic_write_json(directory/'candidates.json',rows)
    log(dict(stage='global_price_search_started',menus=len(global_menus())))
    for p1,p2 in global_menus():evaluate_menu(p1,p2,'global')
    score_rows()
    for step,radius,top in ((.02,.08,5),(.01,.03,4),(.005,.01,3),(.0025,.005,3)):
        # Unresolved high-scoring menus stay in the refinement competition.
        leaders=sorted(rows,key=lambda r:(-r['score'],r['p1'],r['p2']))[:top]
        for p1,p2 in local_menus(leaders,step,radius):evaluate_menu(p1,p2,f'refine_{step}')
        score_rows()
    rescue=max(rows,key=lambda r:r['score'])
    flat=max((r for r in rows if r['p1']==r['p2']),key=lambda r:r['score'])
    summary=dict(m=m,status='price_search_finished',rescue=rescue,flat=flat,
        all_candidates_passed=all(r['passed'] for r in rows),price_search_started=True,
        candidate_count=len(rows),wpbe_certified=False,continuous_global_optimum_proved=False,
        type_route_convergence_verified=False,optimized_V_certified=False)
    if rescue['passed'] and flat['passed']:
        a=(rescue['p1'],rescue['p2'],load_profile(Path(rescue['directory'])/'profile.npz'))
        b=(flat['p1'],flat['p2'],load_profile(Path(flat['directory'])/'profile.npz'))
        r,f,comparison=model.paired_evaluate(m,a,b,10000000,request['seed']+900000003+int(m)*100003)
        summary.update(rescue_outcome=r,flat_outcome=f,comparison=comparison,report_markets=10000000)
    atomic_write_json(directory/'summary.json',clean_json(summary));return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--m',nargs='+',type=int,default=[6,12,24,48]);p.add_argument('--workers',type=int,default=4)
    p.add_argument('--output',required=True);p.add_argument('--phase',choices=['validation','search'],default='search')
    p.add_argument('--seed',type=int,default=2027090601);p.add_argument('--route-seed',type=int,default=20260904)
    args=p.parse_args()
    if args.workers<1 or len(set(args.m))!=len(args.m) or any(m not in BENCHMARKS for m in args.m):p.error('Require distinct supported thicknesses and positive workers')
    if args.seed<0 or args.route_seed<0:p.error('Nonnegative seeds required')
    root=Path(args.output).resolve();root.mkdir(parents=True,exist_ok=False)
    params=build_model_params(load_config(Path(__file__).parent/'configs/research.json')['model'])
    params=replace(params,cost_probability_edges=tuple(np.linspace(0,1,2049)),
        route_positive_quantile_edges=refined_route_edges(params.route_positive_quantile_edges,48),
        route_draws=2400000,seed=args.route_seed)
    model=RescueModel(params)
    np.savez_compressed(root/'support.npz',c=model.c,fc=model.fc,s=model.s,fs=model.fs)
    identity=source_identity();identity['sha256']['run_thick_markets.py']=digest(Path(__file__))
    request=dict(m=args.m,phase=args.phase,workers=args.workers,seed=args.seed,model=asdict(params),
        cost_points=model.C,route_points=model.S,source_identity=identity,support_sha256=digest(root/'support.npz'),
        validation_inputs=BENCHMARKS,prices_are_not_preset_optima=True,
        audit_counts=1000000,train_counts=50000,rerank_markets=2000000,report_markets=10000000)
    atomic_write_json(root/'request.json',request)
    results=[]
    with ProcessPoolExecutor(max_workers=min(args.workers,len(args.m))) as pool:
        futures=[pool.submit(worker,(str(root),m,request)) for m in args.m]
        for future in as_completed(futures):
            results.append(future.result());atomic_write_json(root/'progress_summary.json',clean_json(dict(completed=results)))
    atomic_write_json(root/'summary.json',clean_json(dict(results=results,wpbe_certified=False)))


if __name__=='__main__':main()

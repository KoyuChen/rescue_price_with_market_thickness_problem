#!/usr/bin/env python3
"""Repair a completed gate profile, optionally lifting to a finer cost support.

The branch rule is the SAME original cold-start pipeline followed by the SAME
refinement for every menu. No selecting a branch by platform completion.
Inputs and outputs are distinct; the input profile is never overwritten.
"""
import argparse
from dataclasses import asdict,replace
import json
from pathlib import Path
import time
import numpy as np
from rescue_solver.core import FixedSupportRescueModel,Profile
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings,best_response
from rescue_solver.diagnostics import regret_diagnostics
from rescue_solver.storage import atomic_write_json,digest,load_profile,save_profile
from rescue_solver.cli import clean_json
from research_solver.certified import CertifiedPayoffEvaluator
from research_solver.solve import polish_support
from research_solver.types import lift_profile
from run_research import source_identity,check_source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--menu-dir',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--cost-points',type=int,default=2048)
    parser.add_argument('--train-counts',type=int,default=10000)
    parser.add_argument('--audit-counts',type=int,default=1000000)
    parser.add_argument('--seed',type=int,default=2026490601)
    parser.add_argument('--steps',type=int,default=250)
    args=parser.parse_args()
    if min(args.cost_points,args.steps,args.train_counts,args.audit_counts)<2 or args.seed<0:
        parser.error('Positive seed and budgets >=2 required')
    input_dir=Path(args.menu_dir);root=input_dir.parent
    old=json.loads((input_dir/'result.json').read_text())
    request=json.loads((root/'request.json').read_text());support=json.loads((root/'support.json').read_text())
    check_source(request['source_identity'])
    if digest(input_dir/'profile.npz')!=old['profile_sha256']: raise ValueError('Profile checksum mismatch')
    original_profile=load_profile(input_dir/'profile.npz')
    params=build_model_params(request['config']['model'])
    edges=np.linspace(0,1,args.cost_points+1)
    costs=(edges[:-1]+edges[1:])/2
    original_edges=np.asarray(params.cost_probability_edges)
    model=FixedSupportRescueModel(replace(params,cost_probability_edges=tuple(edges)),
        costs,np.diff(edges),np.asarray(support['s']),np.asarray(support['fs']))
    profile=lift_profile(model,original_edges,original_profile,old['p1'],old['p2'])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    settings=Settings(train_counts=args.train_counts,audit_counts=args.audit_counts,seed=args.seed,
        alpha=.05/8,schedule=((0.,args.steps,.1),))
    evaluator=CertifiedPayoffEvaluator(model,settings)
    output=Path(args.output);output.mkdir(parents=True,exist_ok=False)
    identity=source_identity();identity['sha256']['refine_research.py']=digest(Path(__file__))
    m,p1,p2=old['m'],old['p1'],old['p2'];started=time.monotonic();history=[]
    def record(data):
        event=dict(m=m,p1=p1,p2=p2,cost_points=args.cost_points,**data)
        print(json.dumps(clean_json(event)),flush=True)
        with (output/'progress.jsonl').open('a') as f:f.write(json.dumps(clean_json(event))+'\n')
    atomic_write_json(output/'request.json',dict(m=m,p1=p1,p2=p2,settings=asdict(settings),
        input_profile_sha256=old['profile_sha256'],input_menu=str(input_dir),source_identity=identity,
        input_source_identity=old['source_identity'],cost_points=args.cost_points,route_points=model.S,
        price_optimized=False,lift_feasibility_enforced=True,
        branch_rule='Prior common cold start, feasible interval lift, common zero-temperature refinement.'))
    atomic_write_json(output/'support.json',{k:getattr(model,k).tolist() for k in ('c','fc','s','fs')})
    for step in range(args.steps):
        ev=evaluator.evaluate(m,p1,p2,profile,args.train_counts,args.seed)
        if polish_support(model,profile,ev):ev=evaluator.evaluate(m,p1,p2,profile,args.train_counts,args.seed)
        diagnostic=regret_diagnostics(model,p1,profile,ev,.00075/4,.0015/4)
        if step%10==0:record(dict(stage='iteration',step=step,regrets=diagnostic,unknown=ev['unknown_feasible_history_count']))
        if diagnostic['sample_checks_pass'] and not ev['unknown_feasible_history_count']:break
        br,rr=best_response(model,profile,ev,0.,settings.response_tie_tol)
        rr=np.where(ev['unknown_old_history'].T[:,None,:],profile.retain,rr)
        profile.sigma_e=.9*profile.sigma_e+.1*br[0]
        profile.sigma_h=.9*profile.sigma_h+.1*br[1]
        profile.retain=.9*profile.retain+.1*rr
    ev=evaluator.evaluate(m,p1,p2,profile,args.train_counts,args.seed)
    diagnostic=regret_diagnostics(model,p1,profile,ev)
    audits=[]
    for j in range(2):
        record(dict(stage='audit_started',replicate=j+1,count_draws=args.audit_counts))
        audit=evaluator.audit(m,p1,p2,profile,args.audit_counts,args.seed+1000003+j*104729)
        audits.append(audit)
        record(dict(stage='audit_finished',replicate=j+1,passed=audit['bounded_checks_pass'],
            regret_upper=audit['max_regret_upper'],support_upper=max(audit['initial_support_gap_upper'],audit['retention_support_gap_upper']),
            unresolved=len(audit['unresolved_histories'])))
    profile.meta=dict(early_share=float(np.sum(model.type_mass*profile.sigma_e)),
        hidden_share=float(np.sum(model.type_mass*profile.sigma_h)),max_regret=diagnostic['max_regret'])
    check_source(identity);save_profile(output/'profile.npz',profile)
    atomic_write_json(output/'profile.json',{k:getattr(profile,k).tolist() for k in ('sigma_e','sigma_h','retain','q_values')})
    passed=diagnostic['sample_checks_pass'] and all(a['bounded_checks_pass'] for a in audits)
    result=dict(m=m,p1=p1,p2=p2,status='finite_support_checks_passed' if passed else 'validation_blocked',
        numerical_checks_passed=bool(passed),audits=audits,training_regrets=diagnostic,
        cost_points=model.C,route_points=model.S,tie_quadrature_order=64,settings=asdict(settings),
        input_profile_sha256=old['profile_sha256'],profile_sha256=digest(output/'profile.npz'),
        source_identity=identity,elapsed_seconds=time.monotonic()-started,
        price_optimized=False,lift_feasibility_enforced=True,
        wpbe_certified=False,continuous_type_convergence_verified=False)
    atomic_write_json(output/'result.json',clean_json(result))
    record(dict(stage='refinement_finished',status=result['status']))
    return 0 if passed else 2


if __name__=='__main__':raise SystemExit(main())

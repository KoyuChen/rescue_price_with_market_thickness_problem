#!/usr/bin/env python3
"""Independent precision diagnostics on completed fixed-menu gate outputs."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import numpy as np
from rescue_solver.core import FixedSupportRescueModel
from rescue_solver.config import build_model_params
from rescue_solver.storage import atomic_write_json, digest, load_profile
from rescue_solver.cli import clean_json
from rescue_solver.solver import Settings
from research_solver.evaluator import JointPayoffEvaluator
from research_solver.analytic import no_hidden_completion
from run_research import check_source, source_identity


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gate',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    root=Path(args.gate);target=Path(args.output)
    if target.exists(): raise FileExistsError(target)
    request=json.loads((root/'request.json').read_text())
    check_source(request['source_identity'])
    support=json.loads((root/'support.json').read_text())
    params=build_model_params(request['config']['model'])
    model=FixedSupportRescueModel(params,**{k:np.asarray(v) for k,v in support.items()})
    diagnostic=[]
    for m,p in ((1,.45),(3,.37),(6,.35),(12,.27),(24,.215),(48,.17)):
        exact=no_hidden_completion(model,m,p,True)
        values={'17':no_hidden_completion(model,m,p)}
        for count in (128,512,2048):
            edges=np.linspace(0,1,count+1)
            finer=FixedSupportRescueModel(replace(params,cost_probability_edges=tuple(edges)),
                (edges[:-1]+edges[1:])/2,np.diff(edges),model.s,model.fs)
            values[str(count)]=no_hidden_completion(finer,m,p)
        diagnostic.append(dict(m=m,p=p,branch='all_early_no_hidden',
            price_optimized=False,continuous_cost_completion=exact,
            finite_cost_completion=values,absolute_error_pp={k:100*abs(v-exact) for k,v in values.items()}))
    crosschecks=[]
    for directory in sorted(root.glob('m*_p*')):
        if not (directory/'result.json').exists(): continue
        result=json.loads((directory/'result.json').read_text())
        if result['p1']!=result['p2'] or not result['numerical_checks_passed']: continue
        if digest(directory/'profile.npz')!=result['profile_sha256']: raise ValueError('Profile checksum mismatch')
        profile=load_profile(directory/'profile.npz');m,p=result['m'],result['p1']
        settings=Settings(train_counts=10000,audit_counts=100000)
        evs=[]
        for order in (32,64):
            x,w=np.polynomial.legendre.leggauss(order);model.tie_t=(x+1)/2;model.tie_w=w/2
            evs.append(JointPayoffEvaluator(model,settings).evaluate(m,p,p,profile,100000,2026190601))
        differences={key:float(np.max(np.abs(evs[0][key]-evs[1][key])))
                     for key in ('u_e','u_h','retain_advantage','completion')}
        print(json.dumps(dict(stage='paired_report_started',m=m,p=p,markets=2000000)),flush=True)
        outcome,_,_=model.paired_evaluate(m,(p,p,profile),(p,p,profile),2000000,2026290601+int(m)*104729)
        crosschecks.append(dict(m=m,p=p,price_optimized=False,profile_sha256=result['profile_sha256'],
            quadrature_32_vs_64_max_difference=differences,report_markets=2000000,
            report_seed=2026290601+int(m)*104729,outcome=outcome,
            full_market_MC_report_not_a_regret_certificate=True))
    output=dict(source_identity=source_identity(),diagnostic_script_sha256=digest(Path(__file__)),
        type_diagnostic=diagnostic,fixed_flat_crosschecks=crosschecks,
        scope='Fixed-menu / named branch diagnostics; NOT optimized rescue prices or V(m).',
        continuous_cost_solver_implemented=False,wpbe_certified=False)
    atomic_write_json(target,clean_json(output));print(json.dumps(dict(output=str(target),completed=True)),flush=True)


if __name__=='__main__': main()

#!/usr/bin/env python3
"""Held-out raw-market comparison of validated FIXED menus; no re-selection."""
import argparse
import json
from pathlib import Path
import numpy as np
from rescue_solver.core import FixedSupportRescueModel
from rescue_solver.config import build_model_params
from rescue_solver.storage import load_profile,digest,atomic_write_json
from rescue_solver.cli import clean_json
from run_research import source_identity


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--gate',required=True)
    parser.add_argument('--m',type=int,required=True)
    parser.add_argument('--markets',type=int,default=10000000)
    parser.add_argument('--seed',type=int,default=2026990601)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if args.markets<2 or args.m<=0 or args.seed<0:parser.error('Invalid thickness, markets or seed')
    target=Path(args.output)
    if target.exists():raise FileExistsError(target)
    root=Path(args.root);cases=[];supports=[];identities=[]
    for label in ('rescue','flat'):
        folder=root/f'm{args.m}_{label}'
        result=json.loads((folder/'result.json').read_text())
        if not result['numerical_checks_passed'] or result['m']!=args.m:
            raise ValueError('Both menus must pass the fixed-support audit at this thickness')
        if digest(folder/'profile.npz')!=result['profile_sha256']:raise ValueError('Profile hash mismatch')
        identities.append(result)
        cases.append((result['p1'],result['p2'],load_profile(folder/'profile.npz')))
        supports.append(json.loads((folder/'support.json').read_text()))
    if supports[0]!=supports[1]:raise ValueError('Rescue and flat must have identical support')
    if cases[1][0]!=cases[1][1]:raise ValueError('Flat benchmark must be diagonal')
    gate=json.loads((Path(args.gate)/'request.json').read_text())
    params=build_model_params(gate['config']['model'])
    model=FixedSupportRescueModel(params,**{k:np.asarray(v) for k,v in supports[0].items()})
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    raw,flat,comparison=model.paired_evaluate(args.m,cases[0],cases[1],args.markets,args.seed)
    result=dict(m=args.m,p1=cases[0][0],p2=cases[0][1],p_flat=cases[1][0],
        rescue=raw,flat=flat,comparison=comparison,markets=args.markets,seed=args.seed,
        cost_points=model.C,route_points=model.S,tie_quadrature_order=64,
        profile_sha256={k:r['profile_sha256'] for k,r in zip(('rescue','flat'),identities)},
        audit_max_regret_upper={k:max(a['max_regret_upper'] for a in r['audits'])
                                for k,r in zip(('rescue','flat'),identities)},
        source_identity=source_identity(),report_script_sha256=digest(Path(__file__)),
        fixed_menu_only=True,external_prices_optimized=False,V_is_optimized_value=False,
        continuous_type_convergence_verified=False,wpbe_certified=False,
        interval_scope='Fixed policies; paired raw-market Monte Carlo uncertainty only.')
    atomic_write_json(target,clean_json(result))
    print(json.dumps(clean_json(result)),flush=True)


if __name__=='__main__':main()

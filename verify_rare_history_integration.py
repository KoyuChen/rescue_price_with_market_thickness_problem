#!/usr/bin/env python3
"""Regression on previously archived profiles, never on mutable checkpoints.

Verifies v2 posterior/retention integration against the earlier frozen evidence.
This does NOT certify that those profiles are equilibria.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from rare_history_evaluator import RareHistoryEvaluator
from rescue_solver.config import build_model_params
from rescue_solver.core import Profile
from rescue_solver.solver import Settings
from rescue_solver.diagnostics import regret_diagnostics
from rescue_solver.storage import atomic_write_json,digest
from run_research import source_identity,check_source

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',default='results/thick_rare_certified_20260906')
    ap.add_argument('--output',required=True)
    args=ap.parse_args();source=Path(args.source);output=Path(args.output)
    if output.exists():raise ValueError('Never overwrite a completed regression')
    request=json.loads((source/'request.json').read_text())
    prior=json.loads((source/'posterior_bounds.json').read_text())['rows']
    with np.load(source/'support.npz',allow_pickle=False) as z:
        model=VectorizedTieModel(build_model_params(request['model']),*[z[k] for k in ('c','fc','s','fs')])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    identity=source_identity();root=Path(__file__).resolve().parent
    for name in ('accelerated_evaluator.py','history_envelope.py','zero_retention_envelope.py',
                 'rare_history_enumeration_v2.py','multi_route_envelope_v2.py',
                 'rare_history_evaluator.py','verify_rare_history_integration.py'):
        identity['sha256'][name]=digest(root/name)
    inputs={str(p):digest(p) for p in source.glob('*') if p.is_file()}
    rows=[]
    for m,p1,p2 in ((6,.3,.49),(12,.23,.46),(24,.17,.36)):
        with np.load(source/f'm{m}_checkpoint.npz',allow_pickle=False) as z:
            profile=Profile(*[z[k].copy() for k in ('sigma_e','sigma_h','retain','q_values')],{})
        evaluator=RareHistoryEvaluator(model,Settings())
        ev=evaluator.evaluate(m,p1,p2,profile,50000,2026090610+m)
        for old in [r for r in prior if r['m']==m]:
            tag=old['tag_route'];iq=old['price_index']
            assert not ev['unknown_old_history'][tag,iq],(m,tag,iq)
            if old.get('structurally_off_path'):
                assert ev['offpath_certified'][tag,iq]
            else:
                assert not ev['offpath_certified'][tag,iq]
                assert abs(ev['pi_old'][tag,iq]-old['conditional_win_probability_estimate'])<1e-8
        row=dict(m=m,unknown=ev['unknown_feasible_history_count'],
                 diagnostics=regret_diagnostics(model,p1,profile,ev,.00075,.0015),
                 rare_history_resolution=ev['rare_history_resolution'])
        rows.append(row);print(json.dumps(row),flush=True)
    check_source(identity)
    assert all(digest(Path(p))==h for p,h in inputs.items())
    atomic_write_json(output,dict(source_identity=identity,input_sha256=inputs,rows=rows,
        prior_frozen_posteriors_reproduced=True,active_run_modified=False,
        equilibrium_audit_completed=False,outer_price_optimized=False))

if __name__=='__main__':main()

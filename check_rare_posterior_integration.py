#!/usr/bin/env python3
"""Frozen real-profile regression: detect, rather than certify, old retention errors."""
import json
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from rare_posterior_evaluator import RarePosteriorEvaluator
from rescue_solver.config import build_model_params
from rescue_solver.core import Profile
from rescue_solver.solver import Settings
from rescue_solver.diagnostics import regret_diagnostics
from rescue_solver.storage import atomic_write_json,digest
from run_research import source_identity


def main():
    root=Path('results/thick_rare_certified_20260906')
    out=Path('runs/rare_posterior_integration_20260906');out.mkdir(exist_ok=True)
    request=json.loads((root/'request.json').read_text())
    with np.load(root/'support.npz',allow_pickle=False) as z:
        model=VectorizedTieModel(build_model_params(request['model']),*[z[k] for k in ('c','fc','s','fs')])
    x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
    identity=source_identity()
    for name in ('check_rare_posterior_integration.py','rare_posterior_evaluator.py',
        'bounded_rare_posterior.py','strict_multi_route_envelope.py','zero_retention_envelope.py',
        'history_envelope.py','accelerated_evaluator.py'):
        identity['sha256'][name]=digest(Path(name))
    rows=[]
    for m,p1,p2 in [(6,.3,.49),(12,.23,.46),(24,.17,.36)]:
        src=root/f'm{m}_checkpoint.npz'
        with np.load(src,allow_pickle=False) as z:
            profile=Profile(z['sigma_e'].copy(),z['sigma_h'].copy(),z['retain'].copy(),z['q_values'].copy(),{})
        settings=Settings(train_counts=1000,audit_counts=1000,count_batch_size=64,seed=202609061819+m)
        evaluator=RarePosteriorEvaluator(model,settings)
        ev=evaluator.evaluate(m,p1,p2,profile,1000,settings.seed)
        diag=regret_diagnostics(model,p1,profile,ev)
        audit=evaluator.audit(m,p1,p2,profile,1000,settings.seed+1000003)
        row=dict(m=m,p1=p1,p2=p2,unknown_training_histories=ev['unknown_feasible_history_count'],
            training_regrets=diag,posteriors=ev['rare_posterior_records'],audit=audit,
            source_identity=identity,frozen_checkpoint_sha256=digest(src),support_sha256=digest(root/'support.npz'),
            scope='1000-count integration regression only; these old policies must FAIL, not acceptance evidence')
        assert diag['retention_regret_max']>settings.regret_tol,(m,diag)
        assert audit['retention_regret_upper']>settings.regret_tol,(m,audit)
        assert not audit['bounded_checks_pass']
        atomic_write_json(out/f'm{m}.json',row)
        rows.append(dict(m=m,unknown=ev['unknown_feasible_history_count'],
            retention_regret=diag['retention_regret_max'],retention_audit_upper=audit['retention_regret_upper'],
            old_profile_correctly_rejected=True))
        print(json.dumps(rows[-1]),flush=True)
    atomic_write_json(out/'summary.json',dict(rows=rows,acceptance_audit=False,source_identity=identity))


if __name__=='__main__':main()

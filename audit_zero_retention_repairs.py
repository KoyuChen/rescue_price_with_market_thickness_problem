#!/usr/bin/env python3
"""Fresh held-out audits after repaired cold profiles have been frozen.

The repair runner repeats old seeds for comparable diagnostics. Acceptance
here uses NEW seeds and half the original per-menu alpha, never used to train
or choose profiles. Original and repaired diagnostics remain separate.
"""
import argparse
from dataclasses import replace
import fcntl
import json
from pathlib import Path
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json,digest,load_profile
from rescue_solver.cli import clean_json
from run_research import check_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    args = parser.parse_args();root = Path(args.root).resolve()
    request = json.loads((root/'request.json').read_text())
    if not (root/'summary.json').exists(): raise ValueError('Freeze all repair profiles first')
    identity = dict(request['source_identity'])
    identity['sha256'] = dict(identity['sha256'],**{'audit_zero_retention_repairs.py':digest(__file__)})
    with (root/'fresh_audit.lock').open('a+') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise SystemExit('Fresh audit already running')
        rows = []
        for m,i in request['cases']:
            directory = root/f'm{m}_menu_{i:05d}'
            result = json.loads((directory/'result.json').read_text())
            check_source(identity)
            if digest(directory/'profile.npz') != result['profile_sha256']:
                raise ValueError('Frozen profile changed')
            source = Path(result['original_directory']).parents[1]
            oldrequest = json.loads((source/'request.json').read_text())
            if digest(source/'support.npz') != result['support_sha256']:
                raise ValueError('Support changed')
            with np.load(source/'support.npz',allow_pickle=False) as z:
                model = VectorizedTieModel(build_model_params(oldrequest['model']),
                    *[z[k] for k in ('c','fc','s','fs')])
            x,w = np.polynomial.legendre.leggauss(64); model.tie_t=(x+1)/2; model.tie_w=w/2
            profile = load_profile(directory/'profile.npz')
            settings = Settings(**result['settings'])
            settings = replace(settings,alpha=settings.alpha/2)
            evaluator = ZeroRetentionEnvelopeEvaluator(model,settings)
            audits = []
            for j in range(2):
                seed = 202609060800000+m*100003+i*11+j
                target = directory/f'fresh_audit_{j+1}.json'
                if target.exists():
                    saved = json.loads(target.read_text())
                    if saved['profile_sha256'] != result['profile_sha256'] or saved['source_identity'] != identity or saved['seed'] != seed:
                        raise ValueError('Fresh audit provenance mismatch')
                else:
                    audit = evaluator.audit(m,result['p1'],result['p2'],profile,1000000,seed)
                    check_source(identity)
                    saved = dict(audit=audit,seed=seed,count_draws=1000000,
                        profile_sha256=result['profile_sha256'],source_identity=identity,
                        independent_of_original_audit_and_training_seeds=True)
                    atomic_write_json(target,clean_json(saved))
                audits.append(saved['audit'])
                print(json.dumps(dict(m=m,ordinal=i,replicate=j+1,
                    passed=saved['audit']['bounded_checks_pass'],
                    max_regret_upper=saved['audit']['max_regret_upper'])),flush=True)
            rows.append(dict(m=m,ordinal=i,p1=result['p1'],p2=result['p2'],
                passed=bool(result['training_regrets']['sample_checks_pass'] and all(a['bounded_checks_pass'] for a in audits)),
                max_regret_upper=[a['max_regret_upper'] for a in audits],
                unresolved=[len(a['unresolved_histories']) for a in audits]))
        atomic_write_json(root/'fresh_audit_summary.json',dict(rows=rows,
            all_repairs_passed=all(r['passed'] for r in rows),external_price_optimized=False))


if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Cold-homotopy repair of one newly completed failed menu, in separate output.

Does not replace results in active searches or claim completed price search.
Same support, settings, seeds, confidence allocation, and equilibrium rule.
Original failed results/profiles are archived in full. Per-menu checkpoints
and an exclusive runner lock protect this independent version on restart.
"""
import argparse
from dataclasses import asdict
import datetime
import fcntl
import json
import os
from pathlib import Path
import shutil
import numpy as np
from accelerated_evaluator import VectorizedTieModel
from zero_retention_checkpoint_solver import solve_checkpointed
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, digest, save_profile
from rescue_solver.cli import clean_json
from run_research import check_source, source_identity

ROOT = Path(__file__).resolve().parent
CASES = ((3,157),)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    for m,_ in CASES:
        active = ROOT/f'runs/m{m}_outer_search_20260906'
        if output == active or active in output.parents:
            parser.error('Repair output must be outside every active search')
    output.mkdir(parents=True,exist_ok=True)
    with (output/'runner.lock').open('a+') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise SystemExit('Repair already running')
        identity = source_identity()
        for name in ('history_envelope.py','accelerated_evaluator.py',
                     'zero_retention_envelope.py','zero_retention_checkpoint_solver.py',
                     'run_zero_retention_repair_m3_menu157.py'):
            identity['sha256'][name] = digest(ROOT/name)
        inputs = {}
        for m,i in CASES:
            root = ROOT/f'runs/m{m}_outer_search_20260906'
            d = root/f'm{m}/menu_{i:05d}'
            for f in (root/'request.json',root/'support.npz',d/'result.json',d/'profile.npz'):
                inputs[str(f.relative_to(ROOT))] = digest(f)
        request = clean_json(dict(cases=CASES,source_identity=identity,input_sha256=inputs,
            branch_rule='Same common cold homotopy; never warm-start failed profiles',
            replaces_active_search_results=False,external_price_optimized=False))
        if (output/'request.json').exists():
            if json.loads((output/'request.json').read_text()) != request:
                raise ValueError('Repair inputs or source changed')
        else: atomic_write_json(output/'request.json',request)

        def verify():
            check_source(identity)
            for f,h in inputs.items():
                if digest(ROOT/f) != h: raise ValueError('Repair input changed: '+f)

        def log(row):
            row = clean_json(dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**row))
            print(json.dumps(row),flush=True)
            with (output/'progress.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')

        atomic_write_json(output/'supervisor.json',dict(pid=os.getpid(),status='running'))
        rows = []
        for m,i in CASES:
            verify()
            root = ROOT/f'runs/m{m}_outer_search_20260906'
            source = root/f'm{m}/menu_{i:05d}'
            directory = output/f'm{m}_menu_{i:05d}'; directory.mkdir(exist_ok=True)
            prior = json.loads((source/'result.json').read_text())
            if prior['numerical_checks_passed']: raise ValueError('Only failed completed menus allowed')
            if digest(source/'profile.npz') != prior['profile_sha256']:
                raise ValueError('Failed profile checksum mismatch')
            for name in ('result.json','profile.npz'):
                target = directory/('original_'+name)
                if target.exists():
                    if digest(target) != digest(source/name): raise ValueError('Archive mismatch')
                else: shutil.copy2(source/name,target)
            oldrequest = json.loads((root/'request.json').read_text())
            with np.load(root/'support.npz',allow_pickle=False) as z:
                model = VectorizedTieModel(build_model_params(oldrequest['model']),
                    *[z[k] for k in ('c','fc','s','fs')])
            x,w = np.polynomial.legendre.leggauss(64); model.tie_t=(x+1)/2; model.tie_w=w/2
            settings = Settings(**prior['settings'])
            log(dict(stage='repair_started',m=m,ordinal=i,p1=prior['p1'],p2=prior['p2']))
            if (directory/'result.json').exists():
                result = json.loads((directory/'result.json').read_text())
                if result['source_identity'] != identity or digest(directory/'profile.npz') != result['profile_sha256']:
                    raise ValueError('Completed repair provenance mismatch')
            else:
                profile,result = solve_checkpointed(model,m,prior['p1'],prior['p2'],settings,
                    directory/'checkpoint.npz',identity,
                    lambda row: log(dict(m=m,ordinal=i,**row)))
                verify()
                save_profile(directory/'profile.npz',profile)
                result.update(source_identity=identity,profile_sha256=digest(directory/'profile.npz'),
                    original_result_sha256=digest(source/'result.json'),
                    original_profile_sha256=prior['profile_sha256'],original_directory=str(source),
                    cost_points=model.C,route_points=model.S,tie_quadrature_order=64,
                    support_sha256=digest(root/'support.npz'),settings=asdict(settings),
                    replaces_active_search_results=False)
                atomic_write_json(directory/'result.json',clean_json(result))
            row = dict(m=m,ordinal=i,p1=prior['p1'],p2=prior['p2'],
                passed=result['numerical_checks_passed'],
                unknown_training_histories=result['unknown_training_histories'],
                audits=[dict(passed=a['bounded_checks_pass'],max_regret_upper=a['max_regret_upper'],
                    unresolved=len(a['unresolved_histories'])) for a in result['audits']])
            rows.append(row);log(dict(stage='repair_finished',**row))
        atomic_write_json(output/'summary.json',dict(rows=rows,external_price_optimized=False,
            all_repairs_passed=all(r['passed'] for r in rows),replaces_active_search_results=False))
        atomic_write_json(output/'supervisor.json',dict(pid=os.getpid(),status='finished'))


if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Cold-start posterior-aware repairs for m=3 search menus 157--159.

These completed outer-search failures are kept as evidence only.  Each repair
starts from the common full-support homotopy, checkpoints every iteration and
writes to an independent directory.  It never updates the outer-search cache.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import fcntl
import json
import os
from pathlib import Path
import shutil

import numpy as np

from accelerated_evaluator import VectorizedTieModel
from rare_posterior_checkpoint_solver import solve_checkpointed
from rescue_solver.cli import clean_json
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, digest, save_profile
from run_research import check_source, source_identity


ROOT = Path(__file__).resolve().parent
MARKET = 3
CASES = (157, 158, 159)
DEPENDENCIES = (
    'run_m3_rare_posterior_repairs.py',
    'rare_posterior_checkpoint_solver.py',
    'rare_posterior_evaluator.py',
    'bounded_rare_posterior.py',
    'strict_multi_route_envelope.py',
    'zero_retention_envelope.py',
    'accelerated_evaluator.py',
    'history_envelope.py',
)


def validate_case(ordinal, result):
    expected = ordinal in CASES and result.get('m') == MARKET
    if not expected or result.get('numerical_checks_passed'):
        raise ValueError('Expected one prespecified completed failed m=3 menu')


def worker(task):
    output, ordinal, request = task
    output = Path(output)
    source = Path(request['source_run'])
    directory = output / f'menu_{ordinal:05d}'
    directory.mkdir(exist_ok=True)
    check_source(request['source_identity'])
    for name, expected in request['input_sha256'].items():
        if digest(ROOT / name) != expected:
            raise ValueError('Repair input changed: ' + name)

    source_request = json.loads((source / 'request.json').read_text())
    prior = json.loads((source / f'm3/menu_{ordinal:05d}/result.json').read_text())
    validate_case(ordinal, prior)
    with np.load(source / 'support.npz', allow_pickle=False) as z:
        model = VectorizedTieModel(
            build_model_params(source_request['model']),
            *[z[k] for k in ('c', 'fc', 's', 'fs')],
        )
    x, w = np.polynomial.legendre.leggauss(64)
    model.tie_t, model.tie_w = (x + 1) / 2, w / 2
    settings = Settings(**prior['settings'])

    def log(row):
        event = clean_json(dict(
            m=MARKET, ordinal=ordinal, p1=prior['p1'], p2=prior['p2'], **row,
        ))
        print(json.dumps(event), flush=True)
        with (directory / 'progress.jsonl').open('a') as handle:
            handle.write(json.dumps(event) + '\n')

    if (directory / 'result.json').exists():
        result = json.loads((directory / 'result.json').read_text())
        if (result['source_identity'] != request['source_identity']
                or digest(directory / 'profile.npz') != result['profile_sha256']):
            raise ValueError('Completed repair provenance mismatch')
    else:
        profile, result = solve_checkpointed(
            model, MARKET, prior['p1'], prior['p2'], settings,
            directory / 'checkpoint.npz', request['source_identity'], log,
        )
        check_source(request['source_identity'])
        for name, expected in request['input_sha256'].items():
            if digest(ROOT / name) != expected:
                raise ValueError('Repair input changed: ' + name)
        save_profile(directory / 'profile.npz', profile)
        result.update(
            source_identity=request['source_identity'],
            profile_sha256=digest(directory / 'profile.npz'),
            ordinal=ordinal,
            original_result_sha256=digest(
                source / f'm3/menu_{ordinal:05d}/result.json'),
            original_profile_sha256=prior['profile_sha256'],
            support_sha256=digest(source / 'support.npz'),
            cost_points=model.C,
            route_points=model.S,
            tie_quadrature_order=64,
            original_search_cache_replaced=False,
            external_price_optimized=False,
        )
        atomic_write_json(directory / 'result.json', clean_json(result))

    summary = dict(
        ordinal=ordinal,
        p1=prior['p1'],
        p2=prior['p2'],
        passed=result['numerical_checks_passed'],
        unknown_training_histories=result['unknown_training_histories'],
        training_max_regret=result['training_regrets']['max_regret'],
        audits=[dict(
            passed=a['bounded_checks_pass'],
            max_regret_upper=a['max_regret_upper'],
            unresolved=len(a['unresolved_histories']),
        ) for a in result['audits']],
        original_search_cache_replaced=False,
        external_price_optimized=False,
    )
    atomic_write_json(directory / 'summary.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-run', default='runs/m3_outer_search_20260906')
    parser.add_argument('--output', required=True)
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    source = Path(args.source_run).resolve()
    output = Path(args.output).resolve()
    if (args.workers < 1 or source == output or source in output.parents
            or output in source.parents):
        parser.error('Require positive workers and an independent output directory')

    source_request = json.loads((source / 'request.json').read_text())
    if digest(source / 'support.npz') != source_request['support_sha256']:
        raise ValueError('Source support changed')
    identity = source_identity()
    for name in DEPENDENCIES:
        identity['sha256'][name] = digest(ROOT / name)
    inputs = {
        str((source / 'request.json').relative_to(ROOT)): digest(source / 'request.json'),
        str((source / 'support.npz').relative_to(ROOT)): digest(source / 'support.npz'),
    }
    for ordinal in CASES:
        directory = source / f'm3/menu_{ordinal:05d}'
        prior = json.loads((directory / 'result.json').read_text())
        validate_case(ordinal, prior)
        if digest(directory / 'profile.npz') != prior['profile_sha256']:
            raise ValueError('Original profile hash mismatch')
        for name in ('result.json', 'profile.npz'):
            inputs[str((directory / name).relative_to(ROOT))] = digest(directory / name)

    request = clean_json(dict(
        m=MARKET,
        cases=CASES,
        source_run=str(source),
        source_identity=identity,
        input_sha256=inputs,
        branch_rule='Same common full-support cold homotopy; no failed-profile warm start',
        original_search_cache_replaced=False,
        external_price_optimized=False,
    ))
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'runner.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('m=3 rare-posterior repair already active')
        if (output / 'request.json').exists():
            if json.loads((output / 'request.json').read_text()) != request:
                raise ValueError('Repair source or plan changed')
        else:
            atomic_write_json(output / 'request.json', request)
            shutil.copy2(source / 'request.json', output / 'original_request.json')
            shutil.copy2(source / 'support.npz', output / 'support.npz')
            for ordinal in CASES:
                directory = output / f'menu_{ordinal:05d}'
                directory.mkdir(exist_ok=True)
                shutil.copy2(source / f'm3/menu_{ordinal:05d}/result.json',
                             directory / 'original_result.json')
                shutil.copy2(source / f'm3/menu_{ordinal:05d}/profile.npz',
                             directory / 'original_profile.npz')
        atomic_write_json(output / 'supervisor.json',
                          dict(pid=os.getpid(), status='running'))
        rows = []
        with ProcessPoolExecutor(max_workers=min(args.workers, len(CASES))) as pool:
            futures = [pool.submit(worker, (str(output), ordinal, request))
                       for ordinal in CASES]
            for future in as_completed(futures):
                rows.append(future.result())
                atomic_write_json(output / 'progress_summary.json',
                                  clean_json(dict(rows=rows)))
        rows = sorted(rows, key=lambda row: row['ordinal'])
        atomic_write_json(output / 'summary.json', dict(
            rows=rows,
            all_repairs_passed=all(row['passed'] for row in rows),
            original_search_cache_replaced=False,
            external_price_optimized=False,
        ))
        atomic_write_json(output / 'supervisor.json',
                          dict(pid=os.getpid(), status='finished'))


if __name__ == '__main__':
    main()

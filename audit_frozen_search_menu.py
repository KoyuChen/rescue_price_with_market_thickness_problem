#!/usr/bin/env python3
"""One prespecified, larger held-out audit of an immutable search profile.

No solving, warm start, price selection, or replacement of failed search caches.
The extra audit family spends at most 0.001 across six thicknesses, all menu
ordinals and two replicates. This does not certify the original search family's
combined error rate, continuous types, or an optimized completion difference.
"""
import argparse
from dataclasses import asdict, replace
import fcntl
import json
import math
from pathlib import Path
import shutil
import numpy as np
from accelerated_evaluator import CachedEnvelopeEvaluator, VectorizedTieModel
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, digest, load_profile
from rescue_solver.cli import clean_json
from run_research import check_source, source_identity

ROOT = Path(__file__).resolve().parent


def audit_plan(m, ordinal):
    if m not in (1, 3, 6, 12, 24, 48) or ordinal < 0:
        raise ValueError('Unsupported thickness or negative ordinal')
    return dict(count_draws=5000000,
        seeds=[202609061235000 + m*1000003 + ordinal*11 + j for j in range(2)],
        alpha_per_replicate=.001/6 * 6/math.pi**2/(ordinal+1)**2/2,
        extra_family_error_budget=.001, replicates=2,
        adaptive_retry=False, strategy_adjustment=False)


def validate_output(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output or source in output.parents or output in source.parents:
        raise ValueError('Audit output must be separate from source search')


def verify_hashes(root, hashes):
    for name, expected in hashes.items():
        if digest(Path(root)/name) != expected:
            raise ValueError('Frozen input changed: '+name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--m', type=int, required=True)
    parser.add_argument('--ordinal', type=int, required=True)
    parser.add_argument('--source-run', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    plan = audit_plan(args.m, args.ordinal)
    source, output = Path(args.source_run).resolve(), Path(args.output).resolve()
    validate_output(source, output)
    menu = source/f'm{args.m}/menu_{args.ordinal:05d}'
    prior = json.loads((menu/'result.json').read_text())
    oldrequest = json.loads((source/'request.json').read_text())
    if prior['m'] != args.m or prior['profile_sha256'] != digest(menu/'profile.npz'):
        raise ValueError('Original profile provenance mismatch')
    if not prior['training_regrets']['sample_checks_pass'] or prior['unknown_training_histories']:
        raise ValueError('This audit-only workflow requires converged, resolved training')
    if prior['source_identity'] != oldrequest['source_identity']:
        raise ValueError('Original source identities differ')
    check_source(prior['source_identity'])
    if digest(source/'support.npz') != oldrequest['support_sha256']:
        raise ValueError('Original support changed')
    identity = source_identity()
    for name in ('accelerated_evaluator.py', 'history_envelope.py', 'audit_frozen_search_menu.py'):
        identity['sha256'][name] = digest(ROOT/name)
    inputs = {'original_result.json': menu/'result.json',
              'profile.npz': menu/'profile.npz', 'support.npz': source/'support.npz',
              'original_request.json': source/'request.json'}
    hashes = {k: digest(p) for k,p in inputs.items()}
    request = clean_json(dict(m=args.m, ordinal=args.ordinal, p1=prior['p1'], p2=prior['p2'],
        plan=plan, input_sha256=hashes, source_identity=identity,
        original_directory=str(menu), replaces_active_search_results=False))
    output.mkdir(parents=True, exist_ok=True)
    with (output/'runner.lock').open('a+') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise SystemExit('Frozen audit already running')
        target = output/'request.json'
        if target.exists() and json.loads(target.read_text()) != request:
            raise ValueError('Audit plan or frozen inputs changed')
        if not target.exists(): atomic_write_json(target, request)
        for name,p in inputs.items():
            if not (output/name).exists(): shutil.copy2(p, output/name)
        verify_hashes(output, hashes)
        with np.load(output/'support.npz', allow_pickle=False) as z:
            model = VectorizedTieModel(build_model_params(oldrequest['model']),
                                      *[z[k] for k in ('c','fc','s','fs')])
        x,w = np.polynomial.legendre.leggauss(64)
        model.tie_t, model.tie_w = (x+1)/2, w/2
        profile = load_profile(output/'profile.npz')
        arrays = [getattr(profile,k).copy() for k in ('sigma_e','sigma_h','retain','q_values')]
        settings = replace(Settings(**prior['settings']),
                           audit_counts=plan['count_draws'], alpha=plan['alpha_per_replicate'])
        evaluator = CachedEnvelopeEvaluator(model, settings)
        rows = []
        for j,seed in enumerate(plan['seeds']):
            target = output/f'audit_{j+1}.json'
            if target.exists():
                saved = json.loads(target.read_text())
                if saved['seed'] != seed or saved['request_sha256'] != digest(output/'request.json'):
                    raise ValueError('Cached audit provenance mismatch')
                audit = saved['audit']
            else:
                print(json.dumps(dict(stage='audit_started', replicate=j+1, **plan)), flush=True)
                audit = evaluator.audit(args.m, prior['p1'], prior['p2'], profile, plan['count_draws'], seed)
                check_source(identity); verify_hashes(output, hashes)
                for k,a in zip(('sigma_e','sigma_h','retain','q_values'), arrays):
                    if not np.array_equal(getattr(profile,k),a):
                        raise ValueError('Evaluator mutated frozen strategy')
                atomic_write_json(target, clean_json(dict(audit=audit, seed=seed,
                    request_sha256=digest(output/'request.json'), settings=asdict(settings))))
            row = dict(replicate=j+1, passed=audit['bounded_checks_pass'],
                full_plan_upper=audit['full_plan_regret_upper'],
                retention_upper=audit['retention_regret_upper'],
                max_regret_upper=audit['max_regret_upper'], unresolved=len(audit['unresolved_histories']))
            rows.append(row); print(json.dumps(row), flush=True)
        check_source(identity); verify_hashes(output, hashes)
        summary = dict(m=args.m, ordinal=args.ordinal, p1=prior['p1'],p2=prior['p2'],
            rows=rows, independent_audits_passed=all(r['passed'] for r in rows),
            original_search_status=prior['status'], original_cache_unchanged=True,
            frozen_strategy_unchanged=True, external_price_optimized=False,
            continuous_type_convergence_verified=False, wpbe_certified=False,
            new_family_only_error_budget=plan['extra_family_error_budget'])
        atomic_write_json(output/'summary.json', summary)
        print(json.dumps(summary), flush=True)


if __name__ == '__main__': main()

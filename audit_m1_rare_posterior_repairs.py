#!/usr/bin/env python3
"""Fresh held-out audits for the frozen m=1 rare-posterior repairs.

The repair run deliberately reused the original menu seeds for comparable
diagnostics.  This script never updates a policy: it verifies provenance and
audits every repaired profile with two new one-million-draw count samples.
It leaves the failed outer-search cache untouched.
"""
import argparse
from dataclasses import replace
import fcntl
import json
from pathlib import Path

import numpy as np

from accelerated_evaluator import VectorizedTieModel
from rare_posterior_evaluator import RarePosteriorEvaluator
from rescue_solver.cli import clean_json
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings
from rescue_solver.storage import atomic_write_json, digest, load_profile
from run_research import check_source


CASES = (193, 194, 195)
FRESH_COUNT_DRAWS = 1_000_000


def fresh_seed(ordinal, replicate):
    if ordinal not in CASES or replicate not in (1, 2):
        raise ValueError('Unexpected menu or replicate')
    return 202609061440000 + ordinal * 1009 + replicate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    request = json.loads((root / 'request.json').read_text())
    completed = json.loads((root / 'summary.json').read_text())
    if tuple(request['cases']) != CASES or not completed['all_repairs_passed']:
        raise ValueError('Freeze all prespecified repaired profiles first')

    identity = dict(request['source_identity'])
    identity['sha256'] = dict(identity['sha256'], **{
        'audit_m1_rare_posterior_repairs.py': digest(__file__),
    })
    source = Path(request['source_run'])
    source_request = json.loads((source / 'request.json').read_text())
    if digest(source / 'support.npz') != source_request['support_sha256']:
        raise ValueError('Source support changed')

    with (root / 'fresh_audit.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Fresh repair audit already running')

        rows = []
        for ordinal in CASES:
            directory = root / f'menu_{ordinal:05d}'
            result = json.loads((directory / 'result.json').read_text())
            check_source(identity)
            if result['ordinal'] != ordinal or result['m'] != 1:
                raise ValueError('Repair result does not match requested case')
            if digest(directory / 'profile.npz') != result['profile_sha256']:
                raise ValueError('Frozen repaired profile changed')
            if result['support_sha256'] != digest(source / 'support.npz'):
                raise ValueError('Repair support provenance mismatch')

            with np.load(source / 'support.npz', allow_pickle=False) as z:
                model = VectorizedTieModel(
                    build_model_params(source_request['model']),
                    *[z[k] for k in ('c', 'fc', 's', 'fs')],
                )
            x, w = np.polynomial.legendre.leggauss(result['tie_quadrature_order'])
            model.tie_t, model.tie_w = (x + 1) / 2, w / 2
            profile = load_profile(directory / 'profile.npz')
            settings = replace(Settings(**result['settings']),
                               alpha=result['settings']['alpha'] / 2)
            evaluator = RarePosteriorEvaluator(model, settings)
            original_seeds = {a['seed'] for a in result['audits']}
            audits = []
            for replicate in (1, 2):
                seed = fresh_seed(ordinal, replicate)
                if seed in original_seeds:
                    raise ValueError('Fresh audit seed overlaps an original audit')
                target = directory / f'fresh_audit_{replicate}.json'
                if target.exists():
                    saved = json.loads(target.read_text())
                    expected = (saved['profile_sha256'] == result['profile_sha256']
                                and saved['source_identity'] == identity
                                and saved['seed'] == seed
                                and saved['count_draws'] == FRESH_COUNT_DRAWS)
                    if not expected:
                        raise ValueError('Fresh audit provenance mismatch')
                else:
                    before = digest(directory / 'profile.npz')
                    audit = evaluator.audit(
                        1, result['p1'], result['p2'], profile,
                        FRESH_COUNT_DRAWS, seed,
                    )
                    check_source(identity)
                    if digest(directory / 'profile.npz') != before:
                        raise RuntimeError('Audit changed the frozen profile')
                    saved = dict(
                        audit=audit,
                        seed=seed,
                        count_draws=FRESH_COUNT_DRAWS,
                        profile_sha256=result['profile_sha256'],
                        source_identity=identity,
                        independent_of_training_and_original_audit_seeds=True,
                        policy_frozen=True,
                    )
                    atomic_write_json(target, clean_json(saved))
                audits.append(saved['audit'])
                print(json.dumps(dict(
                    ordinal=ordinal,
                    replicate=replicate,
                    passed=saved['audit']['bounded_checks_pass'],
                    max_regret_upper=saved['audit']['max_regret_upper'],
                    unresolved=len(saved['audit']['unresolved_histories']),
                )), flush=True)

            rows.append(dict(
                ordinal=ordinal,
                p1=result['p1'],
                p2=result['p2'],
                passed=bool(result['training_regrets']['sample_checks_pass']
                            and all(a['bounded_checks_pass'] for a in audits)),
                max_regret_upper=[a['max_regret_upper'] for a in audits],
                unresolved=[len(a['unresolved_histories']) for a in audits],
                profile_sha256=result['profile_sha256'],
            ))

        atomic_write_json(root / 'fresh_audit_summary.json', dict(
            rows=rows,
            all_repairs_passed=all(row['passed'] for row in rows),
            count_draws_per_replicate=FRESH_COUNT_DRAWS,
            policy_frozen=True,
            original_search_cache_replaced=False,
            external_price_optimized=False,
        ))


if __name__ == '__main__':
    main()

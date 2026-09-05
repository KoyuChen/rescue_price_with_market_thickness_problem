#!/usr/bin/env python3
"""Cold-start finite-type solver and complete specified-grid search for v1.1.1."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace
import json
import multiprocessing
import os
from pathlib import Path
import secrets
import time

for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(key, '1')

import numpy as np

from .storage import source_identity, digest, atomic_write_json, save_profile, load_profile
from .solver import Settings, solve_menu, price_grid, grid_summary, ValueIntegratedEvaluator
from .core import ModelParams, RescueModel, FixedSupportRescueModel, draw_routes
from .config import build_model_params, load_config
from .diagnostics import shape_diagnostics, validate_profile, thickness_diagnostics


def clean_json(value):
    """Unused secondary statistics may be undefined; emit JSON null, not NaN."""
    if isinstance(value, dict):
        return {k: clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean_json(v) for v in value]
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(path, value):
    atomic_write_json(path, clean_json(value))


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['menu', 'grid', 'audit', 'routes'])
    parser.add_argument('--m', nargs='+', type=float, default=[1, 3, 6, 12, 24, 48])
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--step', type=float, default=.05)
    parser.add_argument('--workers', type=int, default=1,
                        help='Parallel thickness workers; does not change draws or results')
    parser.add_argument('--config', help='JSON model configuration; omitted uses v1.1.1 defaults')
    parser.add_argument('--output', required=True)
    parser.add_argument('--mode', choices=['sample', 'enumerate'], default='sample')
    parser.add_argument('--count-cap', type=int, default=12)
    parser.add_argument('--max-states', type=int, default=50000)
    parser.add_argument('--train-counts', type=int, default=512)
    parser.add_argument('--audit-counts', type=int, default=10000)
    parser.add_argument('--audit-seed', type=int, help='Required fresh seed for independent re-audit')
    parser.add_argument('--menu-dir', help='Saved menu directory for re-audit')
    parser.add_argument('--route-draws', type=int, default=10000, help='Raw OD draws for routes command')
    parser.add_argument('--iteration-multiplier', type=int, default=1,
                        help='Multiply every response-stage budget, preserving tolerances')
    parser.add_argument('--selection-markets', type=int, default=50000)
    parser.add_argument('--report-markets', type=int, default=200000)
    parser.add_argument('--seed', type=int, default=2026090501, help='Solver/market seed, distinct from route seed')
    parser.add_argument('--route-seed', type=int, help='Omit to generate a fresh random OD sample; actual seed is recorded')
    parser.add_argument('--init', choices=['homotopy', 'early', 'hidden'], default='homotopy')
    parser.add_argument('--smoke', action='store_true', help='Low budget software check, NOT research precision')
    parser.add_argument('--resume', action='store_true', help='Reuse only this exact run and verified local profiles')
    args = parser.parse_args(argv)
    if args.command == 'menu' and (args.p1 is None or args.p2 is None):
        parser.error('menu requires --p1 and --p2')
    if args.command == 'audit' and (args.menu_dir is None or args.audit_seed is None):
        parser.error('audit requires --menu-dir and --audit-seed')
    if args.audit_seed is not None and args.audit_seed < 0:
        parser.error('audit-seed must be nonnegative')
    if args.route_draws < 1:
        parser.error('route-draws must be positive')
    if args.command in ('audit', 'routes') and args.resume:
        parser.error('audit and routes require new outputs, not --resume')
    if any(not np.isfinite(m) or m <= 0 for m in args.m) or len(set(args.m)) != len(args.m):
        parser.error('m must be distinct positive finite values')
    for name in ('selection_markets', 'report_markets', 'train_counts', 'audit_counts'):
        if getattr(args, name) < 2:
            parser.error(f'{name} must be >= 2')
    if args.seed < 0 or (args.route_seed is not None and args.route_seed < 0):
        parser.error('Seeds must be nonnegative')
    if args.iteration_multiplier < 1:
        parser.error('iteration-multiplier must be positive')
    if args.workers < 1:
        parser.error('workers must be positive')
    return args


def create_model(config, route_seed):
    """Random OD sample -> finite support, kept common across menu comparisons."""
    params = build_model_params(config['model'])
    return RescueModel(replace(params, seed=route_seed))


def audit_saved(args):
    folder = Path(args.menu_dir).resolve()
    run = folder.parents[1]
    request = json.loads((run / 'request.json').read_text())
    result = json.loads((folder / 'result.json').read_text())
    if request['baseline'] != source_identity():
        raise ValueError('Source/environment identity mismatch; do not relabel earlier certificates')
    ident = json.loads((run / 'support_identity.json').read_text())
    if digest(run / 'support.npz') != ident['sha256'] or digest(folder / 'profile.npz') != result['profile_sha256']:
        raise ValueError('Support or profile checksum mismatch')
    if result['settings'] != request['settings'] or result['m'] not in request['m'] or [result['p1'], result['p2']] not in request['menus']:
        raise ValueError('Stored menu does not belong to this run')
    used = {request['settings']['seed']} | {a['seed'] for a in result['audits']}
    if args.audit_seed in used:
        raise ValueError('Independent audit requires a seed not used for training or the original audits')
    target = Path(args.output).resolve()
    if target.exists():
        raise FileExistsError('Audit output already exists')
    params = build_model_params(request['model'])
    with np.load(run / 'support.npz', allow_pickle=False) as d:
        model = FixedSupportRescueModel(params, d['c'], d['fc'], d['s'], d['fs'])
    profile = load_profile(folder / 'profile.npz')
    validate_profile(model, result['p1'], result['p2'], profile)
    settings = replace(Settings(**request['settings']), audit_counts=args.audit_counts,
                       count_cap=args.count_cap, max_states=args.max_states)
    audit = ValueIntegratedEvaluator(model, settings).audit(result['m'], result['p1'], result['p2'],
                                                           profile, args.audit_counts, args.audit_seed)
    audit.update(m=result['m'], p1=result['p1'], p2=result['p2'],
                 profile_sha256=result['profile_sha256'], source_identity=source_identity(),
                 status='independent_reaudit', changes_policy=False)
    write_json(target, audit)
    print(json.dumps(dict(stage='audit_finished', output=str(target),
                         bounded_checks_pass=audit['bounded_checks_pass'])), flush=True)
    return 0 if audit['bounded_checks_pass'] else 2


def route_example(args):
    target = Path(args.output).resolve()
    if target.exists():
        raise FileExistsError('Route output already exists')
    seed = secrets.randbits(32) if args.route_seed is None else args.route_seed
    params = build_model_params(load_config(args.config)['model'])
    routes = draw_routes(params, args.route_draws, seed)
    target.mkdir(parents=True)
    np.savez_compressed(target / 'routes.npz', **routes)
    report = dict(route_seed=seed, draws=args.route_draws,
        mean_overlap=float(routes['overlap'].mean()),
        zero_overlap_fraction=float(np.mean(routes['overlap'] == 0)),
        same_direction_fraction=float(routes['same_direction'].mean()),
        model=asdict(params), file_sha256=digest(target / 'routes.npz'),
        interpretation='Raw random OD draws, not an equilibrium or fitted market result.')
    write_json(target / 'summary.json', report)
    print(json.dumps(dict(stage='routes_finished', output=str(target), route_seed=seed)), flush=True)
    return 0


def run_thickness(task):
    """One disjoint output folder per worker; seeds depend on design, not schedule."""
    im, m, menus, model, settings, args, output = task
    rows, profiles = [], []
    folder = output / f'thickness_{im:03d}'; folder.mkdir(exist_ok=True)
    for j, (p1, p2) in enumerate(menus):
        item = folder / f'menu_{j:05d}'; item.mkdir(exist_ok=True)
        result_path = item / 'result.json'
        if result_path.exists():
            result = json.loads(result_path.read_text())
            if digest(item / 'profile.npz') != result['profile_sha256']:
                raise ValueError('Profile checksum mismatch; cannot resume')
            if (result['m'], result['p1'], result['p2']) != (m, p1, p2):
                raise ValueError('Cached candidate coordinates mismatch')
            profile = load_profile(item / 'profile.npz')
        else:
            start = time.monotonic()
            print(json.dumps(dict(stage='solve', m=m, p1=p1, p2=p2, menu=j + 1, total=len(menus))), flush=True)
            def progress(row):
                print(json.dumps(dict(stage='iteration', m=m, p1=p1, p2=p2, **row)), flush=True)
            profile, result = solve_menu(model, m, p1, p2, settings, args.init, progress)
            policy = (p1, p2, profile)
            selected, _, _ = model.paired_evaluate(m, policy, policy, n_markets=args.selection_markets,
                seed=args.seed + 2000003 + im * 10007, batch_size=5000)
            result.update(selection_completion=selected['completion'], selection_se=selected['completion_se'],
                          selection_markets=args.selection_markets,
                          elapsed_seconds=time.monotonic() - start)
            save_profile(item / 'profile.npz', profile)
            result['profile_sha256'] = digest(item / 'profile.npz')
            write_json(result_path, result)
        rows.append(result); profiles.append(profile)
        write_json(folder / 'progress.json', dict(completed=len(rows), expected=len(menus),
                          unresolved=sum(not r['numerical_checks_passed'] for r in rows)))
    if args.command == 'grid':
        summary = grid_summary(rows, menus)
        ri, fi = summary['raw_rescue_leader_index'], summary['raw_flat_leader_index']
        write_json(folder / 'frozen_selection.json', dict(rescue_index=ri, flat_index=fi,
                          rescue_profile_sha256=rows[ri]['profile_sha256'],
                          flat_profile_sha256=rows[fi]['profile_sha256']))
        rp1, rp2 = menus[ri]; fp1, fp2 = menus[fi]
        r, f, comparison = model.paired_evaluate(m, (rp1, rp2, profiles[ri]), (fp1, fp2, profiles[fi]),
            n_markets=args.report_markets, seed=args.seed + 4000037 + im * 10007, batch_size=5000)
        def evidence(row):
            return dict(status=row['status'], numerical_checks_passed=row['numerical_checks_passed'],
                training_regrets=row['training_regrets'],
                audit_max_regrets=[a['regrets']['max_regret'] for a in row['audits']],
                audit_sample_checks_pass=[a['regrets']['sample_checks_pass'] for a in row['audits']],
                audit_max_regret_uppers=[a['max_regret_upper'] for a in row['audits']])
        summary.update(m=m, p1=rp1, p2=rp2, p_flat=fp1, rescue=r, flat=f, comparison=comparison,
            rescue_evidence=evidence(rows[ri]), flat_evidence=evidence(rows[fi]),
            V_estimate=r['completion'] - f['completion'],
            V_is_certified_optimized_value=False, reporting_draws_never_change_selection=True,
            negative_gain_preserved=True, diagonal_reuses_identical_profile=True)
    else:
        summary = rows[0]
    write_json(folder / 'summary.json', summary)
    print(json.dumps(dict(stage='thickness_finished', m=m, output=str(folder))), flush=True)
    return summary


def main(argv=None):
    args = parse_args(argv)
    if args.command == 'audit':
        return audit_saved(args)
    if args.command == 'routes':
        return route_example(args)
    provenance = source_identity()
    output = Path(args.output).resolve()
    old_request = None
    if output.exists():
        if not args.resume:
            raise FileExistsError('Output exists; use a new directory or --resume with the identical request')
        old_request = json.loads((output / 'request.json').read_text())
    elif args.resume:
        raise FileNotFoundError('--resume requires an existing run')
    route_seed = (old_request['route_seed'] if args.route_seed is None and old_request else
                  secrets.randbits(32) if args.route_seed is None else args.route_seed)
    config = load_config(args.config)
    params = replace(build_model_params(config['model']), seed=route_seed)
    settings = Settings(mode=args.mode, train_counts=args.train_counts, audit_counts=args.audit_counts,
                        count_cap=args.count_cap, max_states=args.max_states, seed=args.seed)
    if args.smoke:
        settings = replace(settings, train_counts=min(64, args.train_counts), audit_counts=min(512, args.audit_counts),
                           schedule=((.02, 4, .4), (.003, 5, .3), (.0003, 5, .2), (0., 6, .15)))
    settings = replace(settings, schedule=tuple((t, n*args.iteration_multiplier, d) for t, n, d in settings.schedule))
    settings.validate()
    prices = price_grid(args.step, params.p_bar) if args.command == 'grid' else None
    menus = [(a, b) for i, a in enumerate(prices) for b in prices[i:]] if prices else [(args.p1, args.p2)]
    for p1, p2 in menus:
        if not (np.isfinite(p1) and np.isfinite(p2) and 0 <= p1 <= p2 <= params.p_bar):
            raise ValueError('Invalid menu')
    request = dict(baseline=provenance, solver_sha256=digest(Path(__file__).with_name('solver.py')),
        runner_sha256=digest(__file__), model=asdict(params), settings=asdict(settings),
        route_seed=route_seed, market_seed=args.seed, command=args.command, m=args.m,
        menus=menus, init=args.init, smoke=args.smoke, selection_markets=args.selection_markets,
        report_markets=args.report_markets,
        route_simulation='IID origins, lengths and directions -> random overlap distribution; '
                         'independent IID categorical route types in market evaluation.',
        route_discretization='Finite-type equilibrium approximation, NOT a continuous-route WPBE.',
        v12_candidates_imported=False)
    request = json.loads(json.dumps(request))
    if old_request is not None and old_request != request:
        raise ValueError('Resume request/source identity mismatch; start a new output directory')
    if old_request is None:
        output.mkdir(parents=True)
        write_json(output / 'request.json', request)
        model = create_model(config, route_seed)
        np.savez_compressed(output / 'support.npz', c=model.c, fc=model.fc, s=model.s, fs=model.fs)
        write_json(output / 'support_identity.json', dict(sha256=digest(output / 'support.npz'),
            route_seed=route_seed, route_draws=params.route_draws, costs=model.C, fits=model.S))
    else:
        ident = json.loads((output / 'support_identity.json').read_text())
        if digest(output / 'support.npz') != ident['sha256']:
            raise ValueError('Support checksum mismatch')
        with np.load(output / 'support.npz', allow_pickle=False) as d:
            model = FixedSupportRescueModel(params, d['c'], d['fc'], d['s'], d['fs'])
    print(json.dumps(dict(stage='start', route_seed=route_seed, finite_types=[model.C, model.S],
                          total_menus=len(args.m) * len(menus), smoke=args.smoke)), flush=True)
    tasks = [(im, m, menus, model, settings, args, output) for im, m in enumerate(args.m)]
    if args.workers == 1 or len(tasks) == 1:
        summaries = [run_thickness(t) for t in tasks]
    else:
        with ProcessPoolExecutor(max_workers=min(args.workers, len(tasks)),
                                 mp_context=multiprocessing.get_context('spawn')) as pool:
            summaries = list(pool.map(run_thickness, tasks))
    final = dict(status='completed', smoke=args.smoke, route_seed=route_seed, results=summaries,
                 wpbe_certified=False, v12_candidates_imported=False)
    if args.command == 'grid' and len(summaries) >= 3:
        ordered = sorted(summaries, key=lambda row: row['m'])
        final['shape_diagnostic'] = shape_diagnostics([r['m'] for r in ordered],
            [r['V_estimate'] for r in ordered], [r['comparison']['completion_gain_se'] for r in ordered])
        final['shape_diagnostic']['inputs_equilibrium_certified'] = False
        final['thickness_diagnostic'] = thickness_diagnostics(ordered)
    write_json(output / 'summary.json', final)
    print(json.dumps(dict(stage='finished', output=str(output), wpbe_certified=False)), flush=True)
    # 0: numerical checks completed; 2: completed with unresolved evidence.
    good = all(r.get('numerical_grid_comparison_ready', r.get('numerical_checks_passed', False)) for r in summaries)
    return 0 if good else 2


if __name__ == '__main__':
    raise SystemExit(main())

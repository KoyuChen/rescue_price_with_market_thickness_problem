#!/usr/bin/env python3
"""Resume the saved m=3 branch with added history exclusion and fresh audits.

Original files and running thick-market sources stay unchanged. Every update,
completed audit and frozen-menu report is checkpointed. Same command resumes.
This is fixed-menu validation, not external price optimization.
"""
import argparse
from dataclasses import asdict, replace
import fcntl
import json
import os
from pathlib import Path
import time
import datetime
import numpy as np
from rescue_solver.core import FixedSupportRescueModel, Profile
from rescue_solver.config import build_model_params
from rescue_solver.solver import Settings, best_response
from rescue_solver.diagnostics import regret_diagnostics
from rescue_solver.storage import atomic_write_json, digest, load_profile, save_profile
from rescue_solver.cli import clean_json
from research_solver.solve import polish_support
from checkpoint_solver import fingerprint, write_checkpoint
from history_envelope import EnvelopeHistoryEvaluator
from run_research import check_source, source_identity

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', required=True)
    parser.add_argument('--model-request', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--train-counts', type=int, default=50000)
    parser.add_argument('--audit-counts', type=int, default=1000000)
    parser.add_argument('--steps', type=int, default=300)
    parser.add_argument('--report-markets', type=int, default=10000000)
    parser.add_argument('--seed', type=int, default=2026090617)
    args = parser.parse_args()
    if min(args.train_counts, args.audit_counts, args.steps, args.report_markets) < 2:
        parser.error('Budgets must be at least two')
    source = Path(args.input_root).resolve(); output = Path(args.output).resolve()
    if source == output or source in output.parents:
        parser.error('Use a separate output, outside original results')
    output.mkdir(parents=True, exist_ok=True)
    with (output/'runner.lock').open('a+') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise SystemExit('Already running; duplicate rejected')
        identity = source_identity()
        for name in ('history_envelope.py', 'reactivate_m3.py', 'checkpoint_solver.py'):
            identity['sha256'][name] = digest(ROOT/name)
        settings = Settings(train_counts=args.train_counts, audit_counts=args.audit_counts,
            count_batch_size=64, seed=args.seed, alpha=.05/8,
            schedule=((0., args.steps, .1),))
        settings.validate()
        request = dict(input_root=str(source), model_request=str(Path(args.model_request).resolve()),
            settings=asdict(settings), report_markets=args.report_markets,
            source_identity=identity, m=3., price_optimized=False,
            input_sha256={str(f.relative_to(source)):digest(f)
                for name in ('m3_rescue','m3_flat')
                for f in (source/name/'result.json',source/name/'profile.npz',source/name/'support.json')},
            model_request_sha256=digest(args.model_request))
        request = clean_json(request)
        if (output/'request.json').exists():
            if json.loads((output/'request.json').read_text()) != request:
                raise ValueError('Resume input, settings or source mismatch')
        else: atomic_write_json(output/'request.json', request)
        atomic_write_json(output/'supervisor.json', dict(pid=os.getpid(), status='running',
            started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))

        def log(event):
            row = clean_json(dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), **event))
            print(json.dumps(row), flush=True)
            with (output/'progress.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')

        params = build_model_params(json.loads(Path(args.model_request).read_text())['config']['model'])
        rows = {}; profiles = {}; supports = {}; models = {}
        for name in ('m3_rescue','m3_flat'):
            directory = output/name; directory.mkdir(exist_ok=True)
            input_dir = source/name
            prior = json.loads((input_dir/'result.json').read_text())
            check_source(prior['source_identity'])
            if digest(input_dir/'profile.npz') != prior['profile_sha256']:
                raise ValueError('Input profile checksum mismatch')
            support = json.loads((input_dir/'support.json').read_text()); supports[name]=support
            edges = tuple(np.r_[0.,np.cumsum(support['fc'])]); edges=edges[:-1]+(1.,)
            model = FixedSupportRescueModel(replace(params,cost_probability_edges=edges),
                *[np.asarray(support[k]) for k in ('c','fc','s','fs')]); models[name]=model
            x,w=np.polynomial.legendre.leggauss(64); model.tie_t=(x+1)/2; model.tie_w=w/2
            p1,p2 = prior['p1'],prior['p2']
            key=fingerprint(model,3.,p1,p2,settings,directory.name+json.dumps(request,sort_keys=True))
            checkpoint=directory/'checkpoint.npz'
            if checkpoint.exists():
                with np.load(checkpoint,allow_pickle=False) as z:
                    state=json.loads(str(z['state_json'].item()))
                    if state['fingerprint'] != key: raise ValueError('Checkpoint mismatch')
                    profile=Profile(z['sigma_e'].copy(),z['sigma_h'].copy(),
                        z['retain'].copy(),z['q_values'].copy(),{})
            else:
                profile=load_profile(input_dir/'profile.npz')
                state=dict(fingerprint=key,iteration=0,training_done=False,audits=[])
                write_checkpoint(checkpoint,profile,state)
            evaluator=EnvelopeHistoryEvaluator(model,settings)
            log(dict(menu=name,stage='menu_started',iteration=state['iteration']))
            if not state['training_done']:
                for step in range(state['iteration'],args.steps):
                    ev=evaluator.evaluate(3.,p1,p2,profile,args.train_counts,args.seed)
                    if polish_support(model,profile,ev,settings.support_tol):
                        ev=evaluator.evaluate(3.,p1,p2,profile,args.train_counts,args.seed)
                    diagnostic=regret_diagnostics(model,p1,profile,ev,
                        settings.regret_tol/4,settings.support_tol/4)
                    if step%5==0:
                        log(dict(menu=name,stage='iteration',iteration=step,
                            max_regret=diagnostic['max_regret'],
                            support_gap=max(diagnostic['initial_support_gap_max'],diagnostic['retention_support_gap_max']),
                            unknown=ev['unknown_feasible_history_count'],
                            envelope_certificates=ev['count_envelope_certificates']))
                    if diagnostic['sample_checks_pass'] and ev['unknown_feasible_history_count']==0:
                        break
                    br,rr=best_response(model,profile,ev,0.,settings.response_tie_tol)
                    rr=np.where(ev['unknown_old_history'].T[:,None,:],profile.retain,rr)
                    rr=np.where(ev['offpath_certified'].T[:,None,:],0.,rr)
                    profile.sigma_e=.9*profile.sigma_e+.1*br[0]
                    profile.sigma_h=.9*profile.sigma_h+.1*br[1]
                    profile.retain=.9*profile.retain+.1*rr
                    state['iteration']=step+1
                    write_checkpoint(checkpoint,profile,state)
                state['training_done']=True
                write_checkpoint(checkpoint,profile,state)
            ev=evaluator.evaluate(3.,p1,p2,profile,args.train_counts,args.seed)
            diagnostic=regret_diagnostics(model,p1,profile,ev)
            for j in range(len(state['audits']),2):
                log(dict(menu=name,stage='audit_started',replicate=j+1,count_draws=args.audit_counts))
                audit=evaluator.audit(3.,p1,p2,profile,args.audit_counts,args.seed+1000003+j*104729)
                state['audits'].append(audit); write_checkpoint(checkpoint,profile,state)
                log(dict(menu=name,stage='audit_finished',replicate=j+1,
                    passed=audit['bounded_checks_pass'],unresolved=len(audit['unresolved_histories']),
                    max_regret_upper=audit['max_regret_upper']))
            passed=diagnostic['sample_checks_pass'] and all(a['bounded_checks_pass'] for a in state['audits'])
            save_profile(directory/'profile.npz',profile)
            atomic_write_json(directory/'support.json',support)
            result=dict(m=3.,p1=p1,p2=p2,status='finite_support_checks_passed' if passed else 'validation_blocked',
                numerical_checks_passed=bool(passed),training_regrets=diagnostic,audits=state['audits'],
                source_identity=identity,profile_sha256=digest(directory/'profile.npz'),
                cost_points=model.C,route_points=model.S,tie_quadrature_order=64,
                input_profile_sha256=prior['profile_sha256'],settings=asdict(settings),
                iterations=state['iteration'],price_optimized=False,wpbe_certified=False,
                continuous_type_convergence_verified=False)
            check_source(identity); atomic_write_json(directory/'result.json',clean_json(result))
            rows[name]=result; profiles[name]=profile
            log(dict(menu=name,stage='menu_finished',status=result['status']))
        summary=dict(m=3.,status='validation_finished',menus={k:v['status'] for k,v in rows.items()},
                     price_optimized=False,wpbe_certified=False)
        if all(row['numerical_checks_passed'] for row in rows.values()):
            if supports['m3_rescue'] != supports['m3_flat']: raise ValueError('Comparison support mismatch')
            report_path=output/'fixed_menu_m3_report.json'
            if not report_path.exists():
                log(dict(stage='fixed_menu_report_started',markets=args.report_markets))
                model=models['m3_rescue']; a=rows['m3_rescue']; b=rows['m3_flat']
                ra,rb,comparison=model.paired_evaluate(3.,
                    (a['p1'],a['p2'],profiles['m3_rescue']),
                    (b['p1'],b['p2'],profiles['m3_flat']),args.report_markets,args.seed+900000019)
                report=dict(m=3.,rescue=ra,flat=rb,comparison=comparison,
                    markets=args.report_markets,seed=args.seed+900000019,
                    source_identity=identity,price_optimized=False,wpbe_certified=False,
                    profile_sha256={k:v['profile_sha256'] for k,v in rows.items()})
                atomic_write_json(report_path,clean_json(report))
            summary['fixed_menu_report']=str(report_path)
        atomic_write_json(output/'summary.json',summary)
        atomic_write_json(output/'supervisor.json',dict(pid=os.getpid(),status='finished'))
        log(summary)
        return 0 if all(r['numerical_checks_passed'] for r in rows.values()) else 2


if __name__=='__main__':
    raise SystemExit(main())

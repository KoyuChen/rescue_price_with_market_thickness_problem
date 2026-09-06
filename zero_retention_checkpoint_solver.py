"""Isolated restartable solver adding the zero-retention all-count certificate.

Same updates, count draws, seeds, quadrature and audit thresholds; floating-point
reduction order can differ. Every run records this module in its source identity.

State and policy are one atomic NPZ. A crash can lose only the currently
executing evaluation/audit, never an already committed iteration.
"""
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import tempfile
import numpy as np
from rescue_solver.core import Profile
from rescue_solver.cli import clean_json
from rescue_solver.solver import Settings, best_response, complementarity_diagnostics
from rescue_solver.diagnostics import regret_diagnostics
from zero_retention_envelope import ZeroRetentionEnvelopeEvaluator as CachedEnvelopeEvaluator
from research_solver.solve import polish_support


def fingerprint(model, m, p1, p2, settings, source):
    h = hashlib.sha256(json.dumps(dict(model=asdict(model.par), m=m, p1=p1,
        p2=p2, settings=asdict(settings), source=source), sort_keys=True).encode())
    for name in ('c', 'fc', 's', 'fs', 'tie_t', 'tie_w'):
        a = np.ascontiguousarray(getattr(model, name))
        h.update(str((name, a.shape, a.dtype.str)).encode()); h.update(a.tobytes())
    return h.hexdigest()


def write_checkpoint(path, profile, state):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name+'.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            np.savez_compressed(f, sigma_e=profile.sigma_e, sigma_h=profile.sigma_h,
                retain=profile.retain, q_values=profile.q_values,
                state_json=np.asarray(json.dumps(clean_json(state), allow_nan=False,
                                                 sort_keys=True)))
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
        fd = os.open(path.parent, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def solve_checkpointed(model, m, p1, p2, settings, checkpoint, source, progress=None):
    settings.validate()
    if not np.isfinite(m) or m <= 0 or not 0 <= p1 <= p2 <= model.par.p_bar:
        raise ValueError('Invalid market thickness or menu')
    key = fingerprint(model, m, p1, p2, settings, source)
    checkpoint = Path(checkpoint)
    if checkpoint.exists():
        with np.load(checkpoint, allow_pickle=False) as d:
            state = json.loads(str(d['state_json'].item()))
            if state['fingerprint'] != key:
                raise ValueError('Checkpoint input/source fingerprint mismatch')
            profile = Profile(d['sigma_e'].copy(), d['sigma_h'].copy(),
                d['retain'].copy(), d['q_values'].copy(), {})
        if progress: progress(dict(stage='checkpoint_resumed', iteration=state['iteration']))
    else:
        e, h, r = model._initial_profile(p1, p2, 'homotopy')
        profile = Profile(e, h, r, np.unique(np.round([p1, p2], 12)), {})
        state = dict(fingerprint=key, stage_index=0, next_step=0, iteration=0,
                     history=[], audits=[], last_diagnostic=None)
        write_checkpoint(checkpoint, profile, state)
    evaluator = CachedEnvelopeEvaluator(model, settings)
    for index in range(state['stage_index'], len(settings.schedule)):
        temperature, steps, damping = settings.schedule[index]
        diagnostic = state['last_diagnostic']
        for step in range(state['next_step'], steps):
            ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
            if temperature == 0:
                if polish_support(model, profile, ev, settings.support_tol):
                    ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
            diagnostic = regret_diagnostics(model, p1, profile, ev,
                settings.regret_tol/4, settings.support_tol/4)
            if temperature == 0 and diagnostic['sample_checks_pass'] and not ev['unknown_feasible_history_count']:
                break
            br, rr = best_response(model, profile, ev, temperature, settings.response_tie_tol)
            rr = np.where(ev['unknown_old_history'].T[:, None, :], profile.retain, rr)
            rr = np.where(ev['offpath_certified'].T[:, None, :], 0., rr)
            profile.sigma_e = (1-damping)*profile.sigma_e+damping*br[0]
            profile.sigma_h = (1-damping)*profile.sigma_h+damping*br[1]
            profile.retain = (1-damping)*profile.retain+damping*rr
            state.update(next_step=step+1, iteration=state['iteration']+1,
                         last_diagnostic=diagnostic)
            write_checkpoint(checkpoint, profile, state)
            if progress and step % 5 == 0:
                progress(dict(stage='iteration', temperature=temperature,
                    iteration=state['iteration'], max_regret=diagnostic['max_regret'],
                    unknown=ev['unknown_feasible_history_count']))
        row = dict(temperature=temperature, iteration=state['iteration'], diagnostics=diagnostic)
        state['history'].append(row)
        state.update(stage_index=index+1, next_step=0, last_diagnostic=diagnostic)
        write_checkpoint(checkpoint, profile, state)
        if progress: progress(dict(stage='temperature_finished', **row))
    ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
    diagnostic = regret_diagnostics(model, p1, profile, ev, settings.regret_tol, settings.support_tol)
    for j in range(len(state['audits']), settings.audit_replicates):
        if progress: progress(dict(stage='audit_started', replicate=j+1, count_draws=settings.audit_counts))
        audit = evaluator.audit(m, p1, p2, profile, settings.audit_counts,
                                settings.seed+1000003+j*104729)
        state['audits'].append(audit)
        write_checkpoint(checkpoint, profile, state)
        if progress: progress(dict(stage='audit_finished', replicate=j+1,
            passed=audit['bounded_checks_pass'], unresolved=len(audit['unresolved_histories']),
            full_plan_upper=audit['full_plan_regret_upper'], retention_upper=audit['retention_regret_upper']))
    audits = state['audits']
    passed = diagnostic['sample_checks_pass'] and all(a['bounded_checks_pass'] for a in audits)
    profile.meta = dict(early_share=float(np.sum(model.type_mass*profile.sigma_e)),
        hidden_share=float(np.sum(model.type_mass*profile.sigma_h)),
        max_regret=max(a['regrets']['max_regret'] for a in audits), iterations=state['iteration'])
    return profile, dict(m=m, p1=p1, p2=p2, settings=asdict(settings),
        status='finite_support_checks_passed' if passed else 'validation_blocked',
        numerical_checks_passed=bool(passed), training_regrets=diagnostic,
        unknown_training_histories=ev['unknown_feasible_history_count'], audits=audits,
        complementarity=complementarity_diagnostics(model, p1, profile, ev),
        iteration_history=state['history'], external_price_optimized=False,
        continuous_type_convergence_verified=False, quadrature_convergence_verified=False,
        equilibrium_uniqueness_proved=False, wpbe_certified=False,
        branch_rule='Common homotopy cold start, zero-temperature polishing; no outcome-based branch choice.')

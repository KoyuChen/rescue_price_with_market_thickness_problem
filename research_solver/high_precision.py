"""High-precision cold-start solver; old run sources remain immutable."""
from dataclasses import asdict
import numpy as np
from rescue_solver.core import Profile
from rescue_solver.solver import Settings,best_response,complementarity_diagnostics
from rescue_solver.diagnostics import regret_diagnostics
from .certified import CertifiedPayoffEvaluator
from .solve import polish_support

def solve_high(model, m, p1, p2, settings=None, progress=None):
    settings = settings or Settings(train_counts=50000, audit_counts=1000000,
        count_batch_size=64, schedule=((.02,40,.35),(.004,60,.25),(.0005,100,.15),(0.,500,.1)))
    settings.validate()
    if not np.isfinite(m) or m<=0 or not 0<=p1<=p2<=model.par.p_bar:
        raise ValueError('Invalid market thickness or menu')
    e, h, r = model._initial_profile(p1, p2, 'homotopy')
    profile = Profile(e, h, r, np.unique(np.round([p1, p2], 12)), {})
    evaluator = CertifiedPayoffEvaluator(model, settings)
    history = []; iteration = 0
    # Solve more tightly than the acceptance thresholds to leave audit margin.
    train_regret = settings.regret_tol/4
    train_support = settings.support_tol/4
    for temperature, steps, damping in settings.schedule:
        for step in range(steps):
            ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
            if temperature==0:
                if polish_support(model, profile, ev, settings.support_tol):
                    ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
            diagnostic = regret_diagnostics(model, p1, profile, ev, train_regret, train_support)
            if temperature==0 and diagnostic['sample_checks_pass'] and not ev['unknown_feasible_history_count']:
                break
            br, rr = best_response(model, profile, ev, temperature, settings.response_tie_tol)
            # An unobserved, unproved conditional event never receives a fake posterior.
            rr = np.where(ev['unknown_old_history'].T[:, None, :], profile.retain, rr)
            rr = np.where(ev['offpath_certified'].T[:, None, :], 0., rr)
            profile.sigma_e = (1-damping)*profile.sigma_e+damping*br[0]
            profile.sigma_h = (1-damping)*profile.sigma_h+damping*br[1]
            profile.retain = (1-damping)*profile.retain+damping*rr
            iteration += 1
            if progress and step%5==0:
                progress(dict(stage='iteration', temperature=temperature, iteration=iteration,
                    max_regret=diagnostic['max_regret'], unknown=ev['unknown_feasible_history_count']))
        row = dict(temperature=temperature, iteration=iteration, diagnostics=diagnostic)
        history.append(row)
        if progress: progress(dict(stage='temperature_finished', **row))
    ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
    diagnostic = regret_diagnostics(model, p1, profile, ev, settings.regret_tol, settings.support_tol)
    audits = []
    for j in range(settings.audit_replicates):
        if progress: progress(dict(stage='audit_started', replicate=j+1, count_draws=settings.audit_counts))
        audit = evaluator.audit(m, p1, p2, profile, settings.audit_counts,
                                settings.seed+1000003+j*104729)
        audits.append(audit)
        if progress: progress(dict(stage='audit_finished', replicate=j+1,
            passed=audit['bounded_checks_pass'], unresolved=len(audit['unresolved_histories']),
            full_plan_upper=audit['full_plan_regret_upper'], retention_upper=audit['retention_regret_upper']))
    passed = diagnostic['sample_checks_pass'] and all(a['bounded_checks_pass'] for a in audits)
    profile.meta = dict(early_share=float(np.sum(model.type_mass*profile.sigma_e)),
        hidden_share=float(np.sum(model.type_mass*profile.sigma_h)),
        max_regret=max(a['regrets']['max_regret'] for a in audits), iterations=iteration)
    return profile, dict(m=m, p1=p1, p2=p2, settings=asdict(settings),
        status='finite_support_checks_passed' if passed else 'validation_blocked',
        numerical_checks_passed=bool(passed), training_regrets=diagnostic,
        unknown_training_histories=ev['unknown_feasible_history_count'], audits=audits,
        complementarity=complementarity_diagnostics(model, p1, profile, ev),
        iteration_history=history, external_price_optimized=False,
        continuous_type_convergence_verified=False, quadrature_convergence_verified=False,
        equilibrium_uniqueness_proved=False, wpbe_certified=False,
        branch_rule='Common homotopy cold start, zero-temperature polishing; no outcome-based branch choice.')


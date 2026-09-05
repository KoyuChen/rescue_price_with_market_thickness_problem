"""New finite-type numerical solver using ONLY the frozen v1.1.1 economics.

Integrates uniform rider values over the piecewise-linear upper envelope.
Poisson rivals are either sampled or exhaustively enumerated to a total-count
cap. Enumeration retains the omitted probability as an error bound, never
renormalizes it. No finite-grid or numerical pass is a continuous WPBE proof.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Callable

import numpy as np

from . import core as engine
from .diagnostics import regret_diagnostics, validate_profile


@dataclass(frozen=True)
class Settings:
    mode: str = 'sample'
    train_counts: int = 512
    audit_counts: int = 10000
    count_cap: int = 12
    max_states: int = 50000
    count_batch_size: int = 256
    schedule: tuple = ((.02, 30, .35), (.004, 40, .25), (.0005, 60, .15), (0., 100, .10))
    regret_tol: float = .00075
    support_tol: float = .0015
    response_tie_tol: float = 1e-8
    seed: int = 2026090501
    audit_replicates: int = 2
    alpha: float = .05

    def validate(self):
        if self.mode not in ('sample', 'enumerate'):
            raise ValueError('mode must be sample or enumerate')
        for k in ('train_counts', 'audit_counts', 'max_states', 'audit_replicates', 'count_batch_size'):
            if isinstance(getattr(self, k), bool) or not isinstance(getattr(self, k), int) or getattr(self, k) < 1:
                raise ValueError(f'{k} must be a positive integer')
        if not isinstance(self.count_cap, int) or self.count_cap < 0:
            raise ValueError('count_cap must be a nonnegative integer')
        if not self.schedule or self.schedule[-1][0] != 0:
            raise ValueError('A final zero-temperature stage is required')
        for t, n, damping in self.schedule:
            if not math.isfinite(t) or t < 0 or not isinstance(n, int) or n < 1 or not 0 < damping <= 1:
                raise ValueError('Invalid response schedule')
        if not 0 < self.alpha < 1 or not 0 < self.regret_tol < 1:
            raise ValueError('Invalid audit tolerance')
        if not math.isfinite(self.support_tol) or not 0 < self.support_tol < 1:
            raise ValueError('Invalid support tolerance')
        if not 0 <= self.response_tie_tol <= self.regret_tol:
            raise ValueError('Invalid tie tolerance')
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or self.seed < 0:
            raise ValueError('Invalid solver seed')


def poisson_states(lam, cap, max_states):
    """All vectors with total <= cap; exact product masses, and omitted tail."""
    lam = np.asarray(lam, float)
    if lam.ndim != 1 or not len(lam) or not np.all(np.isfinite(lam)) or np.any(lam < 0):
        raise ValueError('Poisson intensities must be finite, nonnegative and one-dimensional')
    if not isinstance(cap, int) or cap < 0 or not isinstance(max_states, int) or max_states < 1:
        raise ValueError('Invalid enumeration budget')
    active = np.flatnonzero(lam > 0)
    size = math.comb(cap + len(active), len(active))
    if size > max_states:
        raise ValueError(f'Enumeration needs {size} states, exceeds max_states={max_states}; '
                         'use sample mode or a deliberately smaller test model')
    states, weights = [], []
    row = np.zeros(len(lam), dtype=int)

    def visit(j, remaining, weight):
        if j == len(active):
            states.append(row.copy()); weights.append(weight)
            return
        s = active[j]
        for k in range(remaining + 1):
            row[s] = k
            visit(j + 1, remaining - k, weight)
            weight *= lam[s] / (k + 1)
        row[s] = 0

    visit(0, cap, math.exp(-float(lam.sum())))
    weights = np.asarray(weights)
    tail = max(0., 1. - math.fsum(weights))
    return np.asarray(states), weights, tail


class ValueIntegratedEvaluator:
    """Uses the baseline's Bayes/tie/economic rules; changes integration only.

    Floating-point breakpoints and the baseline's 10-node tie quadrature are
    numerical approximations. Probability bounds below cover count truncation
    or sampling, not floating-point, route-support or quadrature error.
    """
    def __init__(self, model, settings):
        settings.validate()
        self.model = model
        self.settings = settings

    def value_intervals(self, counts, p1, q_values, old_r, lambda_new):
        """Lengths of each rider action on [0,1], partitioned at all hinges.

        Between hinges every action is affine. Every pairwise intersection is
        inserted, so tiny positive-length continuation regions are included.
        Ties follow the original immediate-then-low-price order. Exit at zero.
        """
        model = self.model; beta = model.par.beta
        thresholds = [0., 1.]
        thresholds.extend(p1 + model.par.ell * (1 - model.s))
        for q in q_values:
            thresholds.extend((q + model.beta_detour) / beta)
        edges = np.unique(np.clip(thresholds, 0., 1.))
        left, right = edges[:-1], edges[1:]
        mid = (left + right) / 2
        n, B, A = len(counts), len(mid), 1 + len(q_values)
        slope, bias = np.zeros((n, B, A)), np.zeros((n, B, A))
        best = model.S - 1 - np.argmax(counts[:, ::-1] > 0, axis=1)
        threshold = p1 + model.par.ell * (1 - model.s[best])
        active = (counts.sum(axis=1) > 0)[:, None] & (mid[None, :] > threshold[:, None])
        slope[:, :, 0] = active
        bias[:, :, 0] = -active.astype(float) * threshold[:, None]
        for iq, q in enumerate(q_values):
            go, gn = p1 + model.beta_detour, q + model.beta_detour
            levels = np.unique(np.round(np.r_[go, gn], 12))
            log_no = np.log(np.clip(1 - old_r[iq], 1e-14, 1.))
            cdf = np.empty((n, len(levels)))
            for j, level in enumerate(levels):
                mask = go <= level + 1e-11
                log_none = counts[:, mask] @ log_no[mask] - lambda_new[iq][gn <= level + 1e-11].sum()
                cdf[:, j] = 1 - np.exp(np.minimum(log_none, 0))
            mass = np.diff(np.column_stack([np.zeros(n), cdf]), axis=1)
            enabled = beta * mid[:, None] > levels[None, :]
            slope[:, :, iq + 1] = beta * (mass @ enabled.T)
            bias[:, :, iq + 1] = -(mass * levels) @ enabled.T
        cuts = [np.broadcast_to(left, (n, B)), np.broadcast_to(right, (n, B))]
        for a in range(A):
            for b in range(a + 1, A):
                den = slope[:, :, a] - slope[:, :, b]
                cross = np.divide(bias[:, :, b] - bias[:, :, a], den,
                                  out=np.broadcast_to(left, (n, B)).copy(), where=np.abs(den) > 1e-15)
                cuts.append(np.clip(cross, left, right))
        # Include crossings of the baseline's 1e-12 positive-payoff threshold.
        for a in range(A):
            cross = np.divide(1e-12 - bias[:, :, a], slope[:, :, a],
                              out=np.broadcast_to(left, (n, B)).copy(), where=slope[:, :, a] > 0)
            cuts.append(np.clip(cross, left, right))
        cuts = np.sort(np.stack(cuts, axis=-1), axis=-1)
        widths = np.diff(cuts, axis=-1)
        centers = (cuts[:, :, :-1] + cuts[:, :, 1:]) / 2
        values = slope[:, :, None, :] * centers[:, :, :, None] + bias[:, :, None, :]
        action = np.argmax(values, axis=-1)
        action[np.max(values, axis=-1) <= 1e-12] = -1
        lengths = np.stack([np.sum(widths * (action == a), axis=-1) for a in range(A)], axis=1)
        return lengths, mid

    def _weighted_rates(self, counts, weights, p1, profile, old_r, new_lam):
        """Integrate a bounded-size block; weights keep their GLOBAL mass."""
        model = self.model; Q = len(profile.q_values)
        p_immediate = np.zeros(model.S)
        prob_old = np.zeros((model.S, Q)); num_old = np.zeros_like(prob_old)
        num_new = np.zeros_like(prob_old)
        base, mid = self.value_intervals(counts, p1, profile.q_values, old_r, new_lam)
        prob_base = weights @ base[:, 1:, :].sum(axis=-1)
        completion = float(weights @ base[:, 0, :].sum(axis=-1))
        # Rider continuation completion probability is a min-generalized-cost CDF.
        for iq, q in enumerate(profile.q_values):
            go, gn = p1 + model.beta_detour, q + model.beta_detour
            accept_old = model.par.beta * mid[:, None] - go > 1e-12
            accept_new = model.par.beta * mid[:, None] - gn > 1e-12
            log_none = counts @ (np.log(np.clip(1 - old_r[iq], 1e-14, 1)) * accept_old).T
            log_none -= accept_new @ new_lam[iq]
            completion += float(weights @ np.sum(base[:, iq + 1, :] * (-np.expm1(log_none)), axis=1))
            for s in range(model.S):
                selection = model._tag_selection_probability(counts, np.ones(len(counts)), p1,
                    float(q), float(model.s[s]), 'new', old_r[iq], new_lam[iq])
                length = base[:, iq + 1, :] @ accept_new[:, s]
                num_new[s, iq] = weights @ (selection * length)
        for s in range(model.S):
            tagged = counts.copy(); tagged[:, s] += 1
            lengths, mid = self.value_intervals(tagged, p1, profile.q_values, old_r, new_lam)
            share = np.where(np.sum(counts[:, s + 1:], axis=1) > 0, 0., 1 / (1 + counts[:, s]))
            p_immediate[s] = weights @ (lengths[:, 0, :].sum(axis=1) * share)
            for iq, q in enumerate(profile.q_values):
                prob_old[s, iq] = weights @ lengths[:, iq + 1, :].sum(axis=1)
                selection = model._tag_selection_probability(counts, np.ones(len(counts)), p1,
                    float(q), float(model.s[s]), 'old', old_r[iq], new_lam[iq])
                acceptable = model.par.beta * mid - (p1 + model.beta_detour[s]) > 1e-12
                num_old[s, iq] = weights @ (selection * (lengths[:, iq + 1, :] @ acceptable))
        return dict(p_immediate=p_immediate, prob_old=prob_old, num_old=num_old,
                    num_new=num_new, prob_base=prob_base, completion=completion)

    def evaluate(self, m, p1, p2, profile, n, seed):
        validate_profile(self.model, p1, p2, profile)
        model = self.model; Q = len(profile.q_values)
        if not isinstance(n, int) or n < 1:
            raise ValueError('Positive integer count sample size required')
        lam, old_r, new_lam = model._belief_objects(m, p1, profile.q_values,
                                                  profile.sigma_e, profile.sigma_h, profile.retain)
        if self.settings.mode == 'enumerate':
            counts, weights, tail = poisson_states(lam, self.settings.count_cap, self.settings.max_states)
            radius = tail
        else:
            rng = np.random.default_rng(seed)
            draws = rng.poisson(lam, size=(n, model.S))
            counts, multiplicity = np.unique(draws, axis=0, return_counts=True)
            weights = multiplicity / n; tail = None
            # Simultaneous fixed-profile Hoeffding bound on every rate.
            components = model.S + Q + 3 * Q * model.S
            radius = math.sqrt(math.log(2 * components / self.settings.alpha) / (2 * n))
        total = None
        for start in range(0, len(counts), self.settings.count_batch_size):
            end = start + self.settings.count_batch_size
            part = self._weighted_rates(counts[start:end], weights[start:end], p1, profile, old_r, new_lam)
            if total is None:
                total = part
            else:
                for key in total:
                    total[key] += part[key]
        p_immediate, prob_old, num_old = (total[k] for k in ('p_immediate', 'prob_old', 'num_old'))
        num_new, prob_base, completion = (total[k] for k in ('num_new', 'prob_base', 'completion'))
        # Unknown posterior has a marked placeholder, not a zero-win certificate.
        pi_old = np.divide(num_old, prob_old, out=np.full_like(num_old, .5), where=prob_old > 0)
        pi_new = np.divide(num_new, prob_base, out=np.full_like(num_new, .5), where=prob_base > 0)
        margin_old = model.par.delta * p1 - model.a
        old_joint = num_old.T[:, None, :] * margin_old - prob_old.T[:, None, :] * model.par.omega_old
        u_e = p_immediate[None, :] * (p1 - model.a) + np.maximum(old_joint, 0).sum(axis=0)
        u_e = np.where(model.a <= p1 + 1e-12, u_e, -1e6)
        u_h = np.full_like(model.a, -model.par.omega_hidden)
        for iq, q in enumerate(profile.q_values):
            u_h += num_new[:, iq] * np.maximum(q - model.a, 0)
        adv = pi_old.T[:, None, :] * margin_old - model.par.omega_old
        if self.settings.mode == 'enumerate':
            low = np.divide(num_old, prob_old + radius, out=np.zeros_like(num_old), where=prob_old + radius > 0)
            high = np.divide(num_old + radius, prob_old + radius, out=np.ones_like(num_old), where=prob_old + radius > 0)
        else:
            low = np.maximum(num_old - radius, 0) / np.maximum(prob_old + radius, 1e-300)
            high = np.minimum(1., (num_old + radius) / np.maximum(prob_old - radius, 1e-300))
        # When observed probability and the bound are both zero the history is
        # off-path. Leave [0,1] beliefs unspecified; never impose Bayes there.
        return dict(q_values=profile.q_values, u_e=u_e, u_h=u_h, retain_advantage=adv,
            p_immediate=p_immediate, prob_q_base=prob_base, prob_q_early=prob_old,
            pi_old=pi_old, pi_new=pi_new, lambda_early=lam, old_r=np.asarray(old_r),
            lambda_new=np.asarray(new_lam), old_joint=old_joint,
            pi_old_low=np.clip(low, 0, 1), pi_old_high=np.clip(high, 0, 1),
            count_tail=tail, rate_error_radius=radius, count_states=len(counts),
            completion=completion, zero_old_history_count=int(np.sum(prob_old == 0)))

    def audit(self, m, p1, p2, profile, n, seed):
        ev = self.evaluate(m, p1, p2, profile, n, seed)
        model = self.model; settings = self.settings
        diagnostic = regret_diagnostics(model, p1, profile, ev, settings.regret_tol, settings.support_tol)
        margin = model.par.delta * p1 - model.a
        x = ev['pi_old_low'].T[:, None, :] * margin - model.par.omega_old
        y = ev['pi_old_high'].T[:, None, :] * margin - model.par.omega_old
        low, high = np.minimum(x, y), np.maximum(x, y)
        ret_upper = np.maximum(np.maximum(low, 0) - profile.retain * low,
                               np.maximum(high, 0) - profile.retain * high)
        feasible = model.a <= p1 + 1e-12
        retention_upper = float(ret_upper[:, feasible].max()) if feasible.any() else 0.
        if settings.mode == 'enumerate':
            # For one omitted state, early payoff range is bounded by this
            # conservative envelope. Best response and incumbent each move.
            error = 2 * ev['count_tail'] * (2 * model.par.p_bar + model.par.omega_old + model.par.omega_hidden)
        else:
            # All ex-ante payoffs are Lipschitz in bounded win/event rates.
            error = 2 * ev['rate_error_radius'] * (model.par.p_bar +
                       len(profile.q_values) * (model.par.p_bar + model.par.omega_old))
        initial_upper = diagnostic['full_plan_regret_max'] + error
        upper = max(initial_upper, retention_upper)
        initial_support_upper = diagnostic['initial_support_gap_max'] + error
        ret_support = np.maximum(
            np.where(profile.retain > 1e-3, np.maximum(-low, 0), 0),
            np.where(profile.retain < 1-1e-3, np.maximum(high, 0), 0))
        retention_support_upper = float(ret_support[:, feasible].max()) if feasible.any() else 0.
        bounded_pass = (upper <= settings.regret_tol and
                        max(initial_support_upper, retention_support_upper) <= settings.support_tol)
        return dict(mode=settings.mode, seed=seed, count_draws=n if settings.mode == 'sample' else None,
            count_states=ev['count_states'], count_tail=ev['count_tail'],
            rate_error_radius=ev['rate_error_radius'], regrets=diagnostic,
            max_regret_upper=upper, full_plan_regret_upper=initial_upper,
            retention_regret_upper=retention_upper,
            initial_support_gap_upper=initial_support_upper,
            retention_support_gap_upper=retention_support_upper,
            bounded_regret_check_pass=bool(upper <= settings.regret_tol),
            bounded_support_check_pass=bool(max(initial_support_upper, retention_support_upper) <= settings.support_tol),
            bounded_checks_pass=bool(bounded_pass),
            zero_old_history_count=ev['zero_old_history_count'],
            old_history_probability=ev['prob_q_early'].tolist(),
            old_win_probability_lower=ev['pi_old_low'].tolist(),
            old_win_probability_upper=ev['pi_old_high'].tolist(),
            completion=ev['completion'], alpha=settings.alpha if settings.mode == 'sample' else None,
            wpbe_certified=False,
            scope='Count-law uncertainty only; not a bound on type discretization, tie quadrature or floating point.')


def best_response(model, profile, ev, temperature, tie_tol):
    values = np.stack([ev['u_e'], ev['u_h'], np.zeros_like(model.a)])
    if temperature > 0:
        actions = model._softmax(values, temperature)
        retention = model._sigmoid(ev['retain_advantage'], temperature)
    else:
        allowed = values >= values.max(axis=0) - tie_tol
        previous = np.stack([profile.sigma_e, profile.sigma_h, 1 - profile.sigma_e - profile.sigma_h])
        actions = np.maximum(previous, 0) * allowed
        total = actions.sum(axis=0)
        fallback = allowed / allowed.sum(axis=0)
        actions = np.divide(actions, total, out=fallback, where=total > 0)
        adv = ev['retain_advantage']
        retention = np.where(adv > tie_tol, 1., np.where(adv < -tie_tol, 0., profile.retain))
    # Preserve original feasibility restrictions at every temperature.
    actions[0, model.a > profile.q_values[0] + 1e-12] = 0
    actions[1, model.a > profile.q_values[-1] + 1e-12] = 0
    actions /= actions.sum(axis=0)
    retention = np.where((model.par.delta * profile.q_values[0] - model.a > 0)[None, :, :], retention, 0)
    return actions, retention


def complementarity_diagnostics(model, p1, profile, ev):
    """Unscaled economic residuals, not damped step sizes or a WPBE certificate."""
    actions = np.stack([profile.sigma_e, profile.sigma_h, 1 - profile.sigma_e - profile.sigma_h])
    utilities = np.stack([ev['u_e'], ev['u_h'], np.zeros_like(model.a)])
    slack = utilities.max(axis=0) - utilities
    adv = ev['retain_advantage']
    feasible = model.a <= p1 + 1e-12
    stay_violation = profile.retain * np.maximum(-adv, 0)
    leave_violation = (1 - profile.retain) * np.maximum(adv, 0)
    return dict(simplex_residual=float(np.max(np.abs(actions.sum(axis=0) - 1))),
        initial_complementarity_residual=float(np.max(np.abs(actions * slack))),
        retention_complementarity_residual=float(np.max(np.maximum(stay_violation, leave_violation)[:, feasible]))
            if feasible.any() else 0.,
        payoff_units=True, posterior_uncertainty_not_included=True)


def solve_menu(model, m, p1, p2, settings=None, init='homotopy', progress: Callable | None = None):
    settings = settings or Settings(); settings.validate()
    if not math.isfinite(m) or m <= 0 or init not in ('homotopy', 'early', 'hidden'):
        raise ValueError('Invalid thickness or initialization')
    if not (math.isfinite(p1) and math.isfinite(p2) and 0 <= p1 <= p2 <= model.par.p_bar):
        raise ValueError('Invalid menu')
    pe, ph, ret = model._initial_profile(p1, p2, init)
    profile = engine.Profile(pe, ph, ret, np.unique(np.round([p1, p2], 12)), {})
    evaluator = ValueIntegratedEvaluator(model, settings)
    history = []; train_pass = False; iteration = 0
    for temperature, steps, damping in settings.schedule:
        for _ in range(steps):
            ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
            regrets = regret_diagnostics(model, p1, profile, ev, settings.regret_tol, settings.support_tol)
            br, rr = best_response(model, profile, ev, temperature, settings.response_tie_tol)
            residual = max(float(np.max(np.abs(br[0] - profile.sigma_e))),
                           float(np.max(np.abs(br[1] - profile.sigma_h))),
                           float(np.max(np.abs(rr - profile.retain))))
            if temperature == 0 and regrets['sample_checks_pass']:
                train_pass = True
                break
            profile.sigma_e = (1 - damping) * profile.sigma_e + damping * br[0]
            profile.sigma_h = (1 - damping) * profile.sigma_h + damping * br[1]
            profile.retain = (1 - damping) * profile.retain + damping * rr
            iteration += 1
        row = dict(temperature=temperature, iterations=iteration, response_residual=residual,
                   pre_update_max_regret=regrets['max_regret'], train_tolerance_reached=train_pass)
        history.append(row)
        if progress: progress(row)
    # Recompute at the RETURNED profile, including when budget expires on update.
    final_ev = evaluator.evaluate(m, p1, p2, profile, settings.train_counts, settings.seed)
    final_regrets = regret_diagnostics(model, p1, profile, final_ev, settings.regret_tol, settings.support_tol)
    complementarity = complementarity_diagnostics(model, p1, profile, final_ev)
    train_pass = final_regrets['sample_checks_pass']
    audits = [evaluator.audit(m, p1, p2, profile, settings.audit_counts, settings.seed + 1000003 + j * 104729)
              for j in range(settings.audit_replicates)]
    passed = train_pass and all(a['bounded_checks_pass'] for a in audits)
    status = ('numerical_checks_passed' if passed else
              'insufficient_evidence' if train_pass else 'not_converged')
    profile.meta = dict(early_share=float(np.sum(model.type_mass * profile.sigma_e)),
        hidden_share=float(np.sum(model.type_mass * profile.sigma_h)),
        leave_share=float(np.sum(model.type_mass * (1 - profile.sigma_e - profile.sigma_h))),
        max_regret=max(a['regrets']['max_regret'] for a in audits), iterations=float(iteration))
    return profile, dict(m=m, p1=p1, p2=p2, init=init, settings=asdict(settings),
        status=status, training_regret_check_pass=bool(train_pass), training_regrets=final_regrets,
        complementarity=complementarity,
        numerical_checks_passed=bool(passed), audits=audits, iteration_history=history,
        wpbe_certified=False, continuous_type_convergence_verified=False,
        equilibrium_uniqueness_proved=False, external_price_optimized=False,
        v12_candidates_imported=False)


def price_grid(step, pbar=1.):
    if not math.isfinite(step) or step <= 0 or step > pbar:
        raise ValueError('Require 0 < step <= pbar')
    n = round(pbar / step)
    if n > 10000 or not math.isclose(n * step, pbar, abs_tol=1e-10):
        raise ValueError('step must divide pbar exactly (maximum 10000 intervals)')
    return [round(i * step, 12) for i in range(n + 1)]


def grid_summary(rows, expected_menus):
    keys = [(r['p1'], r['p2']) for r in rows]
    if len(set(keys)) != len(keys) or not rows:
        raise ValueError('Nonempty, unique menu records required')
    if len({r['m'] for r in rows}) != 1:
        raise ValueError('One thickness per grid summary')
    full = set(keys) == set(expected_menus)
    unresolved = [i for i, r in enumerate(rows) if not r['numerical_checks_passed']]
    if any(not math.isfinite(r['selection_completion']) for r in rows):
        raise ValueError('Nonfinite score')
    # Do not discard unresolved candidates before ranking.
    leader = max(range(len(rows)), key=lambda i: rows[i]['selection_completion'])
    flat = [i for i, r in enumerate(rows) if r['p1'] == r['p2']]
    flat_leader = max(flat, key=lambda i: rows[i]['selection_completion']) if flat else None
    # Family-wise sampling intervals cover the finite menu scores, not the
    # unknown equilibrium or discretization errors. CRN correlation is allowed.
    have_n = all(isinstance(r.get('selection_markets'), int) and r['selection_markets'] > 0 for r in rows)
    intervals = None; ranking_resolved = False; value_gap_upper = None
    if have_n:
        radius = [math.sqrt(math.log(2*len(rows)/.05)/(2*r['selection_markets'])) for r in rows]
        intervals = [[max(0., r['selection_completion']-e), min(1., r['selection_completion']+e)]
                     for r, e in zip(rows, radius)]
        value_gap_upper = max(0., max(v[1] for v in intervals)-intervals[leader][0])
        ranking_resolved = all(intervals[leader][0] > intervals[i][1] for i in range(len(rows)) if i != leader)
    return dict(full_requested_grid_evaluated=full, unresolved_indices=unresolved,
        raw_rescue_leader_index=leader, raw_flat_leader_index=flat_leader,
        numerical_grid_comparison_ready=bool(full and not unresolved and flat),
        continuous_price_global_optimum_proved=False, wpbe_certified=False,
        fixed_profile_selection_intervals_95=intervals,
        fixed_profile_grid_value_gap_upper_95=value_gap_upper,
        sampling_rank_separated=bool(ranking_resolved),
        grid_optimality_certified=False,
        selection_rule='Maximum independent selection-sample completion over ALL grid menus; lexicographic ties.',
        equilibrium_selection='One common cold-start rule for every menu; no uniqueness claim.',
        raw_leader_is_not_necessarily_an_equilibrium=bool(unresolved))

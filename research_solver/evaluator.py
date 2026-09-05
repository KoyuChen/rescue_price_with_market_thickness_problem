"""Joint-payoff audit with explicit, narrowly certified off-path beliefs.

The finite-sample bound is Maurer & Pontil (2009), Theorem 4:
https://arxiv.org/abs/0907.3740 . Bounds concern a FROZEN profile and the
Poisson count law, not continuous types, floating point, or quadrature.
"""
from itertools import product
import math
import numpy as np

from rescue_solver.solver import ValueIntegratedEvaluator
from rescue_solver.diagnostics import regret_diagnostics


def offpath_certificates(model, p1, q_values, new_lam):
    """Sufficient global proofs, NEVER an inference from no sampled events.

    If no hidden driver can appear, discounted old offers cannot improve
    immediate acceptance. Otherwise even a perfect-fit hidden offer cannot
    beat the tagged immediate offer when q >= beta*(p1+detour). Use a small
    conservative margin for this second sufficient condition.
    """
    no_hidden = np.asarray(new_lam).sum(axis=1) == 0
    dominated = np.asarray(q_values)[None, :] >= (
        model.par.beta * (p1 + model.par.ell * (1-model.s))[:, None] + 1e-12)
    return dominated | no_hidden[None, :]


def bernstein_radius(variance, width, n, log_factor):
    if n < 2:
        raise ValueError('At least two independent count draws required')
    return np.sqrt(2*np.maximum(variance, 0)*log_factor/n) + 7*width*log_factor/(3*(n-1))


class JointPayoffEvaluator(ValueIntegratedEvaluator):
    """Features per route: immediate win, Q old events, Q old wins, Q new wins.

    Features are integrated over rider values, conditional on an IID Poisson
    rival count vector. Duplicate vectors retain their original multiplicity.
    Covariances, not independent marginal error bars, drive payoff bounds.
    """
    collect_moments = False

    def _weighted_rates(self, counts, weights, p1, profile, old_r, new_lam):
        model = self.model; Q = len(profile.q_values); N = len(counts)
        features = np.zeros((N, model.S, 1+3*Q))
        base, mid = self.value_intervals(counts, p1, profile.q_values, old_r, new_lam)
        prob_base = weights @ base[:, 1:, :].sum(axis=-1)
        completion = float(weights @ base[:, 0, :].sum(axis=-1))
        for iq, q in enumerate(profile.q_values):
            go, gn = p1+model.beta_detour, q+model.beta_detour
            accept_old = model.par.beta*mid[:, None]-go > 1e-12
            accept_new = model.par.beta*mid[:, None]-gn > 1e-12
            log_none = counts @ (np.log(np.clip(1-old_r[iq], 1e-14, 1))*accept_old).T
            log_none -= accept_new @ new_lam[iq]
            completion += float(weights @ np.sum(base[:, iq+1, :]*(-np.expm1(log_none)), axis=1))
            for s in range(model.S):
                selection = model._tag_selection_probability(counts, np.ones(N), p1,
                    float(q), float(model.s[s]), 'new', old_r[iq], new_lam[iq])
                features[:, s, 1+2*Q+iq] = selection*(base[:, iq+1, :] @ accept_new[:, s])
        for s in range(model.S):
            tagged = counts.copy(); tagged[:, s] += 1
            lengths, mid = self.value_intervals(tagged, p1, profile.q_values, old_r, new_lam)
            share = np.where(counts[:, s+1:].sum(axis=1)>0, 0., 1/(1+counts[:, s]))
            features[:, s, 0] = lengths[:, 0, :].sum(axis=1)*share
            for iq, q in enumerate(profile.q_values):
                features[:, s, 1+iq] = lengths[:, iq+1, :].sum(axis=1)
                selection = model._tag_selection_probability(counts, np.ones(N), p1,
                    float(q), float(model.s[s]), 'old', old_r[iq], new_lam[iq])
                acceptable = model.par.beta*mid-(p1+model.beta_detour[s]) > 1e-12
                features[:, s, 1+Q+iq] = selection*(lengths[:, iq+1, :] @ acceptable)
        certified = offpath_certificates(model, p1, profile.q_values, new_lam)
        for iq in range(Q):
            mask = certified[:, iq]
            if np.any(features[:, mask, 1+iq] > 1e-10):
                raise ArithmeticError('Off-path proof disagrees with rider integration')
            features[:, mask, 1+iq] = 0
            features[:, mask, 1+Q+iq] = 0
        mean = np.einsum('n,nsf->sf', weights, features)
        if self.collect_moments:
            self.first += mean
            self.second += np.einsum('n,nsf,nsg->sfg', weights, features, features)
        return dict(p_immediate=mean[:, 0], prob_old=mean[:, 1:1+Q],
                    num_old=mean[:, 1+Q:1+2*Q], num_new=mean[:, 1+2*Q:],
                    prob_base=prob_base, completion=completion)

    def evaluate(self, m, p1, p2, profile, n, seed):
        ev = super().evaluate(m, p1, p2, profile, n, seed)
        known_offpath = offpath_certificates(self.model, p1, profile.q_values, ev['lambda_new'])
        observed = ev['prob_q_early'] > 0
        unknown = ~observed & ~known_offpath
        # For proved off-path histories choose belief v=0, no other drivers.
        # No terminal sale is acceptable; retaining loses omega_old. This is
        # an explicit assessment choice, NOT a Bayesian posterior estimate.
        pi = np.zeros_like(ev['pi_old'])
        # Joint rates retained by the parent are recovered without posterior placeholders.
        pi[observed] = ev['pi_old'][observed]
        ev['pi_old'] = pi
        ev['retain_advantage'] = pi.T[:, None, :]*(self.model.par.delta*p1-self.model.a)-self.model.par.omega_old
        # Unknown history: hold retention fixed while solving and BLOCK audit.
        ev['retain_advantage'] = np.where(unknown.T[:, None, :], 0., ev['retain_advantage'])
        ev['offpath_certified'] = known_offpath
        ev['unknown_old_history'] = unknown
        feasible_routes = np.any(self.model.a <= p1+1e-12, axis=0)
        ev['unknown_feasible_history_count'] = int(np.sum(unknown & feasible_routes[:, None]))
        # Do not export a fake point probability for unknown histories.
        ev['pi_old_report'] = [[None if unknown[s, q] else float(pi[s, q])
                               for q in range(len(profile.q_values))] for s in range(self.model.S)]
        return ev

    def audit(self, m, p1, p2, profile, n, seed):
        if self.settings.mode != 'sample':
            raise ValueError('Joint-payoff Bernstein audit requires IID sample mode')
        model = self.model; Q = len(profile.q_values); F = 1+3*Q
        self.first = np.zeros((model.S, F)); self.second = np.zeros((model.S, F, F))
        self.collect_moments = True
        try:
            ev = self.evaluate(m, p1, p2, profile, n, seed)
        finally:
            self.collect_moments = False
        covariance = (self.second-np.einsum('sf,sg->sfg', self.first, self.first))*n/(n-1)
        certified = ev['offpath_certified']
        feature_width = np.ones((model.S, F))
        feature_width[:, 1:1+Q] = ~certified
        feature_width[:, 1+Q:1+2*Q] = ~certified
        # Includes full-plan, three supported-action comparisons, both signs
        # of each retention advantage, and denominator lower bounds.
        plan_count = 2**Q+2
        family_size = model.C*model.S*(4*plan_count+2*Q)+model.S*Q
        log_factor = math.log(2*family_size/self.settings.alpha)

        def bounds(coeff, constant=0.):
            mean = np.einsum('csf,sf->cs', coeff, self.first)+constant
            variance = np.einsum('csf,sfg,csg->cs', coeff, covariance, coeff)
            width = np.sum(np.abs(coeff)*feature_width, axis=-1)
            radius = bernstein_radius(variance, width, n, log_factor)
            # Deterministic support enclosure, valid without estimating variance.
            lower = np.sum(np.minimum(coeff, 0)*feature_width, axis=-1)+constant
            upper = np.sum(np.maximum(coeff, 0)*feature_width, axis=-1)+constant
            return mean, np.maximum(mean-radius, lower), np.minimum(mean+radius, upper)

        def early_coeff(retain):
            coeff = np.zeros((model.C, model.S, F))
            coeff[:, :, 0] = p1-model.a
            coeff[:, :, 1:1+Q] = -model.par.omega_old*np.moveaxis(retain, 0, -1)
            coeff[:, :, 1+Q:1+2*Q] = (model.par.delta*p1-model.a)[:, :, None]*np.moveaxis(retain, 0, -1)
            return coeff

        zero = np.zeros((model.C, model.S, F))
        hc = zero.copy()
        hc[:, :, 1+2*Q:] = np.maximum(profile.q_values-model.a[:, :, None], 0)
        ec = early_coeff(profile.retain)
        incumbent = profile.sigma_e[:, :, None]*ec+profile.sigma_h[:, :, None]*hc
        incumbent_constant = -profile.sigma_h*model.par.omega_hidden
        feasible = model.a <= p1+1e-12
        plans = [(zero, 0., np.ones_like(feasible)), (hc, -model.par.omega_hidden, np.ones_like(feasible))]
        for r in product((0., 1.), repeat=Q):
            rr = np.broadcast_to(np.asarray(r)[:, None, None], profile.retain.shape)
            plans.append((early_coeff(rr), 0., feasible))
        actual_actions = [(ec, 0., profile.sigma_e), (hc, -model.par.omega_hidden, profile.sigma_h),
                          (zero, 0., 1-profile.sigma_e-profile.sigma_h)]
        full_upper = support_upper = 0.
        for coeff, const, allowed in plans:
            _, _, upper = bounds(coeff-incumbent, const-incumbent_constant)
            full_upper = max(full_upper, float(np.max(np.where(allowed, upper, 0))))
            for ac, av, probability in actual_actions:
                _, _, upper = bounds(coeff-ac, const-av)
                support_upper = max(support_upper, float(np.max(np.where(allowed & (probability>1e-3), upper, 0))))
        retention_upper = retention_support_upper = 0.
        unresolved = []
        for iq in range(Q):
            dc = zero.copy(); dc[:, :, 1+iq] = 1
            _, denominator_low, _ = bounds(dc)
            jc = zero.copy(); jc[:, :, 1+iq] = -model.par.omega_old
            jc[:, :, 1+Q+iq] = model.par.delta*p1-model.a
            _, jl, ju = bounds(jc)
            r = profile.retain[iq]
            numerator_upper = np.maximum((1-r)*np.maximum(ju, 0), r*np.maximum(-jl, 0))
            support_num = np.maximum(np.where(r<1-1e-3, np.maximum(ju, 0), 0),
                                     np.where(r>1e-3, np.maximum(-jl, 0), 0))
            off = np.broadcast_to(certified[:, iq], feasible.shape)
            resolved = denominator_low > 0
            # For zero numerator the sign of the deviation is already known;
            # its regret is zero regardless of a positive denominator's size.
            unknown = feasible & ~off & ~resolved & ((numerator_upper>0) | (support_num>0))
            unresolved.extend([dict(q=float(profile.q_values[iq]), cost_index=int(c), route_index=int(s),
                                    event_mean=float(ev['prob_q_early'][s, iq])) for c, s in np.argwhere(unknown)])
            ret = np.divide(numerator_upper, denominator_low, out=np.zeros_like(r), where=resolved)
            sup = np.divide(support_num, denominator_low, out=np.zeros_like(r), where=resolved)
            ret = np.where(off, r*model.par.omega_old, ret)
            sup = np.where(off & (r>1e-3), model.par.omega_old, np.where(off, 0., sup))
            retention_upper = max(retention_upper, float(np.max(np.where(feasible, ret, 0))))
            retention_support_upper = max(retention_support_upper, float(np.max(np.where(feasible, sup, 0))))
        diagnostic = regret_diagnostics(model, p1, profile, ev, self.settings.regret_tol, self.settings.support_tol)
        passed = (not unresolved and max(full_upper, retention_upper)<=self.settings.regret_tol
                  and max(support_upper, retention_support_upper)<=self.settings.support_tol)
        return dict(seed=seed, count_draws=n, count_states=ev['count_states'], alpha=self.settings.alpha,
            family_size=family_size, method='direct_payoff_empirical_Bernstein',
            full_plan_regret_upper=full_upper, initial_support_gap_upper=support_upper,
            retention_regret_upper=retention_upper, retention_support_gap_upper=retention_support_upper,
            max_regret_upper=None if unresolved else max(full_upper, retention_upper),
            unresolved_histories=unresolved, bounded_checks_pass=bool(passed), regrets=diagnostic,
            offpath_certified=certified.tolist(), old_history_probability=ev['prob_q_early'].tolist(),
            old_win_probability=ev['pi_old_report'], completion=ev['completion'],
            offpath_belief='At structurally impossible old histories: v=0 and no rivals; retain=0 is optimal.',
            wpbe_certified=False, scope='Fixed finite-support profile; count-law uncertainty only.')

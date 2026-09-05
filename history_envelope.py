"""Sufficient continuation-history exclusion over ALL early count vectors.

This supplements, rather than weakens, the original finite-support audit.
When high-price retention is supported on only the tagged route s, removing
all other early routes leaves high-price utility unchanged and can only
reduce immediate and low-price utility. It suffices to consider k>=1 copies
of s. Check k=1,...,K-1 individually. For every k>=K bound high-price utility
by certain retention of s, and bound low-price utility below by K copies.
Piecewise-linear envelopes are checked at hinges AND competitor crossings.
No count/probability tail is discarded. Floating point remains a limitation.
"""
import numpy as np
from research_solver.certified import CertifiedPayoffEvaluator


def envelope_check(model, p1, q_values, old, new, route, low, high, k,
                   certain_high=False, safety_margin=1e-10):
    beta = model.par.beta
    go = np.round(p1 + model.beta_detour, 12)
    gl = np.round(q_values[low] + model.beta_detour, 12)
    gh = np.round(q_values[high] + model.beta_detour, 12)
    immediate_threshold = p1 + model.par.ell * (1-model.s[route])
    edges = np.unique(np.clip(np.r_[0., 1., immediate_threshold,
                                    go/beta, gl/beta, gh/beta], 0., 1.))

    def utilities(values):
        counts = np.zeros((len(values), model.S), dtype=int)
        counts[:, route] = k
        lower = model._expected_terminal_value(counts, values, p1,
                    float(q_values[low]), old[low], new[low])
        immediate = np.maximum(values-immediate_threshold, 0.)
        if certain_high:
            counts[:, route] = 1
            retention = np.zeros(model.S); retention[route] = 1.
        else:
            retention = old[high]
        upper = model._expected_terminal_value(counts, values, p1,
                    float(q_values[high]), retention, new[high])
        return immediate, lower, upper

    immediate, lower, _ = utilities(edges)
    difference = immediate-lower
    crossings = []
    for j in range(len(edges)-1):
        if difference[j]*difference[j+1] < 0:
            crossings.append(edges[j]-difference[j]*(edges[j+1]-edges[j])/
                             (difference[j+1]-difference[j]))
    points = np.unique(np.r_[edges, crossings])
    immediate, lower, upper = utilities(points)
    gap = np.maximum(immediate, lower)-upper
    active = upper > 1e-12
    # At inactive vertices both alternatives are nonnegative. Strict margin
    # at active vertices avoids certifying near-equality from rounding.
    passed = bool(np.all(gap >= 0.) and np.all(gap[active] > safety_margin))
    return dict(passed=passed, k=int(k), certain_high=bool(certain_high),
                minimum_active_margin=float(gap[active].min()) if active.any() else None,
                points=len(points), competitor_crossings=len(crossings))


def count_envelope_certificates(model, p1, q_values, old, new, max_k=16):
    proof = np.zeros((model.S, len(q_values)), dtype=bool)
    records = []
    for high in range(1, len(q_values)):
        for s in range(model.S):
            # Exact support test: arbitrarily small positive retention counts.
            if np.any(np.delete(np.asarray(old[high]), s) > 0.):
                continue
            for low in range(high):
                finite = []
                for k in range(1, max_k+1):
                    tail = envelope_check(model, p1, q_values, old, new,
                                          s, low, high, k, True)
                    if tail['passed']:
                        proof[s, high] = True
                        records.append(dict(route_index=s, q=float(q_values[high]),
                            comparator_q=float(q_values[low]), tail_from_k=k,
                            finite_checks=finite, tail_check=tail))
                        break
                    point = envelope_check(model, p1, q_values, old, new,
                                           s, low, high, k)
                    if not point['passed']:
                        break
                    finite.append(point)
                if proof[s, high]:
                    break
    return proof, records


class EnvelopeHistoryEvaluator(CertifiedPayoffEvaluator):
    def evaluate(self, m, p1, p2, profile, n, seed):
        ev = super().evaluate(m, p1, p2, profile, n, seed)
        proof, records = count_envelope_certificates(self.model, p1,
            profile.q_values, ev['old_r'], ev['lambda_new'])
        if np.any(ev['prob_q_early'][proof] > 1e-10):
            raise ArithmeticError('Count-envelope exclusion contradicts rider integration')
        ev['offpath_certified'] |= proof
        ev['unknown_old_history'] &= ~proof
        ev['pi_old'][proof] = 0.
        ev['retain_advantage'] = np.where(proof.T[:, None, :],
            -self.model.par.omega_old, ev['retain_advantage'])
        feasible = np.any(self.model.a <= p1+1e-12, axis=0)
        ev['unknown_feasible_history_count'] = int(np.sum(
            ev['unknown_old_history'] & feasible[:, None]))
        for s, iq in np.argwhere(proof):
            ev['pi_old_report'][s][iq] = 0.
        ev['count_envelope_certificates'] = records
        self.latest_envelope_certificates = records
        return ev

    def audit(self, *args, **kwargs):
        result = super().audit(*args, **kwargs)
        result['count_envelope_certificates'] = self.latest_envelope_certificates
        result['method'] += '_and_all_counts_continuation_envelopes'
        result['floating_point_envelope_verified_with_margin'] = True
        result['exact_arithmetic_certificate'] = False
        return result

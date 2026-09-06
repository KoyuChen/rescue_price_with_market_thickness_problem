"""Additional all-count history certificate; no change to model or beliefs.

If high-price old retention is EXACTLY zero on every route, its continuation
value is independent of early counts. For a tagged early driver on route s,
every additional early driver weakly improves immediate acceptance and the
lower-price continuation. Thus strict domination with ONLY the tag implies
domination for EVERY rival count vector. No count tail is discarded, and no
small positive retention or intensity is rounded to zero.
"""
import numpy as np
from accelerated_evaluator import CachedEnvelopeEvaluator
from history_envelope import envelope_check


def zero_retention_certificates(model, p1, q_values, old, new):
    proof = np.zeros((model.S, len(q_values)), dtype=bool)
    records = []
    for high in range(1, len(q_values)):
        if not np.all(np.asarray(old[high]) == 0.):
            continue
        for s in range(model.S):
            for low in range(high):
                check = envelope_check(model, p1, q_values, old, new,
                                       s, low, high, 1)
                if check['passed']:
                    proof[s, high] = True
                    records.append(dict(route_index=s, q=float(q_values[high]),
                        comparator_q=float(q_values[low]),
                        high_old_retention_exactly_zero=True,
                        all_rival_counts_covered=True, single_tag_check=check))
                    break
    return proof, records


class ZeroRetentionEnvelopeEvaluator(CachedEnvelopeEvaluator):
    def evaluate(self, m, p1, p2, profile, n, seed):
        ev = super().evaluate(m, p1, p2, profile, n, seed)
        proof, records = zero_retention_certificates(self.model, p1,
            profile.q_values, ev['old_r'], ev['lambda_new'])
        if np.any(ev['prob_q_early'][proof] > 1e-10):
            raise ArithmeticError('Zero-retention proof contradicts rider integration')
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
        ev['zero_retention_envelope_certificates'] = records
        self.latest_zero_retention_certificates = records
        return ev

    def audit(self, *args, **kwargs):
        result = super().audit(*args, **kwargs)
        result['zero_retention_envelope_certificates'] = self.latest_zero_retention_certificates
        result['method'] += '_and_zero_old_retention_all_count_envelope'
        return result

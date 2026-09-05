"""Economic primitives and independent evaluation; v1.1.1 model, no legacy optimizer."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple
import math
import numpy as np

OBJECTIVE_NAME = "completion_probability"
OBJECTIVE_FORMULA = "E[1{match}]"

@dataclass(frozen=True)
class ModelParams:
    beta: float = 0.96
    delta: float = 0.90
    ell: float = 0.35
    kappa: float = 0.18
    omega_old: float = 0.004
    omega_hidden: float = 0.005
    p_bar: float = 1.0

    # One-dimensional OD generator. The rider route is normalized to [0,1].
    driver_origin_low: float = -0.75
    driver_origin_high: float = 0.75
    driver_length_low: float = 0.45
    driver_length_high: float = 1.75
    same_direction_probability: float = 0.82
    route_draws: int = 800_000

    # Tail-adaptive finite-type approximation. Cost is uniform, so these are
    # probability edges and interval means are exact.
    cost_probability_edges: Tuple[float, ...] = (
        0.0, 0.003, 0.008, 0.016, 0.030, 0.052, 0.082, 0.125,
        0.18, 0.25, 0.34, 0.45, 0.58, 0.72, 0.86, 1.0,
    )
    # Conditional quantile edges for positive route overlaps. The top tail is
    # deliberately fine because thick-market behavior is driven by s close to 1.
    route_positive_quantile_edges: Tuple[float, ...] = (
        0.0, 0.08, 0.16, 0.24, 0.32, 0.40, 0.48, 0.56, 0.64,
        0.72, 0.80, 0.86, 0.90, 0.93, 0.95, 0.97, 0.98,
        0.99, 0.995, 0.998, 0.9995, 1.0,
    )
    seed: int = 20260904

    def __post_init__(self):
        for name in ('beta', 'delta'):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (float, int)) or not 0 < value <= 1:
                raise ValueError(f'{name} must lie in (0,1]')
        for name in ('ell', 'kappa', 'omega_old', 'omega_hidden', 'p_bar'):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
                raise ValueError(f'{name} must be finite and nonnegative')
        if self.p_bar <= 0:
            raise ValueError('p_bar must be positive')
        for lo, hi in ((self.driver_origin_low, self.driver_origin_high),
                       (self.driver_length_low, self.driver_length_high)):
            if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi):
                raise ValueError('Invalid route interval')
        if self.driver_length_low <= 0:
            raise ValueError('Route lengths must be positive')
        if not 0 <= self.same_direction_probability <= 1:
            raise ValueError('Invalid direction probability')
        for name in ('route_draws', 'seed'):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < (1 if name == 'route_draws' else 0):
                raise ValueError(f'Invalid {name}')
        for name in ('cost_probability_edges', 'route_positive_quantile_edges'):
            edges = np.asarray(getattr(self, name), float)
            if edges.ndim != 1 or len(edges) < 2 or not np.all(np.isfinite(edges)) or edges[0] != 0 or edges[-1] != 1 or not np.all(np.diff(edges) > 0):
                raise ValueError(f'{name} must strictly increase from 0 to 1')


def draw_routes(params, n, seed):
    """Independent 1D OD draws, with direction and realized overlap retained."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer')
    rng = np.random.default_rng(seed)
    origin = rng.uniform(params.driver_origin_low, params.driver_origin_high, n)
    length = rng.uniform(params.driver_length_low, params.driver_length_high, n)
    same = rng.random(n) < params.same_direction_probability
    common = np.maximum(0., np.minimum(1., origin + length) - np.maximum(0., origin))
    overlap = np.where(same, 2 * common / (1 + length), 0.)
    return dict(origin=origin, length=length, same_direction=same, overlap=overlap)


@dataclass
class Profile:
    sigma_e: np.ndarray
    sigma_h: np.ndarray
    retain: np.ndarray
    q_values: np.ndarray
    meta: Dict[str, float]


# ---------------------------------------------------------------------------
# Core finite-type equilibrium solver
# ---------------------------------------------------------------------------


class RescueModel:
    def __init__(self, params: ModelParams = ModelParams()):
        self.par = params
        self.c, self.fc = self._make_cost_support()
        self.s, self.fs = self._make_route_support()
        self.C = len(self.c)
        self.S = len(self.s)
        self.type_mass = self.fc[:, None] * self.fs[None, :]
        self.a = self.c[:, None] + self.par.kappa * (1.0 - self.s[None, :])
        self.beta_detour = self.par.beta * self.par.ell * (1.0 - self.s)

        # Exact expected tie share against binomial/Poisson rivals.
        x, w = np.polynomial.legendre.leggauss(10)
        self.tie_t = (x + 1.0) / 2.0
        self.tie_w = w / 2.0

    def _make_cost_support(self) -> Tuple[np.ndarray, np.ndarray]:
        edges = np.asarray(self.par.cost_probability_edges, dtype=float)
        if not (edges[0] == 0.0 and edges[-1] == 1.0 and np.all(np.diff(edges) > 0)):
            raise ValueError("cost_probability_edges must strictly increase from 0 to 1")
        probs = np.diff(edges)
        means = 0.5 * (edges[:-1] + edges[1:])
        return means, probs

    def _make_route_support(self) -> Tuple[np.ndarray, np.ndarray]:
        p = self.par
        n = p.route_draws
        overlap = draw_routes(p, n, p.seed)['overlap']

        zero = overlap <= 1.0e-14
        positive = overlap[~zero]
        if len(positive) == 0:
            return np.array([0.]), np.array([1.])
        qedges = np.asarray(p.route_positive_quantile_edges, dtype=float)
        if not (qedges[0] == 0.0 and qedges[-1] == 1.0 and np.all(np.diff(qedges) > 0)):
            raise ValueError("route_positive_quantile_edges must increase from 0 to 1")
        cuts = np.quantile(positive, qedges)

        s_values: List[float] = [0.0]
        probs: List[float] = [float(zero.mean())]
        for j in range(len(qedges) - 1):
            if j < len(qedges) - 2:
                mask = (positive >= cuts[j]) & (positive < cuts[j + 1])
            else:
                mask = (positive >= cuts[j]) & (positive <= cuts[j + 1])
            if not np.any(mask):
                continue
            s_values.append(float(np.mean(positive[mask])))
            probs.append(float(np.sum(mask) / n))
        probs_arr = np.asarray(probs, dtype=float)
        probs_arr /= probs_arr.sum()
        return np.asarray(s_values, dtype=float), probs_arr

    @staticmethod
    def _softmax(values: np.ndarray, temperature: float) -> np.ndarray:
        z = values / max(temperature, 1.0e-10)
        z -= np.max(z, axis=0, keepdims=True)
        e = np.exp(np.clip(z, -700.0, 50.0))
        return e / np.sum(e, axis=0, keepdims=True)

    @staticmethod
    def _sigmoid(x: np.ndarray, temperature: float) -> np.ndarray:
        z = np.clip(x / max(temperature, 1.0e-10), -60.0, 60.0)
        return 1.0 / (1.0 + np.exp(-z))

    def _belief_objects(
        self,
        m: float,
        p1: float,
        q_values: np.ndarray,
        sigma_e: np.ndarray,
        sigma_h: np.ndarray,
        retain: np.ndarray,
    ) -> Tuple[np.ndarray, List[np.ndarray], List[np.ndarray]]:
        del p1  # p1 is retained in the signature for readability.
        early_mass_s = np.sum(self.fc[:, None] * sigma_e, axis=0)
        lambda_early = m * self.fs * early_mass_s

        old_retention: List[np.ndarray] = []
        lambda_new: List[np.ndarray] = []
        for iq, q in enumerate(q_values):
            retained_mass_s = np.sum(
                self.fc[:, None] * sigma_e * retain[iq], axis=0
            )
            r_s = np.divide(
                retained_mass_s,
                early_mass_s,
                out=np.zeros_like(retained_mass_s),
                where=early_mass_s > 1.0e-13,
            )
            old_retention.append(np.clip(r_s, 0.0, 1.0 - 1.0e-13))

            feasible_new = (q - self.a) >= -1.0e-12
            new_mass_s = np.sum(
                self.fc[:, None] * sigma_h * feasible_new, axis=0
            )
            lambda_new.append(m * self.fs * new_mass_s)
        return lambda_early, old_retention, lambda_new

    def _expected_terminal_value(
        self,
        counts: np.ndarray,
        v: np.ndarray,
        p1: float,
        q: float,
        old_r: np.ndarray,
        lambda_new: np.ndarray,
    ) -> np.ndarray:
        g_old = p1 + self.beta_detour
        g_new = q + self.beta_detour
        levels = np.unique(np.round(np.concatenate([g_old, g_new]), 12))
        levels.sort()
        log_one_minus_r = np.log(np.clip(1.0 - old_r, 1.0e-14, 1.0))

        cdf = np.empty((counts.shape[0], len(levels)), dtype=float)
        for j, level in enumerate(levels):
            old_mask = g_old <= level + 1.0e-11
            new_mask = g_new <= level + 1.0e-11
            log_none = counts[:, old_mask] @ log_one_minus_r[old_mask]
            log_none -= float(np.sum(lambda_new[new_mask]))
            cdf[:, j] = 1.0 - np.exp(np.minimum(log_none, 0.0))
        mass = np.diff(np.column_stack([np.zeros(counts.shape[0]), cdf]), axis=1)
        utility = np.maximum(self.par.beta * v[:, None] - levels[None, :], 0.0)
        return np.sum(mass * utility, axis=1)

    def _rider_action(
        self,
        counts: np.ndarray,
        v: np.ndarray,
        p1: float,
        q_values: np.ndarray,
        old_r: Sequence[np.ndarray],
        lambda_new: Sequence[np.ndarray],
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return -1 exit, 0 accept, and 1+iq for continuation at q_i.

        Positive-payoff ties are resolved in favor of immediate acceptance and
        then the lower continuation price. A zero-payoff tie is resolved by exit.
        """
        has_early = np.sum(counts, axis=1) > 0
        reversed_positive = counts[:, ::-1] > 0
        index_from_top = np.argmax(reversed_positive, axis=1)
        best_s_index = self.S - 1 - index_from_top
        best_s = self.s[best_s_index]
        immediate = np.where(
            has_early,
            np.maximum(v - self.par.ell * (1.0 - best_s) - p1, 0.0),
            0.0,
        )
        continuation = np.column_stack([
            self._expected_terminal_value(
                counts, v, p1, float(q), old_r[iq], lambda_new[iq]
            )
            for iq, q in enumerate(q_values)
        ])
        values = np.column_stack([immediate, continuation])
        best = np.max(values, axis=1)
        action = np.argmax(values, axis=1)
        return np.where(best > 1.0e-12, action, -1), immediate, continuation

    def _tie_factor(
        self,
        counts: np.ndarray,
        equal_old_mask: np.ndarray,
        old_r: np.ndarray,
        lambda_equal_new: float,
    ) -> np.ndarray:
        if not np.any(equal_old_mask) and lambda_equal_new <= 1.0e-14:
            return np.ones(counts.shape[0])
        out = np.zeros(counts.shape[0])
        n_equal = counts[:, equal_old_mask]
        r_equal = old_r[equal_old_mask]
        for t, w in zip(self.tie_t, self.tie_w):
            log_g = np.full(counts.shape[0], lambda_equal_new * (t - 1.0))
            if n_equal.shape[1] > 0:
                base = np.clip(1.0 - r_equal + r_equal * t, 1.0e-14, 1.0)
                log_g += n_equal @ np.log(base)
            out += w * np.exp(log_g)
        return out

    def _tag_selection_probability(
        self,
        counts: np.ndarray,
        v: np.ndarray,
        p1: float,
        q: float,
        s_tag: float,
        cohort: str,
        old_r: np.ndarray,
        lambda_new: np.ndarray,
    ) -> np.ndarray:
        g_old = p1 + self.beta_detour
        g_new = q + self.beta_detour
        g_tag = (p1 if cohort == "old" else q) + self.par.beta * self.par.ell * (1.0 - s_tag)
        tol = 1.0e-10
        lower_old = g_old < g_tag - tol
        lower_new = g_new < g_tag - tol
        equal_old = np.abs(g_old - g_tag) <= tol
        equal_new = np.abs(g_new - g_tag) <= tol
        log_one_minus_r = np.log(np.clip(1.0 - old_r, 1.0e-14, 1.0))
        if np.any(lower_old):
            log_no_lower_old = counts[:, lower_old] @ log_one_minus_r[lower_old]
        else:
            log_no_lower_old = np.zeros(counts.shape[0])
        lambda_lower_new = float(np.sum(lambda_new[lower_new]))
        no_better = np.exp(np.minimum(log_no_lower_old - lambda_lower_new, 0.0))
        tie_share = self._tie_factor(
            counts, equal_old, old_r, float(np.sum(lambda_new[equal_new]))
        )
        acceptable = (self.par.beta * v - g_tag) > 1.0e-12
        return acceptable.astype(float) * no_better * tie_share

    def _evaluate_profile(
        self,
        m: float,
        p1: float,
        p2: float,
        sigma_e: np.ndarray,
        sigma_h: np.ndarray,
        retain: np.ndarray,
        n_markets: int,
        seed: int,
    ) -> Dict[str, np.ndarray]:
        q_values = np.unique(np.round(np.array([p1, p2], dtype=float), 12))
        Q = len(q_values)
        lambda_early, old_r, lambda_new = self._belief_objects(
            m, p1, q_values, sigma_e, sigma_h, retain[:Q]
        )
        rng = np.random.default_rng(seed)
        counts = rng.poisson(lambda_early[None, :], size=(n_markets, self.S))
        v = rng.random(n_markets)

        base_action, _, _ = self._rider_action(
            counts, v, p1, q_values, old_r, lambda_new
        )
        prob_q_base = np.array([
            float(np.mean(base_action == (1 + iq))) for iq in range(Q)
        ])

        pi_new = np.zeros((self.S, Q))
        for iq, q in enumerate(q_values):
            event = base_action == (1 + iq)
            if np.any(event):
                for is_, s in enumerate(self.s):
                    selection = self._tag_selection_probability(
                        counts, v, p1, float(q), float(s), "new",
                        old_r[iq], lambda_new[iq],
                    )
                    pi_new[is_, iq] = float(np.mean(selection[event]))

        p_immediate = np.zeros(self.S)
        prob_q_early = np.zeros((self.S, Q))
        pi_old = np.zeros((self.S, Q))
        for is_, s in enumerate(self.s):
            counts_with_tag = counts.copy()
            counts_with_tag[:, is_] += 1
            tagged_action, _, _ = self._rider_action(
                counts_with_tag, v, p1, q_values, old_r, lambda_new
            )
            if is_ + 1 < self.S:
                has_higher = np.sum(counts[:, is_ + 1 :], axis=1) > 0
            else:
                has_higher = np.zeros(n_markets, dtype=bool)
            tie_share = np.where(has_higher, 0.0, 1.0 / (1.0 + counts[:, is_]))
            p_immediate[is_] = float(np.mean((tagged_action == 0) * tie_share))
            for iq, q in enumerate(q_values):
                event = tagged_action == (1 + iq)
                prob_q_early[is_, iq] = float(np.mean(event))
                if np.any(event):
                    selection = self._tag_selection_probability(
                        counts, v, p1, float(q), float(s), "old",
                        old_r[iq], lambda_new[iq],
                    )
                    pi_old[is_, iq] = float(np.mean(selection[event]))

        margin_now = p1 - self.a
        u_e = p_immediate[None, :] * margin_now
        for iq, _q in enumerate(q_values):
            old_net = (
                pi_old[:, iq][None, :] * (self.par.delta * p1 - self.a)
                - self.par.omega_old
            )
            u_e += prob_q_early[:, iq][None, :] * np.maximum(old_net, 0.0)
        u_e = np.where(margin_now >= -1.0e-12, u_e, -1.0e6)

        u_h = np.full_like(self.a, -self.par.omega_hidden)
        for iq, q in enumerate(q_values):
            margin_new = float(q) - self.a
            u_h += prob_q_base[iq] * np.where(
                margin_new >= -1.0e-12,
                pi_new[:, iq][None, :] * margin_new,
                0.0,
            )

        retain_advantage = np.empty((Q, self.C, self.S))
        for iq in range(Q):
            retain_advantage[iq] = (
                pi_old[:, iq][None, :] * (self.par.delta * p1 - self.a)
                - self.par.omega_old
            )

        return {
            "q_values": q_values,
            "u_e": u_e,
            "u_h": u_h,
            "retain_advantage": retain_advantage,
            "p_immediate": p_immediate,
            "prob_q_base": prob_q_base,
            "prob_q_early": prob_q_early,
            "pi_old": pi_old,
            "pi_new": pi_new,
            "lambda_early": lambda_early,
            "old_r": np.asarray(old_r),
            "lambda_new": np.asarray(lambda_new),
        }

    def _initial_profile(self, p1: float, p2: float, mode: str = "homotopy") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        q_values = np.unique(np.round(np.array([p1, p2], dtype=float), 12))
        Q = len(q_values)
        feasible_e = (p1 - self.a) >= 0.0
        feasible_h = (np.max(q_values) - self.a) >= 0.0
        if mode == "early":
            e0, h0 = 0.78, 0.10
        elif mode == "hidden":
            e0, h0 = 0.10, 0.78
        else:
            e0, h0 = 0.33, 0.33
        sigma_e = np.where(feasible_e, e0, 0.0)
        sigma_h = np.where(feasible_h, h0, 0.0)
        total = sigma_e + sigma_h
        over = total > 0.96
        sigma_e[over] *= 0.96 / total[over]
        sigma_h[over] *= 0.96 / total[over]
        retain = np.zeros((Q, self.C, self.S))
        positive_margin = (self.par.delta * p1 - self.a) > 0.0
        for iq in range(Q):
            retain[iq] = 0.4 * positive_margin
        return sigma_e, sigma_h, retain

    @staticmethod
    def _choose_by_min_key(
        market_index: np.ndarray,
        eligible_driver_index: np.ndarray,
        key: np.ndarray,
        n_markets: int,
    ) -> np.ndarray:
        chosen = np.full(n_markets, -1, dtype=np.int64)
        if eligible_driver_index.size == 0:
            return chosen
        markets = market_index[eligible_driver_index]
        keys = key[eligible_driver_index]
        minimum = np.full(n_markets, np.inf)
        np.minimum.at(minimum, markets, keys)
        winner_mask = keys == minimum[markets]
        winners = eligible_driver_index[winner_mask]
        chosen[market_index[winners]] = winners
        return chosen

    def paired_evaluate(
        self,
        m: float,
        rescue: Tuple[float, float, Profile],
        flat: Tuple[float, float, Profile],
        n_markets: int,
        seed: int,
        batch_size: int = 5_000,
    ) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
        """Evaluate rescue and flat on identical realized markets.

        Underlying N, driver types, rider values, and all auxiliary uniforms are
        common across policies. The paired standard error therefore applies to
        the menu-value difference directly.
        """
        rng = np.random.default_rng(seed)
        policies = {"rescue": rescue, "flat": flat}
        sum_metrics: Dict[str, Dict[str, float]] = {
            name: {
                "surplus": 0.0, "completion": 0.0, "period1": 0.0,
                "period2_old": 0.0, "period2_new": 0.0,
                "overlap_sum": 0.0, "cost_sum": 0.0,
                "completed_count": 0.0, "base_activation": 0.0,
                "high_activation": 0.0, "period1_surplus": 0.0,
                "period2_old_surplus": 0.0, "period2_new_surplus": 0.0,
                "high_new_completion": 0.0, "high_new_surplus": 0.0,
            }
            for name in policies
        }
        diff_sum = 0.0
        diff_sumsq = 0.0
        surplus_diff_sum = 0.0
        surplus_diff_sumsq = 0.0
        done = 0

        while done < n_markets:
            Bn = min(batch_size, n_markets - done)
            v = rng.random(Bn)
            n_driver = rng.poisson(m, Bn)
            market_index = np.repeat(np.arange(Bn, dtype=np.int64), n_driver)
            D = len(market_index)
            c_index = rng.choice(self.C, size=D, p=self.fc)
            s_index = rng.choice(self.S, size=D, p=self.fs)
            u_action = rng.random(D)
            u_retain = rng.random(D)
            u_select1 = rng.random(D)
            u_select2 = rng.random(D)

            surplus_by_policy: Dict[str, np.ndarray] = {}
            completion_by_policy: Dict[str, np.ndarray] = {}
            for name, (p1, p2, profile) in policies.items():
                q_values = profile.q_values
                Q = len(q_values)
                # Initial action, coupled by the same uniform.
                pe = profile.sigma_e[c_index, s_index]
                ph = profile.sigma_h[c_index, s_index]
                early = u_action < pe
                hidden = (u_action >= pe) & (u_action < pe + ph)

                counts_flat = np.bincount(
                    market_index[early] * self.S + s_index[early],
                    minlength=Bn * self.S,
                )
                early_counts = counts_flat.reshape(Bn, self.S)
                _lam_e, old_r, lambda_new = self._belief_objects(
                    m, p1, q_values, profile.sigma_e, profile.sigma_h, profile.retain
                )
                action, _, _ = self._rider_action(
                    early_counts, v, p1, q_values, old_r, lambda_new
                )

                selected = np.full(Bn, -1, dtype=np.int64)
                selected_period = np.zeros(Bn, dtype=np.int8)
                selected_new = np.zeros(Bn, dtype=bool)

                # Period 1: highest s, random within the top bin.
                now_market = action == 0
                has_early = np.sum(early_counts, axis=1) > 0
                best_s = np.where(
                    has_early,
                    self.S - 1 - np.argmax(early_counts[:, ::-1] > 0, axis=1),
                    -1,
                )
                eligible_now = np.where(
                    early & now_market[market_index] &
                    (s_index == best_s[market_index])
                )[0]
                chosen_now = self._choose_by_min_key(
                    market_index, eligible_now, u_select1, Bn
                )
                now_chosen_market = chosen_now >= 0
                selected[now_chosen_market] = chosen_now[now_chosen_market]
                selected_period[now_chosen_market] = 1

                # Period 2: actual old retention and hidden surfacing.
                continuation = action >= 1
                q_index_market = np.where(continuation, action - 1, 0)
                q_market = q_values[q_index_market]
                q_index_driver = q_index_market[market_index]
                q_driver = q_market[market_index]

                old_probability = profile.retain[
                    q_index_driver, c_index, s_index
                ]
                old = early & continuation[market_index] & (u_retain < old_probability)
                new = (
                    hidden & continuation[market_index] &
                    ((q_driver - self.a[c_index, s_index]) >= -1.0e-12)
                )
                period2_eligible = old | new
                g_driver = np.full(D, np.inf)
                g_driver[old] = p1 + self.beta_detour[s_index[old]]
                g_driver[new] = q_driver[new] + self.beta_detour[s_index[new]]

                min_g = np.full(Bn, np.inf)
                np.minimum.at(min_g, market_index[period2_eligible], g_driver[period2_eligible])
                tied_best = np.zeros(D, dtype=bool)
                finite_candidate = period2_eligible & np.isfinite(min_g[market_index])
                tied_best[finite_candidate] = (
                    np.abs(
                        g_driver[finite_candidate]
                        - min_g[market_index[finite_candidate]]
                    ) <= 1.0e-12
                )
                eligible_two = np.where(tied_best)[0]
                chosen_two = self._choose_by_min_key(
                    market_index, eligible_two, u_select2, Bn
                )
                two_candidate = chosen_two >= 0
                two_accept = two_candidate & (
                    self.par.beta * v - min_g > 1.0e-12
                )
                # Only continuation markets can be assigned here.
                two_accept &= continuation
                selected[two_accept] = chosen_two[two_accept]
                selected_period[two_accept] = 2
                selected_new[two_accept] = new[chosen_two[two_accept]]

                completed = selected >= 0
                selected_s = np.zeros(Bn)
                selected_a = np.zeros(Bn)
                if np.any(completed):
                    idx = selected[completed]
                    selected_s[completed] = self.s[s_index[idx]]
                    selected_a[completed] = self.a[c_index[idx], s_index[idx]]
                gross = v - self.par.ell * (1.0 - selected_s)
                surplus = np.where(completed, gross - selected_a, 0.0)
                surplus_by_policy[name] = surplus
                completion_by_policy[name] = completed.astype(float)

                sm = sum_metrics[name]
                sm["surplus"] += float(np.sum(surplus))
                sm["completion"] += float(np.sum(completed))
                sm["period1"] += float(np.sum(selected_period == 1))
                sm["period2_old"] += float(np.sum((selected_period == 2) & (~selected_new)))
                sm["period2_new"] += float(np.sum((selected_period == 2) & selected_new))
                sm["overlap_sum"] += float(np.sum(selected_s[completed]))
                sm["cost_sum"] += float(np.sum(selected_a[completed]))
                sm["completed_count"] += float(np.sum(completed))
                mask_p1 = selected_period == 1
                mask_old2 = (selected_period == 2) & (~selected_new)
                mask_new2 = (selected_period == 2) & selected_new
                sm["period1_surplus"] += float(np.sum(surplus[mask_p1]))
                sm["period2_old_surplus"] += float(np.sum(surplus[mask_old2]))
                sm["period2_new_surplus"] += float(np.sum(surplus[mask_new2]))
                sm["base_activation"] += float(np.sum(action == 1))
                if p2 > p1 + 1.0e-12:
                    high_index = int(np.argmax(q_values))
                    high_active = action == (1 + high_index)
                    sm["high_activation"] += float(np.sum(high_active))
                    high_new = mask_new2 & (q_index_market == high_index)
                    sm["high_new_completion"] += float(np.sum(high_new))
                    sm["high_new_surplus"] += float(np.sum(surplus[high_new]))

            # The platform objective is the completion indicator.  Surplus is
            # retained only as a secondary diagnostic.
            diff = completion_by_policy["rescue"] - completion_by_policy["flat"]
            diff_sum += float(np.sum(diff))
            diff_sumsq += float(np.sum(diff * diff))
            surplus_diff = surplus_by_policy["rescue"] - surplus_by_policy["flat"]
            surplus_diff_sum += float(np.sum(surplus_diff))
            surplus_diff_sumsq += float(np.sum(surplus_diff * surplus_diff))
            done += Bn

        policy_outputs: Dict[str, Dict[str, float]] = {}
        for name, (p1, p2, profile) in policies.items():
            sm = sum_metrics[name]
            complete_n = sm["completed_count"]
            completion_rate = sm["completion"] / n_markets
            policy_outputs[name] = {
                "m": float(m), "p1": float(p1), "p2": float(p2),
                "objective_name": OBJECTIVE_NAME,
                "objective_formula": OBJECTIVE_FORMULA,
                "objective_value": completion_rate,
                "completed_surplus": sm["surplus"] / n_markets,
                "completion": completion_rate,
                "completion_se": math.sqrt(max(completion_rate * (1.0 - completion_rate), 0.0) / n_markets),
                "period1_completion": sm["period1"] / n_markets,
                "old_period2_completion": sm["period2_old"] / n_markets,
                "new_period2_completion": sm["period2_new"] / n_markets,
                "period2_completion": (sm["period2_old"] + sm["period2_new"]) / n_markets,
                "mean_overlap_completed": sm["overlap_sum"] / complete_n if complete_n > 0 else math.nan,
                "mean_effective_cost_completed": sm["cost_sum"] / complete_n if complete_n > 0 else math.nan,
                "period1_surplus": sm["period1_surplus"] / n_markets,
                "old_period2_surplus": sm["period2_old_surplus"] / n_markets,
                "new_period2_surplus": sm["period2_new_surplus"] / n_markets,
                "base_continuation_activation": sm["base_activation"] / n_markets,
                "high_rescue_activation": sm["high_activation"] / n_markets,
                "high_new_completion": sm["high_new_completion"] / n_markets,
                "high_new_success_given_activation": (
                    sm["high_new_completion"] / sm["high_activation"]
                    if sm["high_activation"] > 0 else 0.0
                ),
                "mean_surplus_high_new": (
                    sm["high_new_surplus"] / sm["high_new_completion"]
                    if sm["high_new_completion"] > 0 else 0.0
                ),
                "early_share": profile.meta["early_share"],
                "hidden_share": profile.meta["hidden_share"],
                "max_regret": profile.meta["max_regret"],
            }

        mean_diff = diff_sum / n_markets
        variance = max(
            (diff_sumsq - n_markets * mean_diff * mean_diff) / max(n_markets - 1, 1),
            0.0,
        )
        completion_se = math.sqrt(variance / n_markets)

        mean_surplus_diff = surplus_diff_sum / n_markets
        surplus_variance = max(
            (surplus_diff_sumsq - n_markets * mean_surplus_diff * mean_surplus_diff)
            / max(n_markets - 1, 1),
            0.0,
        )
        surplus_gain_se = math.sqrt(surplus_variance / n_markets)

        delta_period1_completion = (
            policy_outputs["rescue"]["period1_completion"]
            - policy_outputs["flat"]["period1_completion"]
        )
        delta_old_period2_completion = (
            policy_outputs["rescue"]["old_period2_completion"]
            - policy_outputs["flat"]["old_period2_completion"]
        )
        delta_new_period2_completion = (
            policy_outputs["rescue"]["new_period2_completion"]
            - policy_outputs["flat"]["new_period2_completion"]
        )

        comparison = {
            "m": float(m),
            "objective_name": OBJECTIVE_NAME,
            "objective_formula": OBJECTIVE_FORMULA,
            # rescue_value is retained as a backward-compatible alias; in v1.1.0
            # it is exactly the paired completion-probability gain.
            "rescue_value": float(mean_diff),
            "completion_gain": float(mean_diff),
            "delta_period1_completion": float(delta_period1_completion),
            "delta_old_period2_completion": float(delta_old_period2_completion),
            "delta_new_period2_completion": float(delta_new_period2_completion),
            "rescue_value_se": float(completion_se),
            "completion_gain_se": float(completion_se),
            "rescue_value_ci_low": float(mean_diff - 1.96 * completion_se),
            "rescue_value_ci_high": float(mean_diff + 1.96 * completion_se),
            "completion_gain_ci_low": float(mean_diff - 1.96 * completion_se),
            "completion_gain_ci_high": float(mean_diff + 1.96 * completion_se),
            # Secondary, non-objective diagnostics.
            "surplus_gain": float(mean_surplus_diff),
            "surplus_gain_se": float(surplus_gain_se),
            "delta_period1_surplus": (
                policy_outputs["rescue"]["period1_surplus"]
                - policy_outputs["flat"]["period1_surplus"]
            ),
            "delta_old_period2_surplus": (
                policy_outputs["rescue"]["old_period2_surplus"]
                - policy_outputs["flat"]["old_period2_surplus"]
            ),
            "delta_new_period2_surplus": (
                policy_outputs["rescue"]["new_period2_surplus"]
                - policy_outputs["flat"]["new_period2_surplus"]
            ),
        }
        return policy_outputs["rescue"], policy_outputs["flat"], comparison



class FixedSupportRescueModel(RescueModel):
    def __init__(
        self,
        params: ModelParams,
        c: np.ndarray,
        fc: np.ndarray,
        s: np.ndarray,
        fs: np.ndarray,
    ) -> None:
        for support, weights in ((c, fc), (s, fs)):
            support, weights = np.asarray(support, float), np.asarray(weights, float)
            if support.ndim != 1 or not len(support) or support.shape != weights.shape:
                raise ValueError('Support and weights must be equal-length nonempty vectors')
            if not np.all(np.isfinite(support)) or np.any(support < 0) or np.any(support > 1) or not np.all(np.diff(support) > 0):
                raise ValueError('Support must strictly increase in [0,1]')
            if not np.all(np.isfinite(weights)) or np.any(weights <= 0) or not np.isclose(weights.sum(), 1., atol=1e-12, rtol=0):
                raise ValueError('Weights must be positive and sum to one')
        self._fixed_support = (
            np.asarray(c, dtype=float),
            np.asarray(fc, dtype=float),
            np.asarray(s, dtype=float),
            np.asarray(fs, dtype=float),
        )
        super().__init__(params)

    def _make_cost_support(self) -> Tuple[np.ndarray, np.ndarray]:
        c, fc, _, _ = self._fixed_support
        return c.copy(), fc.copy()

    def _make_route_support(self) -> Tuple[np.ndarray, np.ndarray]:
        _, _, s, fs = self._fixed_support
        return s.copy(), fs.copy()


# ---------------------------------------------------------------------------
# General utilities
# ---------------------------------------------------------------------------

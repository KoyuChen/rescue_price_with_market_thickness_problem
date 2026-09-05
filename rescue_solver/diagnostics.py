"""Profile validity, full-plan regrets and shape diagnostics."""
import math
from statistics import NormalDist
import numpy as np

REGRET_CAP=.00075
SUPPORT_CAP=.0015

def validate_profile(model,p1,p2,profile):
    shape=(model.C,model.S); q=np.unique(np.round([p1,p2],12))
    if not (0<=p1<=p2<=model.par.p_bar): raise ValueError('Invalid prices')
    if profile.sigma_e.shape!=shape or profile.sigma_h.shape!=shape or profile.retain.shape!=(len(q),*shape):
        raise ValueError('Wrong profile dimensions')
    if not np.array_equal(q,profile.q_values): raise ValueError('Price/profile mismatch')
    for a in (profile.sigma_e,profile.sigma_h,profile.retain):
        if not np.all(np.isfinite(a)) or np.any(a < -1e-12) or np.any(a>1+1e-12):
            raise ValueError('Nonfinite or invalid strategy probabilities')
    if np.any(profile.sigma_e+profile.sigma_h>1+1e-12): raise ValueError('Action probabilities exceed one')


def regret_diagnostics(model,p1,profile,ev,regret_tol=REGRET_CAP,support_tol=SUPPORT_CAP):
    pe,ph=profile.sigma_e,profile.sigma_h
    probs=np.stack([pe,ph,np.maximum(0,1-pe-ph)])
    adv=ev['retain_advantage']
    # v1.1.1 u_e is the value of early entry WITH optimal later retention.
    # The realized incumbent strategy instead uses profile.retain at that node.
    early_actual=ev['p_immediate'][None,:]*(p1-model.a)
    early_actual+=np.sum(ev['prob_q_early'].T[:,None,:]*profile.retain*adv,axis=0)
    early_actual=np.where(p1-model.a>=-1e-12,early_actual,-1e6)
    best=np.maximum.reduce([ev['u_e'],ev['u_h'],np.zeros_like(pe)])
    expected=pe*early_actual+ph*ev['u_h']
    full=np.maximum(0,best-expected)
    legacy=np.maximum(0,best-np.sum(probs*np.stack([ev['u_e'],ev['u_h'],np.zeros_like(pe)]),axis=0))
    retain_reg=np.maximum(adv,0)-profile.retain*adv
    feasible=model.a<=p1+1e-12
    retmax=float(np.max(retain_reg[:,feasible])) if np.any(feasible) else 0.
    gaps=best[None,:,:]-np.stack([ev['u_e'],ev['u_h'],np.zeros_like(pe)])
    init_support=float(np.max(np.where(probs>1e-3,np.maximum(gaps,0),0)))
    ret_support=np.maximum(np.where(profile.retain>1e-3,np.maximum(-adv,0),0),
                           np.where(profile.retain<1-1e-3,np.maximum(adv,0),0))
    retention_support=float(np.max(ret_support[:,feasible])) if np.any(feasible) else 0.
    idx=np.unravel_index(np.argmax(full),full.shape)
    return dict(legacy_initial_regret_max=float(legacy.max()),
        full_plan_regret_max=float(full.max()),retention_regret_max=retmax,
        max_regret=max(float(full.max()),retmax),initial_support_gap_max=init_support,
        retention_support_gap_max=retention_support,
        full_plan_minus_legacy_max=float(np.max(full-legacy)),
        witness=dict(cost_index=int(idx[0]),route_index=int(idx[1]),
                     cost=float(model.c[idx[0]]),fit=float(model.s[idx[1]])),
        sample_checks_pass=bool(max(float(full.max()),retmax)<=regret_tol
            and max(init_support,retention_support)<=support_tol))


def shape_diagnostics(m, value, se=None, alpha=.05):
    x=np.asarray(m,float); v=np.asarray(value,float)
    if len(x)!=len(v) or len(x)<3 or not np.all(np.isfinite(x)) or not np.all(np.diff(x)>0) or not np.all(np.isfinite(v)):
        raise ValueError('Need at least 3 ordered, unique, finite points')
    d=np.diff(v)
    peaks=[i for i in range(len(v)) if np.all(d[:i]>=0) and np.all(d[i:]<=0)]
    result=dict(raw_grid_weakly_single_peaked=bool(peaks),raw_peak_indices=peaks,
        negative_values_preserved=bool(np.any(v<0)),continuous_single_peak_proved=False,
        standard_errors_supplied=se is not None,observed_peak_m=float(x[np.argmax(v)]),
        note='Shape describes supplied values, not verified globally optimized WPBE values.')
    if se is not None:
        se=np.asarray(se,float)
        if se.shape!=v.shape or np.any(se<0) or not np.all(np.isfinite(se)):
            raise ValueError('Invalid standard errors')
        z=NormalDist().inv_cdf(1-alpha/(2*len(d)))
        radius=z*np.sqrt(se[:-1]**2+se[1:]**2)
        result.update(differences=d.tolist(),difference_ci_low=(d-radius).tolist(),
            difference_ci_high=(d+radius).tolist(),
            assumption='Independent fixed-design reporting estimates across thickness; '
                       'normal approximation, not a finite-sample exact interval.')
    return result


def thickness_diagnostics(rows, alpha=.05):
    """Describe prices and test a selected interior peak without imposing either.

    Simultaneous all-pair normal intervals account for choosing the largest
    observed point. They cover held-out MC noise, not equilibrium/search error.
    """
    if len(rows) < 3 or not 0 < alpha < 1:
        raise ValueError('At least three thickness rows and 0 < alpha < 1 required')
    ordered = sorted(rows, key=lambda r: r['m'])
    x = np.asarray([r['m'] for r in ordered], float)
    prices = np.asarray([[r['p1'], r['p2'], r['p_flat']] for r in ordered], float)
    values = np.asarray([r['V_estimate'] for r in ordered], float)
    ses = np.asarray([r['comparison']['completion_gain_se'] for r in ordered], float)
    shape_diagnostics(x, values, ses, alpha)
    if not np.all(np.isfinite(prices)):
        raise ValueError('Nonfinite price')
    nested = (prices[:, 0] <= prices[:, 2]+1e-12) & (prices[:, 2] <= prices[:, 1]+1e-12)
    pairs = len(rows)*(len(rows)-1)//2
    z = NormalDist().inv_cdf(1-alpha/(2*pairs))
    peak = int(np.argmax(values))
    contrasts = []
    for j in range(len(rows)):
        if j == peak:
            continue
        diff = float(values[peak]-values[j])
        radius = float(z*np.hypot(ses[peak], ses[j]))
        contrasts.append(dict(other_m=float(x[j]), difference=diff,
                              simultaneous_ci_low=diff-radius, simultaneous_ci_high=diff+radius))
    interior = 0 < peak < len(rows)-1
    endpoint_contrasts = [c for c in contrasts if c['other_m'] in (x[0], x[-1])]
    supported = interior and all(c['simultaneous_ci_low'] > 0 for c in endpoint_contrasts)
    return dict(m=x.tolist(), price_order_p1_le_flat_le_p2=nested.tolist(),
        price_order_holds_at_all_observed_points=bool(nested.all()),
        violating_price_order_m=x[~nested].tolist(),
        price_differences={k: np.diff(prices[:, j]).tolist() for j, k in enumerate(('p1', 'p2', 'p_flat'))},
        prices_weakly_decrease={k: bool(np.all(np.diff(prices[:, j]) <= 1e-12))
                                for j, k in enumerate(('p1', 'p2', 'p_flat'))},
        rescue_spread=(prices[:, 1]-prices[:, 0]).tolist(),
        observed_peak_m=float(x[peak]), observed_peak_is_interior=interior,
        peak_vs_other_thicknesses=contrasts,
        interior_peak_exceeds_both_endpoints_under_MC_only=bool(supported),
        all_point_contrasts_family_size=pairs, alpha=alpha,
        all_grid_numerical_checks_pass=all(r.get('numerical_grid_comparison_ready', False) for r in ordered),
        equilibrium_price_relation_verified=False, optimized_middle_peak_verified=False,
        scope='Descriptive grid candidates only. Simultaneous normal intervals assume independent '
              'fixed-design reporting draws across thickness; exclude equilibrium, type and price errors.')

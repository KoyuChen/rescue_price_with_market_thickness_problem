# Numerical results: three supply regimes (legacy executed-contact objective)

> This file documents the earlier cost per executed outer contact. It is kept
> for robustness and provenance only. The maintained committed-reach results
> are in `committed_reach_results.md` and
> `results/csv/regime_comparison_committed.csv`.

## Design and calibration

For every environment \((m,\beta,\delta)\), the program separately solves:

1. incumbent-only recall with optimized \((p_1,p_2)\);
2. fixed-footprint fresh arrivals with optimized \((p_1,p_2)\);
3. expanded search with optimized \((p_1,p_2,s)\).

Every candidate policy re-enumerates and validates its pure cutoff-WPBE
correspondence. The platform uses conservative selection on

\[
J_\kappa=M-\kappa Q^O.
\]

The archived formal solver first computes the requested nested profile
(fix \(p_1\), optimize \(p_2,s\), then optimize \(p_1\)) and then challenges
it with an independent deterministic-seed differential-evolution search. Any
better basin is included in dense cutoff-WPBE certification. Accordingly,
"optimized" below means the best certified candidate found by both searches,
not an analytic proof of a continuous global maximum.

The formal grid uses:

- \(m\in\{.5,.75,1,1.5,2,3,4,6,8,12,16\}\);
- \(\beta\in\{.6,.8,.9\}\);
- \(\delta\in\{.4,.8,.95\}\);
- \((\tau,\omega,\bar s,\kappa)=(.25,.8,4,.0125)\).

This yields 99 environments and 297 optimized regime outcomes. All 297 final
policies have one cutoff-WPBE in the computed correspondence, and all 297 root
sets are stable under the archived grid-refinement certification. This is a
numerical fact for the grid, not a global uniqueness theorem.

## Main slice: value of time-homogeneous arrivals

For \((\beta,\delta)=(.8,.8)\), the completion comparison is:

| \(m\) | Incumbents only | Fixed arrivals | Arrival gain (pp) |
|---:|---:|---:|---:|
| .5 | .1154 | .1873 | 7.20 |
| 1 | .2094 | .3185 | 10.91 |
| 2 | .3520 | .4870 | 13.50 |
| 3 | .4539 | .5889 | 13.50 |
| 4 | .5295 | .6567 | 12.72 |
| 6 | .6330 | .7410 | 10.80 |
| 8 | .6998 | .7914 | 9.16 |
| 12 | .7801 | .8489 | 6.87 |
| 16 | .8264 | .8809 | 5.45 |

The arrival layer is hump-shaped on this grid, with an almost flat top at
\(m=2\)--3 and the displayed maximum at \(m=3\). This is an optimized
equilibrium-design pattern, not a fixed-price decomposition.

## Main slice: costly expanded search

The best cross-checked expanded-search candidate targets \(J_{.0125}\). Its
selected multiplier and net value over fixed-footprint arrivals are:

| \(m\) | \(s^*\) | \(100(V_E^\kappa-V_A)\) |
|---:|---:|---:|
| .5 | 4.000 | 9.99 |
| 1 | 4.000 | 11.45 |
| 2 | 3.938 | 8.84 |
| 3 | 3.059 | 5.94 |
| 4 | 2.512 | 3.98 |
| 6 | 1.876 | 1.78 |
| 8 | 1.504 | .75 |
| 12 | 1.112 | .05 |
| 16 | 1.000 | 0 |

Thus the same model generates a search-cap region, an interior-search region,
and an endogenous no-expansion choice. At \(m=16\), the best cross-checked
candidate selects \(s=1\) once expected outer contacts are priced.

## Comparative market conditions

The maximum arrival gain rises with both rider patience and incumbent patience
over the formal grid:

| \(\delta\) \textbackslash \(\beta\) | .6 | .8 | .9 |
|---:|---:|---:|---:|
| .4 | 10.7 | 12.8 | 13.7 |
| .8 | 11.2 | 13.5 | 14.6 |
| .95 | 11.3 | 13.8 | 14.9 |

The first grid thickness at which expanded search selects \(s^*=1\) is
greater than 16 for \(\beta=.6\) and 16 for \(\beta\in\{.8,.9\}\), with
little movement across \(\delta\) at the displayed resolution.

The independent adversarial pass improves on the nested-profile candidate in
292 of 297 rows, usually by a small amount (mean \(J\) improvement about
\(5.0\times10^{-4}\), maximum about \(3.9\times10^{-3}\)). This diagnostic is
why the archive reports the cross-checked candidate rather than silently
treating a single local refinement as the maximum.

## Interpretation

- Incumbent-only versus fixed arrivals identifies the supply value of an
  independent core cohort. Core notification infrastructure is normalized as
  installed and free.
- Fixed arrivals versus expanded search identifies the incremental value of
  geographic reach under a cost per executed outer contact.
- Driver-paid pickup cost \(d(u)\) thins outer willingness but is not counted
  again as a platform cost.
- If core activation is itself a design choice, add \(\kappa_CQ^C\); if the
  target is platform profit, separate rider fares from driver wages.

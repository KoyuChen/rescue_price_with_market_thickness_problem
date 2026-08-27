# Closest-paper positioning

## 1. Equilibrium architecture

[Hu, Hu, and Zhu (2022)](https://doi.org/10.1287/msom.2020.0960) organize a
two-period ride-hailing model as individual threshold behavior, equilibrium
regimes, policy comparison, and comparative statics of regime boundaries.
That is the right proof architecture here.  The present model differs because
first-window incumbents know the focal order and may reject it strategically;
after universal rejection, the rider updates and chooses abandon, repeat, or
rescue, while fresh drivers see the order only in the terminal window.

The theoretical chain should therefore be written as:

1. characterize the complete symmetric cutoff-WPBE correspondence;
2. prove the spatial thinning and search-scope results within one branch;
3. prove ordered peaks for adjacent nested controls on a common branch;
4. lift the order to the re-optimized mechanism values only under an explicit
   branch-stability or uniform-separation condition.

## 2. Spatial scope and pickup timing

[Yang, Qin, Ke, and Ye (2020)](https://doi.org/10.1016/j.trb.2019.11.005)
jointly choose matching interval and maximum pickup radius.  This supports a
radius-based scope control, but it has no committed same-order payment path or
strategic reject-and-wait response.

[Qin, Yang, and Liu (2025)](https://doi.org/10.1016/j.trc.2025.105318) use
round-specific broadcast radii under spatial Poisson arrivals.  This is the
closest notification design.  The distinction here is joint design of
`(p1,p2,s)` after universal rejection, with Bayesian rider continuation and the
complete driver cutoff-WPBE solved inside the mechanism problem.

[Wang, Zhang, and Zhang (2024)](https://doi.org/10.1287/opre.2022.2399),
*On-Demand Ride-Matching in a Spatial Model with Abandonment and
Cancellation*, treat pickup after matching and characterize matching scope
through a scalar index crossing.  This supports winner-only pickup timing and
provides the cleanest precedent for writing the search-cost condition as
`Psi(s;m)=1`, with expansion for `Psi>1` and contraction for `Psi<1`.

[Feng, Kong, and Wang (2021)](https://doi.org/10.1287/msom.2020.0880) study a
matching-distance cap.  Their displayed cap formula is a heuristic supported
by numerics, not a theorem characterizing an optimal cap.  It should not be
cited as a formal radius proposition.

The Lyft notification-set model of
[Ekbatani et al. (2026)](https://arxiv.org/html/2603.21533v2) gives a
set-dependent marginal cutoff: adding a notified driver is beneficial only
when the driver's score exceeds a threshold.  It is useful evidence that
notification scope is a resource-allocation decision rather than a free pool
multiplier.

## 3. Thickness and intermediate-value statements

[Afèche, Liu, and Maglaras (2023)](https://doi.org/10.1287/msom.2023.1221)
use scarce, moderate, and ample capacity thresholds.  Their nested controls
have value on an intermediate interval, producing a zero-positive-zero support
statement.  They do not claim that the value function is globally unimodal or
has a unique peak.  We should borrow the regime wording, not overread it as a
peak theorem.

[Zhao, Papier, and Teo (2024)](https://doi.org/10.1287/msom.2021.0354) show
that delivery-platform cost is quasi-convex in market thickness and characterize
an intermediate optimum.  Weak quasi-convexity does not by itself imply a
unique optimum.

[Nikzad (2022)](https://afshin-nikzad.com/pdfs/on-demand.pdf) uses two
thresholds and states comparative statics only on the interval where they are
proved.  This is the right conservative language when a derivative sign is
known locally but its global reversal has not been established.

## 4. Exact contribution boundary

Neither search radius, price-induced supply, nor an intermediate-thickness
effect is new by itself.  The defensible new theoretical object is:

- three strictly nested rescue mechanism classes;
- universal-rejection screening of incumbents who already know the order;
- time-homogeneous fresh terminal supply under fixed reach and Poisson-thinned
  outer supply under expanded reach;
- incumbent retention `omega` entering both the aggregate terminal pool and
  the focal waiting payoff;
- Bayesian rider continuation without realized driver counts;
- outer mechanism design over the complete cutoff-WPBE correspondence; and
- a strict ordering of the two adjacent mechanism-gain peak locations on a
  common branch, plus an explicit stability condition for the full optimized
  value gaps.

The current full-model figure is evidence for the last item.  The theorem in
`ordered_peaks_theorem.md` proves the branchwise result and gives an exact
counterexample showing why policy-specific continuation or branch switching
cannot be ignored.

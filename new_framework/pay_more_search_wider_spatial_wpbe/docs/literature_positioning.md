# Closest-paper positioning and pickup-cost timing

## Hu, Hu, and Zhu (2022)

[Surge Pricing and Two-Sided Temporal Responses in Ride Hailing](https://doi.org/10.1287/msom.2020.0960)
uses a two-period surge environment in which drivers may relocate before
matching and incur the relocation cost when they make that move. This archive
borrows its fixed-plus-distance spatial language, but deliberately changes the
timing: the incremental pickup cost here is paid only by the assigned winner.
The present platform also commits to how widely a failed focal order will be
notified.

## Yang, Qin, Ke, and Ye (2020)

[Optimizing matching time interval and matching radius in on-demand ride-sourcing markets](https://doi.org/10.1016/j.trb.2019.11.005)
models the matching radius as a maximum pickup distance and studies its tradeoff
with matching interval, matching rate, waiting, and pickup distance. It
supports a radius-based search control, but does not have a committed
same-order payment path or strategic reject-and-wait behavior.

## Qin, Yang, and Liu (2025)

[Two-round broadcast matching in ride-sourcing markets](https://doi.org/10.1016/j.trc.2025.105318)
is the closest search-design paper: it uses round-specific broadcast radii and
spatial Poisson arrivals. The remaining distinction is joint design of
`(p1,p2,s)` after universal rejection, with the driver cutoff-WPBE and Bayesian
rider continuation solved inside the mechanism problem.

## Wang, Zhang, and Zhang (2024)

[Online Ride-Matching Decisions with High-Dimensional State Space](https://doi.org/10.1287/opre.2022.2399)
models pickup after matching: an assigned driver enters a pickup state, and
pickup duration occupies system capacity. This supports treating pickup as an
assignment-contingent friction rather than a sunk cost paid by every notified
driver. Its pickup-quality control is not an order-level rescue price/search
mechanism.

## Castillo, Knoepfle, and Weyl (2024)

[Surge Pricing Solves the Wild Goose Chase](https://doi.org/10.1287/mnsc.2022.00096)
links spatial thickness to pickup distance and the number of dispatched drivers
traveling toward riders. This again supports the post-match pickup-time
interpretation, although its market-level surge analysis differs from the
same-order rescue game here.

## Contribution boundary

Neither search radius nor price-induced supply is new by itself. The promising
theoretical object is the interaction of:

1. universal-rejection screening of incumbents who already know the order;
2. a publicly committed same-order payment path;
3. a separately committed search-area multiplier;
4. fresh second-window Poisson supply under winner-only pickup cost;
5. Bayesian rider continuation without observing realized driver counts; and
6. an outer mechanism design constrained by the complete cutoff-WPBE
   correspondence.

The current closed-form spatial thinning result is a useful foundation. The
headline theory still requires sufficient conditions for the numerical
thin/intermediate/thick policy allocation; the archived figures should not be
described as a proved global comparative-statics theorem.

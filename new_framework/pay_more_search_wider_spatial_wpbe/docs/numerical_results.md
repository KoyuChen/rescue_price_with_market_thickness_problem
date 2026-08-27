# Numerical results

Formal configuration:

- `tau=.25`, `s_bar=4`.
- `m in {.5,.75,1,1.5,2,3,4,6,8,12,16}`.
- Main slice: `beta=delta=.8`.
- Market-condition slices: `beta in {.6,.9}` and
  `delta in {.4,.8,.95}`.
- 77 environments and 231 separately optimized mechanism outcomes.
- Conservative selection over the complete cutoff-WPBE correspondence.

## Main slice: optimized completion

| `m` | Flat `(p,p,1)` | Fixed `(p1,p2,1)` | Expanded `(p1,p2,s)` | Fixed gain (pp) | Expanded gain (pp) |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.182982 | 0.189448 | 0.295490 | 0.6466 | 10.6041 |
| 1 | 0.309654 | 0.322106 | 0.448515 | 1.2452 | 12.6410 |
| 2 | 0.471098 | 0.491793 | 0.603679 | 2.0695 | 11.1887 |
| 4 | 0.634394 | 0.661463 | 0.731314 | 2.7069 | 6.9850 |
| 6 | 0.717024 | 0.745087 | 0.791841 | 2.8063 | 4.6754 |
| 8 | 0.767341 | 0.794950 | 0.828238 | 2.7609 | 3.3288 |
| 16 | 0.859952 | 0.882394 | 0.896601 | 2.2442 | 1.4207 |

The fixed-rescue increment peaks near `m=6` in the main slice. The expanded
search increment peaks much earlier, near `m=1`, and declines with thickness.

## Representative optimized policies

| `m` | Mechanism | `p1*` | `p2*` | `s*` | WPBE cutoff `a*` | Holdout share |
|---:|---|---:|---:|---:|---:|---:|
| 0.5 | Flat | 0.408167 | 0.408167 | 1.000 | 0.408167 | 0.0000 |
| 0.5 | Fixed | 0.341500 | 0.449247 | 1.000 | 0.301347 | 0.1176 |
| 0.5 | Expanded | 0.333333 | 0.403333 | 4.000 | 0.281759 | 0.1547 |
| 1 | Flat | 0.368500 | 0.368500 | 1.000 | 0.368500 | 0.0000 |
| 1 | Fixed | 0.298427 | 0.416296 | 1.000 | 0.261538 | 0.1236 |
| 1 | Expanded | 0.262093 | 0.356227 | 4.000 | 0.215665 | 0.1771 |
| 4 | Flat | 0.238760 | 0.238760 | 1.000 | 0.238760 | 0.0000 |
| 4 | Fixed | 0.180260 | 0.288714 | 1.000 | 0.161122 | 0.1062 |
| 4 | Expanded | 0.150412 | 0.225115 | 3.769 | 0.133075 | 0.1153 |
| 16 | Flat | 0.105719 | 0.105719 | 1.000 | 0.105719 | 0.0000 |
| 16 | Fixed | 0.069596 | 0.117986 | 1.000 | 0.062909 | 0.0961 |
| 16 | Expanded | 0.061649 | 0.110565 | 2.089 | 0.055422 | 0.1010 |

These are not fixed-`p1` counterfactuals. Every row is the solution of its own
outer mechanism problem, and every objective evaluation re-solves the induced
cutoff-WPBE.

## Market-condition patterns

- Fixed rescue is modest in thin markets, rises to an intermediate-thickness
  peak, and eventually declines as the flat benchmark approaches high
  completion.
- Expanded search creates its largest incremental value in thin and
  moderately thin markets, where the core catchment is the binding scarcity.
- Higher rider delay tolerance `beta` raises both layers' potential value.
- Driver patience `delta` changes fixed-rescue value visibly through the
  incumbent holdout option; expanded-search value is much less sensitive in
  the displayed grid because outer drivers are fresh to the order.

These are numerical comparative statics, not global theorems.

## Verification

- All 231 final outcomes have one cutoff-WPBE and zero equilibrium completion
  spread.
- All final policies preserve the same root set on grids 401, 801, and 1601.
- A denser independent re-optimization at `m={.5,1,4,16}` changes completion by
  at most `0.0001123533` (0.0112 percentage points).
- A 120-policy adversarial root test is stable on grids 151, 301, and 601 and
  finds no multiple cutoff-WPBE.
- In 300,000 Poisson-thinning replications, simulated coverage differs from
  exact coverage by `-0.0007708`, about 1.22 simulated standard errors.
- 13 unit tests pass.

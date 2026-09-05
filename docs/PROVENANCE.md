# Source and verification

The economic baseline is the user's v1.1.1 research-precision model, not its
historical numerical answers. The original engine SHA-256 was:

`c1ece6dd81a2286e889110238ac85c9c82cf26942f3fcd4b9d811c00e83f1b69`.

`rescue_solver/core.py` extracts the model parameters, finite supports, belief
objects, rider best response, tie allocation, tagged-driver payoff evaluation,
initialization and explicit paired market simulator. The old price optimizer,
fallback logic, certification wrappers, plots and result tables are excluded.
The old IID tagged payoff evaluator remains solely as an independent numerical
reference; production solving uses `ValueIntegratedEvaluator`.

The standalone implementation adds strict model/support validation and exposes
the existing random OD generator as `draw_routes`. A degenerate all-zero overlap
sample is now represented by a single zero-support point. The default route
budget is 800000, matching the earlier core configuration. No economic payoff,
driver information set or platform objective was changed during extraction.

`solver.py` implements piecewise-affine value integration, Poisson sampling or
bounded enumeration, full-plan regret checks, zero-temperature response,
conditional-probability uncertainty and all-menu grid comparison. `cli.py`
implements fresh random route seeds, independent selection/report samples,
source-checked menu-level resume, saved-profile re-audit and raw shape diagnostics.
Every run records all module hashes and Python/NumPy versions.

## Tests included

- Independent direct IID and dense-value integration comparisons.
- Explicit realized-market completion versus integrated completion.
- Poisson state probabilities, retained tail mass and state-count limits.
- A positive continuation region missed by 50000 naive value draws.
- Unobserved posterior intervals and nonconvergence failing the checks.
- Zero-trade and positive-trade finite toy problems.
- Full-plan/retention complementarity, flat nesting and non-clipped shape.
- Small weighted regret cannot hide a large positive-probability support gap.
- Random OD formula, seed reproduction and all-zero-route support.
- Unknown/invalid configuration, corrupt profile, seed-mismatched resume.
- Independent re-audit leaving the saved policy unchanged.
- End-to-end complete small grids retaining unresolved candidates.
- Serial and parallel thickness execution producing identical fixed-design summaries.
- Price-order violations and statistically inconclusive interior peaks are preserved.

As an extraction check, the standalone economic kernel and original v1.1.1
kernel were evaluated with identical support draws and seeds at three menus
with m=1,6,48. Supports and every tagged-payoff output field matched exactly.
This checks extraction, not the correctness of the economic assumptions or a
WPBE theorem. No runtime test requires the historical package.

No continuous-type equilibrium, off-path belief system, global continuous-price
optimum or single-peakedness result has been certified. Fixed-menu and coarse-grid
integration checks are software checks, not a replacement for a research run.

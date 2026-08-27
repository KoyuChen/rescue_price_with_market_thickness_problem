# Pay More or Search Wider? Spatial Pickup WPBE Archive

This folder is a self-contained archive of the new spatial rescue framework.
It does not replace the repository's maintained manuscript or legacy model.

## Design question

The platform chooses among three strictly nested mechanism classes:

\[
\mathcal M_0=\{(p,p,1)\}
\subset
\mathcal M_F=\{(p_1,p_2,1):p_2\ge p_1\}
\subset
\mathcal M_E=\{(p_1,p_2,s):p_2\ge p_1,\ 1\le s\le \bar s\}.
\]

- **Flat fixed reach** uses one optimized payment and the core second-window
  catchment.
- **Fixed-reach rescue** commits to a second-window payment in the same
  catchment.
- **Expanded-search rescue** also commits to an area multiplier `s`.

Every second window has a time-homogeneous core fresh cohort
`Pois(m)`. Expanded search adds only an independent outer-annulus cohort
`Pois((s-1)m)`.

First-window rejectors remain available and eligible with probability
`omega=alpha*chi`.  This factor multiplies both their terminal intensity and
the focal rejector's continuation payoff.  The archived formal grid uses
`omega=1`; the solver supports any value in `[0,1]`.

## Equilibrium-constrained mechanism design

For every candidate mechanism `mu`, the code enumerates the complete symmetric
cutoff-WPBE correspondence. It verifies the driver best-response inequalities
on the full cost domain using the exact piecewise-affine payoff structure. The
platform then solves

\[
V_k(\theta)=
\max_{\mu\in\mathcal M_k}
\min_{a\in\mathcal E^{\mathrm{WPBE}}(\mu;\theta)} M(\mu,a),
\qquad \theta=(m,\beta,\delta).
\]

The numerical nesting is literal: fix `p1`, optimize the admissible `p2,s`
while re-solving the inner WPBE at every evaluation, and only then optimize
`p1`.

## Maintained pickup-cost timing

Fresh drivers pay no notification-time activation or relocation cost. A driver
at normalized area rank `u=(r/R0)^2` pays

\[
d(u)=\tau(\sqrt u-1)_+
\]

only if selected for the order. Therefore a fresh driver responds iff
`c+d(u)<=p`, and Poisson thinning gives

\[
e(p,s)=m\int_0^s F\!\left(p-d(u)\right)du.
\]

There is no fresh-entry congestion fixed point in this maintained version.

## Contents

- `src/`: inner cutoff-WPBE solver, outer mechanism-design solver, formal
  experiment runner, and numerical audits.
- `tests/`: model, equilibrium, certification, and mechanism-nesting tests.
- `results/`: the 77-environment formal grid, dense re-optimization,
  random-policy root stress, Monte Carlo audit, and run metadata.
- `figures/`: publication-quality PDF and PNG outputs.
- `group_meeting/`: preserved source pages 1--2, the new six-page extension,
  merge script, and the verified eight-page PDF.
- `docs/`: formal setting, numerical summary, and closest-paper positioning.
  `docs/ordered_peaks_theorem.md` contains the branchwise theorem, proof,
  stability lift, counterexample, and search-cost extension.

## Reproduce

From this directory:

```bash
python -m pip install -r requirements.txt
make test
make quick
make audit
make group-note
```

`make numerics` re-runs the full 77-environment outer optimization. The formal
run uses a search cap `s_bar=4`, pickup rate `tau=.25`, and certifies the final
cutoff correspondence on grids 401, 801, and 1601.

## Current numerical audit

- 77 environments, 3 mechanism classes, 231 outer optima.
- All 231 final policies have a unique cutoff-WPBE in the formal grid.
- All final correspondences are stable on grids 401, 801, and 1601.
- Independent dense re-optimization changes completion by at most
  `0.0001123533`, or 0.0112 percentage points.
- 120 random policies retain the same root set under grid refinement; none has
  multiple cutoff-WPBE in this stress sample.
- 15 tests pass, including incumbent-retention consistency.

The uniqueness findings are numerical facts for the archived grid, not a
global uniqueness theorem.

## Theoretical status

On a common Poisson-WPBE branch, the adjacent gains from adding contingent pay
and then expanded search are strictly single-peaked in market thickness.  Their
closed-form peaks satisfy

\[
m_S^*<\frac1{r+\lambda_F}<m_P^*.
\]

This branchwise theorem does not automatically apply to the re-optimized value
envelopes: rider-composition changes and policy switching can reverse the order
or create multiple peaks.  The theorem note states a uniform-separation
condition that is sufficient to lift the ordering to the full mechanism
design.

The archived objective maximizes completion with free search contacts.  It is
a maximal-completion frontier.  The economic extension uses expected extra
contacts `Q^O=q_R*m*(s-1)` and objective `B*M-kappa*Q^O`, or an equivalent
notification budget.

# Rescue pricing with arrivals and costly expanded search

This folder is a self-contained archive of the new group-meeting framework. It
keeps the original manuscript separate and preserves physical pages 1--2 of
the earlier group-meeting note.

## Research design

The extension compares three supply/notification regimes:

| Regime | Second-window supply | Platform policy |
|---|---|---|
| Incumbents only | Retained first-window rejectors | \((p_1,p_2)\) |
| Fixed footprint with arrivals | Rejectors plus an independent fresh core cohort | \((p_1,p_2)\) |
| Expanded search | The same core supply plus an outer annulus in rescue | \((p_1,p_2,s)\) |

The first two are supply benchmarks, not nested mechanism sets. Fixed-footprint
arrivals are nested in expanded search because \(s=1\) exactly reproduces the
fixed footprint.

Every candidate policy is evaluated at a complete pure cutoff-WPBE. The outer
design literally fixes \(p_1\), optimizes the admissible \(p_2,s\) while
re-solving the WPBE at every objective evaluation, and then optimizes \(p_1\).
Each formal run also applies an independent differential-evolution search to
the equivalent joint policy domain. Any better basin is fed back into the same
dense WPBE certification. This is an adversarial numerical cross-check, not a
claim that a continuous global maximum has been proved analytically.

## Time-homogeneous arrivals and incumbent exit

The two response windows have equal length:

\[
N_1\sim\operatorname{Pois}(m),\qquad
N_2^C\sim\operatorname{Pois}(m),\qquad N_1\perp N_2^C.
\]

Here \(m\) is a per-window cohort flow. A first-window rejector remains
physically available with probability \(\omega\). The main numerical
calibration uses \(\omega=.8\), so incumbent exit is active in both terminal
supply and the focal rejector's waiting payoff.

## Search multiplier and costs

The core footprint has area one. Expanded rescue uses area multiplier \(s\):

\[
R(s)=R_0\sqrt{s},\qquad
N_2^O(s)\sim\operatorname{Pois}((s-1)m).
\]

An outer driver at area rank \(u=(\ell/R_0)^2\) pays

\[
d(u)=\tau(\sqrt u-1)_+
\]

only after assignment. Consequently she volunteers iff \(c+d(u)\le p\), and
the outer cohort is thinned without an entry fixed point.

Driver pickup cost is distinct from the platform's search/contact cost.
Expected incremental outer contacts are

\[
Q^O=(1-p_1)e^{-mF(a)}\eta_2(a)m(s-1),
\]

and the maintained outer objective is

\[
J_\kappa=BM-\kappa Q^O.
\]

This is completion net of notification opportunity cost, not platform profit.
The main costly-search slice uses
\((B,\kappa,\tau,\omega,\bar s)=(1,.0125,.25,.8,4)\).

## Contents

- src/spatial_wpbe.py: inner cutoff-WPBE solver and exact type-domain
  validation.
- src/spatial_design.py: nested outer mechanism design, independent global
  basin search, and conservative selection on \(J_\kappa\).
- src/run_regime_numerics.py: reproducible grid runner over
  \((m,\beta,\delta)\).
- src/plot_regime_comparison.py: group-meeting figures.
- tests/test_spatial_wpbe.py: spatial thinning, exit, regime, WPBE,
  certification, and costly-search tests.
- docs/model_spec.md: formal model and objective.
- results/: optimized policies and run metadata.
- group_meeting/: unchanged source pages 1--2, six replacement pages, merge
  script, and the verified eight-page PDF.

## Reproduce

    python -m pip install -r requirements.txt
    make test
    make numerics
    make free-search
    make audit
    make figures
    make group-note

make quick runs a small main-slice diagnostic. The default Makefile uses one
worker for portability; run_regime_numerics.py --workers N parallelizes
independent environments.

## Interpretation boundary

- Regime \(I\rightarrow A\) reports the best cross-checked completion value
  found for an installed time-homogeneous core cohort.
- Regime \(A\rightarrow E\) reports the net value of incremental geographic
  reach after pricing outer contacts.
- If core broadcast itself is a platform choice, add a core-contact term
  \(\kappa_CQ^C\). If the objective is platform profit, separate rider fares
  from driver wages.
- The previous ordered-peaks theorem remains archived in
  docs/ordered_peaks_theorem.md; it is intentionally not used as the main
  group-meeting narrative.

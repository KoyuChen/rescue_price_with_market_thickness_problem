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

Driver pickup cost is distinct from the platform's search-capacity cost.  The
main specification charges the failure-contingent capacity required to honor
the promised outer footprint,

\[
Q^{\mathrm{com}}=(1-p_1)e^{-mF(a)}m(s-1),
\]

and the maintained outer objective is

\[
J_\kappa=BM-\kappa Q^{\mathrm{com}}.
\]

Unlike cost per executed rescue contact, this resource does not disappear at
the rider's rescue-activation boundary.  The code retains executed outer
contacts as a reported diagnostic and optional legacy objective.  The main
objective is completion net of committed search capacity, not platform profit.
The main costly-search slice uses
\((B,\kappa,\tau,\omega,\bar s)=(1,.0125,.25,.8,4)\).

## Contents

- src/spatial_wpbe.py: inner cutoff-WPBE solver and exact type-domain
  validation.
- src/spatial_design.py: nested outer mechanism design, independent global
  basin search, and conservative selection on \(J_\kappa\).
- src/run_regime_numerics.py: reproducible grid runner over
  \((m,\beta,\delta)\).
- src/plot_group_meeting_five_page.py: the two committed-cost figures used in
  the five-page group-meeting note.
- src/plot_regime_comparison.py: archived broader figure generator.
- tests/test_spatial_wpbe.py: spatial thinning, exit, regime, WPBE,
  certification, and costly-search tests.
- docs/model_spec.md: formal model and objective.
- docs/committed_reach_results.md: the audited main numerical slice used by
  the five-page group-meeting note.
- docs/peak_search_proof_note.tex: proof note establishing unique cutoff-WPBE,
  full-design endpoint/interior-peak results, ordered peaks on a common branch,
  counterexamples to unconditional ordering, and endogenous search-cost
  thresholds.
- output/pdf/peak_search_proof_note.pdf: rendered and visually checked proof
  note.
- results/csv/regime_comparison_committed.csv: main committed-reach policies;
  the older executed-contact tables remain archived separately.
- group_meeting/: unchanged source pages 1--2, three replacement pages, merge
  script, and the five-page PDF.

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
  reach after pricing failure-contingent committed outer capacity.
- If core broadcast itself is a platform choice, add a core-contact term
  \(\kappa_CQ^C\). If the objective is platform profit, separate rider fares
  from driver wages.
- The previous ordered-peaks note remains archived in
  docs/ordered_peaks_theorem.md. Its common-branch theorem is valid, but its
  frozen-composition search index is not the complete-WPBE first-order
  condition; the new proof note records the corrected scope.

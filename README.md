# Rescue pricing with latent market thickness

This repository contains the complete paper-building, proof-audit, and
numerical-falsification record for a two-period announced rescue-price model
with strategic drivers and latent Poisson supply.

The maintained correction is that an incumbent driver who waits and is
selected in period 2 receives the period-1-equivalent net payoff

\[
\delta(p_j-c),\qquad 0<\delta\le 1,
\]

whereas a fresh entrant receives the contemporaneous payoff \(p_j-c\).
Rider patience is \(\beta\), incumbent-driver patience is \(\delta\), and a
common-discount specification is the restriction \(\delta=\beta\). Discounting
changes incumbent incentives, not physical survival, entry, terminal
eligibility, or completion.

## Formal theory paper

The formal manuscript is rebuilt independently from the group-meeting note.
It uses a general-distribution equilibrium foundation, an exact uniform
no-entry design core, market-thickness results, and a surviving-incumbent plus
fresh-entry extension.  The current version is theory-only; no empirical
package is active.

- [Formal theory PDF](paper/formal/main.pdf)
- [Formal theory source](paper/formal/main.tex)
- [Formal bibliography](paper/formal/references.bib)
- [Reusable theory-manuscript prompt](prompt/formal_theory_manuscript_prompt.md)

The current paper uses the requested official Management Science
`informs3`/`blindrev` template. Superseded rendered manuscript drafts and their
unused `informs4` dependencies have been removed from the working tree; they
remain recoverable from Git history and the
`archive/pre-composition-template-20260827` protection branch. The standalone
group-meeting note remains a separate document:

- [Eight-page figure-first group-meeting note (PDF)](output/pdf/group_meeting_market_thickness.pdf)
- [Group-meeting note LaTeX source](group_meeting/group_meeting_market_thickness.tex)
- [Adversarial nearest-literature and novelty memo](literature/adversarial_literature_novelty_memo.md)
- [Proof-claim ledger](analysis/proof_claim_ledger.md)
- [Approach and counterexample registry](analysis/approach_and_counterexample_registry.md)
- [Final integration red-team](audits/incumbent_discount_final_redteam.md)
- [Numerical falsification report](analysis/incumbent_discount_numerical_report.md)

## Main results

Within anonymous symmetric independently mixed WPBE:

1. For general continuous full-support \(F,G\), cutoff behavior is endogenous:
   every equilibrium strategy is almost everywhere a pure cutoff, and the
   cutoff set is nonempty and compact.
2. Under smooth \(F,G\) and no fresh entry, a small rescue increase at any
   active flat price strictly raises completion on every nearby equilibrium
   branch.  Convex \(F\) extends same-\(p_1\) dominance globally; a concave-CDF
   counterexample shows why the shape condition matters.
3. A flat menu retains the unique cutoff \(a=p_1\), and its physical completion
   probability is independent of \(\delta\).
4. In the uniform no-entry core, every menu has a unique cutoff and the global
   policy problem reduces to a continuous one-dimensional maximum.  The local
   wedge decomposes as
   \[
   \phi(mp_1)-\delta e^{-mp_1}
   =\{\phi(mp_1)-e^{-mp_1}\}+(1-\delta)e^{-mp_1},
   \]
   separating assignment competition from incumbent impatience.
5. With surviving incumbents and fresh entrants, a small announced rescue
   strictly beats optimized flat pricing whenever at least one optimized flat
   price is below \(\beta\) and satisfies the rider-activity inequality. Strict
   failure of that inequality makes the same small perturbation exactly
   ineffective.
6. Holding either flat-failure continuation headcount or price-marginal
   capacity fixed, a larger incumbent share strictly increases first-order
   cutoff erosion in the active local region. Its marginal completion effect
   is generally nonmonotone; the two pure endpoints have a closed-form
   patience threshold.
7. With \(\gamma=0\), \(\alpha>0\), and \(\beta\ge 1/2\), the globally
   optimized announced menu strictly dominates the optimized flat payment for
   every finite \(m>0\) and every \(0<\delta\le1\).
8. Incumbent impatience changes the thin-market order. For \(\beta>1/2\),
   the gain is order \(m\) when \(\delta<1\), versus order \(m^2\) at
   \(\delta=1\). At \(\beta=1/2\), it is order \(m^3\) when \(\delta<1\),
   versus \(\alpha m^4/2048\) at \(\delta=1\).
9. For fixed positive \((\alpha,\beta)\), the thick-market rates are uniform
   over \(\delta\in(0,1]\): dynamic loss is \((\log\log m)/m\), and the gain
   over optimized flat is \((\log m)/m\).
10. In the public deterministic-\(n\) benchmark, for positive survival and an
   interior first payment, rescue is locally productive for every \(n\ge1\)
   when \(\delta<1\). At \(\delta=1\), the derivative is zero for \(n=1\) and
   positive for \(n\ge2\).

Strict single-peakedness in market thickness is false for \(\beta<1/2\)
because the optimized gain has an exact initial zero plateau. For
\(\beta\ge1/2\), strict single-peakedness and uniqueness of the globally best
thickness remain open.

## Repository layout

```text
paper/formal/ independent journal manuscript, PDF, tables, figures, and scripts
paper/        formal paper and exact INFORMS3 class/bibliography style
group_meeting/ standalone eight-page benchmark, numerical thickness, and WPBE note
figures/     extensive-form source and rendered formats
analysis/    claim ledger, counterexample registry, numerical reports
audits/      independent derivations and adversarial proof checks
code/        baseline and incumbent-discount falsification engines
literature/  adversarial nearest-literature and contribution memo
prompt/      proof-audit and theory-manuscript prompts
archive/     original theory-source foundations retained for provenance
```

The original source foundations and intermediate audits are retained so that
every correction can be traced. Redundant rendered drafts are kept in Git
history rather than duplicated in the working tree.

## Reproduce the numerical checks

Create an environment with Python 3.11+ and install the dependencies:

```bash
python -m pip install -r paper/formal/requirements.txt
```

Run all 20 regression tests:

```bash
PYTHONPATH=code python -m unittest discover -s code -p 'test_*.py' -v
```

Run the mixed-supply theorem red team:

```bash
PYTHONPATH=code python code/check_mixed_supply_theorems.py
```

Reproduce the two type-region figures in the group-meeting note:

```bash
python code/exact_one_driver_regions.py
python code/thickness_regions.py
```

Run the corrected deterministic audit:

```bash
for section in formulas roots exact thickness; do
  PYTHONPATH=code python code/run_discount_falsification.py \
    --full --section "$section"
done
```

Run `make paper`, `make figure`, or `make test` for the common build and test
targets. `make paper` aliases the maintained formal build. The repository
bundles the exact `informs3` class used by the requested Management Science
template and the bibliography style. A full TeX installation should provide
the remaining standard packages.

Regenerate and build the independent formal theory paper with:

```bash
make formal-figures
make formal
```

## Verification record

- 20/20 unit and backward-compatibility tests pass.
- The discounted scan covers 150,800 menus and 80 multiprecision root
  cross-checks, with no cutoff-multiplicity, ordering, or same-price dominance
  failure.
- 108 thickness profiles and 90 rider-patience curves produced no additional
  counterexample. These scans are falsification evidence, not proofs.
- The mixed-supply red-team script checks global flat-root enumeration, an
  active strict-improvement case, an inactive exact-zero case, the closed-form
  composition threshold, and a fully mixed nonmonotonic composition profile.
- The maintained formal paper has no unresolved references, citation errors,
  duplicate PDF anchors, or overfull boxes and is visually checked after each
  formal build.
- The current manuscript source contains no boxed-formula commands.

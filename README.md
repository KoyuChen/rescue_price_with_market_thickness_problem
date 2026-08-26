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

## Current paper

- [Management Science-formatted audited paper (PDF)](paper/announced_escalation_theory_overhaul.pdf)
- [LaTeX source](paper/announced_escalation_theory_overhaul.tex)
- [Group-meeting note on the exact benchmark and market thickness (PDF)](output/pdf/group_meeting_market_thickness.pdf)
- [Group-meeting note LaTeX source](group_meeting/group_meeting_market_thickness.tex)
- [BibTeX database](paper/announced_escalation_references.bib)
- [Adversarial nearest-literature and novelty memo](literature/adversarial_literature_novelty_memo.md)
- [Proof-claim ledger](analysis/proof_claim_ledger.md)
- [Approach and counterexample registry](analysis/approach_and_counterexample_registry.md)
- [Final integration red-team](audits/incumbent_discount_final_redteam.md)
- [Numerical falsification report](analysis/incumbent_discount_numerical_report.md)

## Main results

Within anonymous symmetric pure driver-cutoff WPBE:

1. Every announced menu admits an equilibrium. In the no-fresh-entry model,
   every menu has a unique equilibrium cutoff value.
2. A flat menu retains the unique cutoff \(a=p_1\), and its physical completion
   probability is independent of \(\delta\).
3. Active marginal rescue raises completion. The local wedge decomposes as
   \[
   \phi(mp_1)-\delta e^{-mp_1}
   =\{\phi(mp_1)-e^{-mp_1}\}+(1-\delta)e^{-mp_1},
   \]
   separating assignment competition from incumbent impatience.
4. With \(\gamma=0\), \(\alpha>0\), and \(\beta\ge 1/2\), the globally
   optimized announced menu strictly dominates the optimized flat payment for
   every finite \(m>0\) and every \(0<\delta\le1\).
5. Incumbent impatience changes the thin-market order. For \(\beta>1/2\),
   the gain is order \(m\) when \(\delta<1\), versus order \(m^2\) at
   \(\delta=1\). At \(\beta=1/2\), it is order \(m^3\) when \(\delta<1\),
   versus \(\alpha m^4/2048\) at \(\delta=1\).
6. For fixed positive \((\alpha,\beta)\), the thick-market rates are uniform
   over \(\delta\in(0,1]\): dynamic loss is \((\log\log m)/m\), and the gain
   over optimized flat is \((\log m)/m\).
7. In the public deterministic-\(n\) benchmark, for positive survival and an
   interior first payment, rescue is locally productive for every \(n\ge1\)
   when \(\delta<1\). At \(\delta=1\), the derivative is zero for \(n=1\) and
   positive for \(n\ge2\).

Strict single-peakedness in market thickness is false for \(\beta<1/2\)
because the optimized gain has an exact initial zero plateau. For
\(\beta\ge1/2\), strict single-peakedness and uniqueness of the globally best
thickness remain open.

## Repository layout

```text
paper/       current paper, PDF, bibliography, and official INFORMS style files
group_meeting/ exact benchmark, formal thickness setup, and V(m) note
figures/     extensive-form source and rendered formats
analysis/    claim ledger, counterexample registry, numerical reports
audits/      independent derivations and adversarial proof checks
code/        baseline and incumbent-discount falsification engines
literature/  adversarial nearest-literature and contribution memo
prompt/      reusable long-run multi-agent research prompt
archive/     original upload and superseded pre-discount drafts
```

The archive and intermediate audits are retained deliberately so that every
correction can be traced. The current authoritative objects are the files
linked under **Current paper**.

## Reproduce the numerical checks

Create an environment with Python 3.11+ and install the dependencies:

```bash
python -m pip install -r code/requirements.txt
```

Run all 20 regression tests:

```bash
PYTHONPATH=code python -m unittest discover -s code -p 'test_*.py' -v
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
targets. The repository bundles the official INFORMS class, bibliography
style, equation-style helper, and logo. A full TeX installation should provide
the remaining standard packages, including `newtx` and `tex-gyre`.

## Verification record

- 20/20 unit and backward-compatibility tests pass.
- The discounted scan covers 150,800 menus and 80 multiprecision root
  cross-checks, with no cutoff-multiplicity, ordering, or same-price dominance
  failure.
- 108 thickness profiles and 90 rider-patience curves produced no additional
  counterexample. These scans are falsification evidence, not proofs.
- The 30-page double-anonymous Management Science manuscript compiles without
  unresolved references, citation errors, overfull boxes, or duplicate PDF
  anchors and has been visually checked page by page.
- The current manuscript source contains no boxed-formula commands.

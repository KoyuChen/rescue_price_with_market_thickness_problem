# Copy-paste prompt: formal manuscript restart with calibration protocol

You are rebuilding a journal manuscript in operations management and applied
game theory.  Treat this as a formal-paper project, not as a group-meeting
note, slide deck, theorem memo, or cosmetic LaTeX rewrite.

## 1. Nonnegotiable separation of deliverables

The formal manuscript and the group-meeting note are different products.

- Do not edit, import, overwrite, or restyle anything under
  `group_meeting/`, its compiled PDF, or its figure-generation scripts.
- Build the formal manuscript in `paper/formal/` with its own source,
  bibliography, figures, tables, scripts, and compiled PDF.
- Preserve a recoverable Git protection branch before replacing or deleting
  earlier formal drafts. Keep original theory-source foundations, but remove
  redundant rendered drafts after the maintained paper passes all checks.
- Group-meeting conveniences, such as compressed derivations, type-region
  teaching figures, conversational headings, or theorem-free exposition, do
  not determine the structure of the formal paper.

Before editing, create a Git protection branch at the current clean commit and
work on a new branch named `formal-restart-calibration`.  Make one coherent
local commit only after all checks pass.  Never push unless a verified remote
and authorization are available.

## 2. Style references

Use exactly the official Management Science Overleaf template at
<https://www.overleaf.com/latex/templates/template-for-management-science-journal/bjpqpdqhbshy>:

```latex
\documentclass[mnsc,blindrev]{informs3}
\OneAndAHalfSpacedXI
\TheoremsNumberedThrough
\ECRepeatTheorems
\EquationsNumberedThrough
\MANUSCRIPTNO{}
```

Put the main references after the conclusion, followed by `\ECSwitch` and
`\ECHead{Proofs and Additional Material}`. Do not substitute `informs4`,
rename another class as `informs3`, or import obsolete equation-validation
helpers.

Read the following reference papers before drafting:

1. `Slide_or_Feed_unblinded.pdf`;
2. `Diffusion_nonblinded.pdf`.

Use them only as structural and editorial references.  Do not copy their
language, substantive claims, data, equations, references, or idiosyncratic
formatting.  Extract the conventions they share:

- a self-contained title page, abstract, keywords, introduction, literature
  review, formal model/analysis, quantitative or empirical implementation,
  managerial implications, conclusion, references, and ordered appendices;
- an introduction that moves from the operational problem to the economic
  mechanism, results, contributions, and roadmap;
- a literature review organized by research stream, explaining what the
  closest individual papers do before stating the exact remaining difference;
- a clean transition from analytical model to estimation/calibration and
  counterfactual policy analysis;
- table titles above tables, figure captions below figures, `booktabs` without
  vertical rules, self-contained notes, panel labels, consistent units, and
  references in the journal's author--year style;
- proofs in the appendix in the same order as the corresponding main-text
  results.

The resulting paper should read like a submitted Management Science or M&SOM
manuscript.  Avoid rhetorical questions, self-questioning headings, defensive
novelty language, audit jargon, and theorem inventories in the abstract or
introduction.

Open the introduction with a short institutional hook based on two to four
verified news or official-platform facts. Prefer Reuters, AP, FT, WSJ, major
regulators, or first-party platform documentation. Each fact must map directly
to rejection, driver pay, supply scarcity, incumbent persistence, or new entry.
Do not claim that a reported platform already uses the paper's exact
same-request announced-rescue contract unless the source establishes that
timing. Add every source to the author--year bibliography with verified title,
author, date, and stable URL.

## 3. Research question and economic narrative

Study a platform that publicly commits to a same-request payment menu

\[
0\le p_1\le p_2\le1,
\]

where `p_1` is paid following immediate acceptance and `p_2` is available only
after universal first-window rejection.  The economic tension is that a
higher rescue payment increases terminal coverage but can induce incumbent
drivers to wait.

The central information mechanism is screening history.  Expected incumbent
thickness `m` is public, but the realized incumbent count is latent.  Universal
rejection both triggers continuation and reveals that the remaining incumbent
pool has passed a first-period rejection screen.  The value of second-window
supply therefore depends on composition and history, not only its expected
size.

Use `p_1,p_2` everywhere.  Never introduce `(p,q)` as an alias.  A generic
flat-payment optimizer may be denoted `p_F`, but do not recycle `p` as the
first component of a two-price menu.

## 4. Canonical primitives and timing

Define all primitives once, with domains and empirical counterparts:

- `m>0`: public expected incumbent thickness;
- `N^I~Pois(m)`: latent realized incumbent count;
- `alpha in [0,1]`: probability a rejected incumbent remains eligible in the
  second response window;
- `gamma>=0`: fresh-entry intensity multiplier, so
  `N^E~Pois(gamma*m)`;
- `beta in (0,1)`: rider continuation factor;
- `delta in (0,1]`: incumbent waiting-payoff factor;
- `F`: primitive driver-cost distribution;
- `G`: primitive rider-value distribution.

The baseline uniform model has driver costs and rider values on `[0,1]`.
State exactly which results rely on uniformity.

Write the timing in full prose, even if an extensive-form figure is also used:

1. the platform observes `m` and commits to `(p_1,p_2)`;
2. the rider observes private value and chooses whether to post;
3. the latent incumbent pool realizes;
4. incumbents simultaneously accept `p_1` or wait;
5. if at least one accepts, one is selected and the request completes;
6. otherwise universal rejection is publicly observed;
7. the rider chooses abandon, repeat `p_1`, or activate `p_2`;
8. conditional on continuation, rejected incumbents independently survive
   with probability `alpha`, while a fresh unscreened pool with mean
   `gamma*m` enters;
9. available drivers accept the active terminal payment or reject, followed by
   assignment or expiration.

An incumbent selected in period 2 earns the period-1-equivalent payoff
`delta*(p_j-c)`.  A fresh entrant made no earlier waiting decision and earns
the contemporaneous payoff `p_j-c`.  Discounting changes incumbent incentives,
not physical survival, entry, eligibility, or completion.

At terminal payment `p_j`, the expected eligible-driver intensity is

\[
m\{\alpha[p_j-a]^++\gamma p_j\}.
\]

Explain explicitly why the first term is a screened, truncated incumbent
pool and the second term is an unscreened entrant pool.  Do not collapse them
to one continuation-supply scalar.  The global analytical solution may impose
`gamma=0`; with `alpha<1` and `gamma>0`, state the local equilibrium theorem,
the activity-gated optimized-flat dominance theorem, and the composition
results separately. Treat claims beyond those proved regions as numerical
evidence rather than as global implications.

## 5. Equilibrium and policy objects

Use weak perfect Bayesian equilibrium, restricted to anonymous symmetric pure
first-period driver cutoffs.  State strategies, beliefs, Bayes consistency,
sequential rationality, Palm conditioning, assignment, off-path conventions,
and tie-breaking.  Do not call the concept subgame-perfect equilibrium, and do
not describe a minimum within the maintained cutoff class as a worst case over
all PBE.

For a candidate cutoff `a`, derive:

- first-period coverage and assignment probability;
- the failure posterior;
- surviving-incumbent and fresh-entrant terminal intensities;
- rider post, abandon, repeat, and rescue regions;
- incumbent accept-now and wait payoffs;
- cutoff indifference and boundary conditions;
- unconditional completion on every equilibrium branch.

Define the optimized policy values cleanly at a common market thickness:

\[
M_R^*(m)=\text{maximum completion under an announced rescue menu},
\]

\[
M_F^*(m)=\text{maximum completion under a flat payment},
\]

and

\[
V(m)=M_R^*(m)-M_F^*(m).
\]

Immediately explain that `100*V(m)` is the percentage-point completion gain
from allowing an optimally designed rescue menu rather than an optimally
chosen flat payment while holding the same `m` fixed.  It is not the marginal
value of adding drivers and should not be called “the value of market
thickness.”

Never state strict single-peakedness or uniqueness of the maximizing thickness
unless proved.  Continuity, endpoint vanishing, and existence of a finite
positive maximizer do not imply a unique peak.

## 6. Target manuscript architecture

Use the following main-text structure unless a mathematically necessary change
is documented:

1. **Introduction**
   - operational problem and rescue/waiting tension;
   - latent realized supply and universal-rejection screening;
   - surviving incumbents versus fresh entrants;
   - principal equilibrium and policy results in economic language;
   - a narrow contribution paragraph;
   - roadmap.

2. **Literature Review**
   - dynamic search auctions and procurement clocks;
   - announced pricing and strategic waiting;
   - platform bonuses, dispatch, and strategic rejection;
   - latent supply, screening, and market thickness;
   - empirical platform matching and structural estimation.

3. **Institutional Setting and Empirical Requirements (Protocol Only)**
   - exact operational timing;
   - payment incidence;
   - model-to-data measurement map;
   - identification gates;
   - an explicit statement that no estimates or empirical results are reported
     before the required data exist.

4. **Model**
   - primitives table;
   - detailed timing and information;
   - equilibrium class and beliefs;
   - policy classes and performance measures.

5. **Equilibrium under an Announced Menu**
   - Poisson competition and failure posterior;
   - rider continuation;
   - driver cutoff-WPBE;
   - completion and flat benchmark.

6. **Extension: Surviving Incumbents and Fresh Driver Entry**
   - `alpha<1`, `gamma>0` mixed continuation pool;
   - screening-history interpretation;
   - local rescue theorem and its activity condition;
   - exact boundary between proof and numerical evidence.

7. **Global Menu Design without Fresh Entry**
   - unique cutoff geometry;
   - fixed-`p_1` optimization over `p_2`;
   - one-dimensional global policy problem;
   - optimized rescue versus optimized flat;
   - rider-patience threshold.

8. **Market Thickness and Mechanism Decomposition**
   - clean definition of `V(m)`;
   - thin and thick endpoint economics;
   - finite positive maximizer without a shape theorem;
   - public-supply benchmark;
   - theoretical numerical illustration clearly labeled nonempirical.

9. **Planned Empirical Calibration and Counterfactual Design**
   - parameter/status ledger;
   - minimum-distance or simulated-moments criterion;
   - targeted versus validation moments;
   - future observed, flat, announced-rescue, and no-anticipation comparisons;
   - uncertainty propagation;
   - every table title marked “design only; no estimates” until populated.

10. **Managerial Interpretation and Institutional Scope**
    - rider patience;
    - intermediate thickness;
    - why screened survivors and unscreened entrants cannot be pooled;
    - transfer, objective, equilibrium-class, and fresh-entry scope.

11. **Conclusion**
    - mechanism;
    - global no-entry result and `V(m)`;
    - survival-and-entry extension;
    - empirical data gates and future calibration.

Appendices should contain proofs in main-text order, numerical algorithms and
root checks, and the empirical reproducibility contract.

## 7. Literature review and novelty boundary

Search primary sources and verify bibliographic metadata before citing.  The
review must directly discuss the strongest overlapping papers, including at
least:

- McAfee and McMillan (1988) and Crémer, Spiegel, and Zheng (2007) on search
  mechanisms and retained incumbents/new bidders;
- Lee and Li (2023) on committed dynamic search with strategic incumbents,
  new entrants, and a screened old-bidder distribution;
- Correa, Montoya, and Thraves (2016) on contingent preannounced pricing;
- Wu et al. (2022) on multistage platform bonuses;
- Loertscher, Muir, and Taylor (2022) and Zhao, Papier, and Teo (2024) on
  market thickness;
- Zhang et al. (2026) and other directly relevant platform structural work on
  driver acceptance, rider choice, or market density.

For each stream, write connected prose that answers:

1. What is the closest paper's decision problem and information structure?
2. Which part of the present mechanism already exists there?
3. What exact joint structure remains different here?

Do not claim that any of the following is new by itself: a two-period price
path, precommitment, strategic waiting, Poisson supply, hidden realized group
size, fresh entry, a screened-incumbent/unscreened-entrant mixed pool, or an
interior market-thickness optimum.

Use a safe contribution statement such as:

> We build on dynamic search auctions, strategic waiting, and multistage
> platform bonuses.  Our analysis focuses on a different institutional
> combination: an anonymous same-request posted-payment menu announced before
> driver action; public expected but latent realized incumbent supply;
> universal rejection that updates beliefs about competition and costs; a
> private rider continuation choice; and a continuation pool containing
> selectively retained incumbents and fresh entrants.  We characterize the
> resulting cutoff-WPBE and compare optimized rescue and flat policies in
> terms of unconditional request completion.

Avoid “first,” “novel,” or an exhaustive “none of the literature combines
A+B+C” claim unless a documented search establishes it.

## 8. Empirical calibration protocol and stop conditions

Do not fabricate a dataset, descriptive statistic, estimate, standard error,
model fit, or counterfactual.  If observed request-level data are unavailable,
write a real empirical protocol with visible placeholders and label every
entry `DATA REQUIRED`.

The minimum empirical package is:

- request-level `p_1,p_2`, disclosure timestamps, and assignment mechanism;
- first- and second-window eligible/exposed driver IDs;
- accept, reject, timeout, and assignment timestamps;
- rider post, abandon, repeat, rescue, and cancellation events;
- a public pre-decision thickness signal or a defensible measurement model;
- persistent driver IDs that distinguish screened surviving incumbents from
  fresh entrants;
- the experiment or identification protocol and payment incidence.

The decisive gate is announcement timing.  If `p_2` was not displayed and
credibly committed before first-window incumbent decisions, the data cannot
identify the strategic anticipation channel.  Static price variation may
discipline contemporaneous acceptance or a flat/no-anticipation benchmark,
but it does not identify `delta`.

Pre-specify a criterion of the form

\[
\widehat\theta\in\arg\min_{\theta\in\Theta}
[\widehat g-g(\theta)]^{\mathsf T}W[\widehat g-g(\theta)],
\]

where each evaluation of `g(theta)` re-solves all relevant cutoff-WPBE roots
before aggregating moments.  Target posting, first-window acceptance,
universal rejection, abandon/repeat/rescue, incumbent survival, fresh entry,
terminal acceptance, and unconditional completion.  Separate targeted and
holdout moments, report parameter bounds and numerical tolerances, and
re-estimate within each bootstrap draw.

The initial empirical implementation should maintain the model's common
primitive cost distribution.  Allowing entrant and incumbent distributions to
differ is a separately derived robustness extension, not a relabeling of the
current equilibrium formulas.

## 9. Figures and tables

The formal paper should contain only figures that support the main economic
argument:

- one compact extensive-form/timing figure;
- a multi-panel theoretical figure for `p_1^*(m)`, `p_2^*(m)`,
  `M_R^*(m)`, `M_F^*(m)`, and `V(m)`;
- a selected-thickness table for `m=1,5,10,20`;
- empirical measurement, parameter, fit, and counterfactual tables marked as
  design-only placeholders until real data are available.

Every numerical figure must state the assumed parameters, units, solver, and
whether the pattern is a theorem, numerical evidence, or conjecture.  Do not
reuse the group-meeting type maps as formal-main-text figures unless they
answer a specific mechanism or calibration question.

## 10. Repository artifacts

Create or maintain:

```text
paper/formal/main.tex
paper/formal/references.bib
paper/formal/main.pdf
paper/formal/figures/
paper/formal/tables/
paper/formal/scripts/
empirical/README.md
empirical/data_dictionary.md
empirical/identification_ledger.csv
empirical/config/
empirical/src/
empirical/tests/
empirical/output/figures/
empirical/output/tables/
literature/adversarial_literature_novelty_memo.md
```

Raw or restricted empirical data must remain outside Git.  Synthetic fixtures
may test schemas, identifiers, event order, and incumbent/entrant
classification, but may never be described as empirical evidence.

## 11. Final quality gates

Before committing:

1. compile the formal PDF from a clean LaTeX build;
2. regenerate all theoretical figures and tables from code;
3. run the complete existing mathematical test suite;
4. run empirical schema and timing tests in synthetic mode;
5. check for undefined citations/references, duplicate anchors, overfull boxes,
   stale equation references, and unexplained notation;
6. render and inspect every PDF page for clipping, drift, illegible figures,
   empty pages, and misleading placeholder tables;
7. verify that no `(p,q)` alias remains and every empirical result is visibly
   unobserved;
8. verify that `group_meeting/**`, its PDF, and its supporting scripts are
   byte-for-byte unchanged from the protection branch;
9. update the adversarial literature memo with the strongest novelty threats
   and the narrowed contribution boundary;
10. commit the complete restart on `formal-restart-calibration` and report the
    branch, commit hash, tests, PDF page count, and absence of a configured
    remote if applicable.

The final handoff must distinguish four evidentiary levels:

- proved analytical result;
- reproducible theoretical numerical evidence;
- conjecture or open shape property;
- empirical design placeholder with no observed evidence.

Do not stop at a plausible draft.  Stop only when the formal manuscript,
bibliography, figures, empirical contract, literature memo, compilation,
tests, visual inspection, and Git state agree with one another.

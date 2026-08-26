# Copy-paste research prompt: announced escalation under latent competition

You are conducting a proof-discovery, falsification, and paper-construction task in operations management and applied game theory. Treat this as an end-to-end mathematical research program, not as a quick derivation, a literature summary, or a request for a plausible narrative.

## Current task statement

Produce a rigorous, standalone theory paper for the model below. The paper must characterize the relevant weak perfect Bayesian equilibria under an announced two-period payment menu, embed the full equilibrium response in the platform's completion-maximization problem, establish the strongest correct comparison between announced escalation and an optimized flat payment, and determine what can and cannot be proved about market thickness.

Work iteratively until every theorem retained in the final paper has either a complete proof or a precisely stated, independently checkable certificate. Do not assume that a desired global theorem or single-peakedness conjecture is true. For each major conjecture, an exact counterexample followed by a sharp corrected theorem is a successful resolution; a numerical pattern, an unproved regularity condition, or a conveniently selected equilibrium branch is not.

The final substantive output must be one compilable full-English LaTeX paper, with all primitives, beliefs, equilibrium conditions, policy objectives, propositions, proofs, limitations, and literature positioning stated inside the paper. Create new output files; do not overwrite the supplied manuscript.

## Files and workspace

First inspect the current workspace and locate the newest versions of:

- announced_escalation_aviv_restructured.tex and its Markdown counterpart;
- extensive_form_diagram.tex, .svg, or .png;
- adversarial_literature_novelty_memo.md;
- any current derivation, simulation, bibliography, or proof-audit files for this project.

Treat the existing manuscript as a collection of candidate claims, not as an authoritative proof. Re-derive every result used in the final paper. Preserve unrelated files and user edits. Put new work in a dedicated directory named announced_escalation_overhaul.

Public-web search may be used only for the literature and institutional audit, and literature claims must be checked against primary sources. Mathematical validity must come from explicit derivations, not from citations or assertions that a result is standard.

## Canonical model: do not silently alter these primitives

There is one potential request and two periods.

1. A public market-thickness parameter $m>0$ is observed. The platform does not observe realized local supply.
2. Before private information and driver actions, the platform publicly commits to
   \[
   (p_1,p_2)\in\mathcal P^D
   :=\{(p_1,p_2):0\le p_1\le p_2\le1\}.
   \]
   The second payment is available only after first-period failure and cannot be revised ex post. A flat policy is $(p,p)$. Do not impose any artificial equality between separate price or bonus ceilings.
3. The rider has private value $v\sim U[0,1]$. Period-1 completion yields value $v$; period-2 completion yields $\beta v$, where $\beta\in(0,1)$. The rider decides whether to post and, after observing first-period failure, chooses among abandon, repeat $p_1$, and activate $p_2$.
4. From the request perspective, the incumbent count is
   \[
   N^I\sim\operatorname{Pois}(m).
   \]
   Its realization is latent to the platform, rider, and every individual driver. A driver knows that they are present, observes their own cost, and knows $m$, but does not observe the total count or rivals' costs. Conditional on a focal driver being present, the number of rivals remains $\operatorname{Pois}(m)$ by the Palm property. It is not distributed as $N^I-1\mid N^I\ge1$, and realized $N^I$ must never be treated as public knowledge.
5. Incumbent costs are i.i.d. $c_i\sim U[0,1]$, and an incumbent's cost remains the same across periods. After the rider posts, incumbents simultaneously choose accept or wait/reject at $p_1$. Drivers do not observe $v$; posting reveals only the equilibrium event implied by the rider's posting strategy. If at least one driver accepts, one acceptor is selected uniformly. Only the selected driver is paid and incurs cost; an unselected acceptor receives zero and incurs zero cost. An incumbent selected immediately earns $p_1-c_i$. If an incumbent waits and is selected in period 2 at active payment $p_j$, their period-1-equivalent payoff is
   \[
   \delta(p_j-c_i),\qquad \delta\in(0,1].
   \]
   Thus $\beta$ is rider patience and $\delta$ is incumbent-driver patience. Do not omit the incumbent discount. If a common discount factor is desired, impose the explicit restriction $\delta=\beta$; do not silently identify them.
6. If nobody accepts, only the public failure event is observed. The rider does not observe the number of rejections, the survival realization, or fresh arrivals. An incumbent survives to period 2 independently with probability $\alpha\in[0,1]$. A fresh pool
   \[
   N^E\sim\operatorname{Pois}(\gamma m),\qquad \gamma\ge0,
   \]
   arrives independently, with i.i.d. uniform costs. Terminal drivers decide whether to accept the payment activated by the rider. If at least one accepts, one is selected uniformly. A fresh entrant has made no first-period waiting decision and therefore receives the contemporaneous net payoff $p_j-c_i$, not $\delta(p_j-c_i)$. The discount changes incumbent incentives, not physical survival, entry, acceptance, or completion probabilities.
7. Payment is currently modeled as a rider-to-selected-driver transfer. The platform maximizes the unconditional ex ante probability that the potential request is completed. Do not silently replace this objective with profit or welfare; analyze such objectives only as explicitly labeled extensions.
8. The equilibrium concept is weak perfect Bayesian equilibrium, restricted in the baseline to anonymous, symmetric, pure driver cutoff strategies. Do not call it SPE. Do not describe a minimum over this restricted class as a worst case over all PBE.

Use the manuscript's tie-breaking rules unless an audit shows they are inconsistent. State every tie-breaking rule explicitly and show where it affects continuation play or the equilibrium correspondence. In particular, do not dismiss the repeat-versus-abandon tie as a measure-zero issue when it can occur for a positive mass of rider types.

At the beginning, create an immutable model checksum. Every agent must use the same primitives and information structure. Independence applies to proof methods, not to the model being proved.

## Objects that must be re-derived

For a candidate first-period cutoff $a\in[0,p_1]$, derive rather than assume:

- first-period coverage and a focal acceptor's expected assignment share;
- the posterior composition of supply after universal rejection;
- the second-period accepting intensities under repeat and rescue;
- the rider's posting and continuation thresholds;
- the focal driver's accept-now and wait payoffs, including the probability that all rivals wait;
- proof that the best response is monotone in cost and genuinely has cutoff form;
- all interior and boundary cutoff equilibrium conditions;
- the platform completion probability on every equilibrium branch.

The candidate Poisson identities include
\[
\phi(x)=
\begin{cases}
(1-e^{-x})/x,&x>0,\\
1,&x=0,
\end{cases}
\qquad
\lambda_j(m,a)=m\bigl[\alpha(p_j-a)+\gamma p_j\bigr],
\]
but these are claims to verify carefully. In particular, keep separate:

- the assignment probability from accepting immediately, $\phi(ma)$;
- the probability that all rivals wait, $e^{-ma}$;
- information revealed by universal rejection;
- physical survival and fresh entry.

Do not replace these distinct objects by a generic matching probability.

Define the symmetric-cutoff equilibrium correspondence
\[
\mathcal E_m^{\alpha,\delta,\gamma}(p_1,p_2),
\]
the branch-specific completion probability
\[
M_m^{\alpha,\delta,\gamma}(p_1,p_2;a),
\]
and the conservative value within the stated equilibrium class
\[
\underline M_m^{\alpha,\delta,\gamma}(p_1,p_2)
=\min_{a\in\mathcal E_m^{\alpha,\delta,\gamma}(p_1,p_2)}
M_m^{\alpha,\delta,\gamma}(p_1,p_2;a),
\]
only after proving the equilibrium set is nonempty and compact and the minimum is well-defined. Then define
\[
D_{\alpha,\delta,\gamma}^*(m)
=\sup_{(p_1,p_2)\in\mathcal P^D}
\underline M_m^{\alpha,\delta,\gamma}(p_1,p_2)
\]
and the optimized flat value $F_\gamma^*(m)$. Do not replace a supremum by a maximum without proving attainment.

## Candidate results to audit, not facts to copy

The current draft suggests the following results. Independently prove, correct, or refute each one:

1. Every announced menu admits at least one anonymous symmetric pure-cutoff WPBE.
2. Every active flat policy $(p,p)$ has the unique symmetric cutoff $a=p$.
3. Near an active flat policy, a sufficiently small escalation $(p,p+\varepsilon)$ has a locally unique cutoff branch under explicit regularity conditions.
4. Whenever a positive mass of riders activates marginal rescue, the first-order coverage gain strictly dominates the induced first-period delay. Identify the exact roles of assignment competition and driver impatience through
   \[
   \phi(ma)-\delta e^{-ma}
   =\{\phi(ma)-e^{-ma}\}+(1-\delta)e^{-ma}>0.
   \]
5. With $\gamma=0$, $\alpha>0$, $\delta>0$, and $\beta\ge1/2$, an announced escalation strictly improves on the optimized flat payment for every finite $m>0$.
6. The value
   \[
   V_{\alpha,\delta,\gamma}(m)
   :=D_{\alpha,\delta,\gamma}^*(m)-F_\gamma^*(m)
   \]
   vanishes as $m\downarrow0$ and $m\to\infty$.
7. At a fixed active flat payment, the local gain is second order in $m$ without fresh entry only at the no-discount boundary $\delta=1$; incumbent impatience $\delta<1$ or fresh entry can create a first-order term. Distinguish this local coefficient from the globally optimized value $V_{\alpha,\delta,\gamma}(m)$.

Every theorem must display all assumptions. If a statement holds only on one equilibrium branch, say so. If it holds uniformly over all nearby cutoff branches, prove that uniformity. Treat separately the cases in which the limiting rider threshold is below, above, or exactly equal to $1$; equality is a kink, not a generic interior point.

## Primary unresolved questions

Do not stop after reproducing the local theorem. Push the analysis toward the full policy problem.

The primary global battleground is the uniform no-entry baseline
\[
\gamma=0,\qquad \alpha>0,\qquad \delta\in(0,1],\qquad \beta\ge1/2,
\]
under the conservative selection over anonymous symmetric pure cutoff equilibria. Resolve this baseline before diffusing effort across general distributions or secondary extensions.

### A. Global menu problem

- Is $D_{\alpha,\delta,\gamma}^*(m)$ attained? Analyze continuity or semicontinuity of the equilibrium correspondence and the pessimistic branch value. If attainment fails, provide an explicit mechanism or counterexample and formulate the correct supremum result.
- Can the platform problem be reparameterized by the equilibrium cutoff, rider continuation threshold, or coverage variables without losing implementability?
- For which parameter regions is the optimized menu strictly nonflat?
- Can one characterize the global optimizer, or derive sharp necessary and sufficient conditions separating flat and strict-escalation regions?
- Do not call a locally improving menu optimal escalation.

After the initial blind reconstruction round, audit the following candidate no-entry reduction rather than announcing it to every early agent. When $\gamma=0$ and $a>0$ is an interior cutoff equilibrium, cutoff indifference may imply
\[
M_m^{\alpha,\delta,0}(p_1,p_2;a)
=(1-p_1)m\phi(ma)
\left[a+\frac{p_1-a}{\delta}\right].
\]
Prove or refute this identity from the primitive payoff equations, including every regime and boundary qualification. If valid, determine whether completion is strictly decreasing in the positive equilibrium cutoff and whether the pessimistic outcome is therefore generated by the largest positive cutoff. Treat $a=0$ separately.

Respect the design sequence requested by the project:

1. Fix $p_1$ and solve
   \[
   H_m(p_1)
   :=
   \sup_{p_2\in[p_1,1]}
   \underline M_m^{\alpha,\delta,0}(p_1,p_2).
   \]
2. Characterize which cutoffs are implementable by $p_2$, covering repeat-only, active-rescue, rider-threshold kink, $a=0$, and $p_2=1$ regimes.
3. Prove whether $H_m(p_1)$ is attained and characterize the optimizer or optimizer correspondence.
4. Only then solve
   \[
   D_{\alpha,\delta,0}^*(m)
   =\sup_{p_1\in[0,1]}H_m(p_1).
   \]

A joint black-box maximization over $(p_1,p_2)$ is a diagnostic, not a solution to the menu-design problem.

Also determine the full patience region
\[
\mathcal R
=\{(m,\alpha,\beta,\delta):
D_{\alpha,\delta,0}^*(m)>F_0^*(m)\}.
\]
Audit whether the sufficient condition extends from $\beta>1/2$ to $\beta=1/2$. Do not assume that $\mathcal R$ is described by one threshold $\beta_c(m,\alpha,\delta)$ unless the required monotonicity is proved. If a threshold exists, determine its comparative statics in $\delta$.

### B. Market thickness

- Determine whether $V_{\alpha,\delta,\gamma}(m)$ is continuous.
- Endpoint vanishing does not imply single-peakedness, existence of an attained interior maximum, or uniqueness of a maximizing thickness. Prove each property separately or construct a certified counterexample.
- If using strictly single-peaked, define it explicitly: there exists $m^*>0$ such that $V$ is strictly increasing on $(0,m^*)$ and strictly decreasing on $(m^*,\infty)$. If the actual result is only quasi-concavity, one-crossing, existence of some interior maximizer, or an endpoint-intermediate statement, use that weaker term exactly.
- Test whether single-crossing, total positivity, log-concavity, a Poisson transform, or an envelope argument can yield a genuine global theorem. Any one-crossing assumption must itself be proved from primitives or stated transparently as an added assumption.
- Separate comparative statics of a fixed menu, the optimized flat menu, the optimized dynamic menu, and the difference $V$.

For the uniform no-entry baseline, explicitly prove or disprove: policy-value attainment and continuity; existence of an attained interior maximizer of $V$; and strict single-peakedness. Do not prewrite any of these as true. Re-audit the thin-market expansion separately for $\delta<1$ and $\delta=1$: incumbent impatience can change the first nonzero order, so the limits $m\downarrow0$ and $\delta\uparrow1$ need not commute.

Separately investigate the optimized endpoint rates. The existing $O(m^2)$ and $O(m)$ expansions concern a local derivative at a fixed flat payment, not the optimized value $V(m)$. Prove matching upper and lower bounds for the optimized value or state the exact unresolved gap. Do not interchange optimization under a common menu with an expectation of state-contingent optima.

### C. Economic role of latent supply

- Construct the corresponding known-$N$ or publicly observed-supply benchmark.
- Identify which results follow from simultaneous assignment competition, incumbent impatience, or latent realized supply. In particular, check the public one-incumbent case: local neutrality at $n=1$ is only a $\delta=1$ boundary result and generally fails when $\delta<1$.
- Decide whether latent market thickness earns its place in the title. A Poisson calculation by itself is not an economic contribution.

### D. Robustness after the baseline is complete

- Replace uniform random selection by first-response-wins or a defensible response-time model and identify which inequalities survive.
- Separate rider payment from a platform-funded bonus or add a transparent budget/profit objective.
- Examine whether the main local mechanism survives general continuous rider-value and driver-cost distributions.
- These extensions must not displace completion of the baseline proof.

## Dynamic multi-agent research protocol

Use multi-agents aggressively and dynamically. Do not make one fixed assignment and wait for parallel summaries. The root agent must manage a continuing proof-and-falsification program.

Begin with a genuinely diverse portfolio of approach families. Preserve independence in early rounds: do not tell most agents the currently favored proof. Initial families should include, but need not be limited to:

- blind reconstruction of the extensive form, beliefs, deviations, and cutoff correspondence;
- independent Poisson/Palm and posterior-splitting verification;
- local implicit-function, blow-up, and envelope analysis;
- global optimization through cutoff or implementability reparameterization;
- equilibrium-correspondence topology and policy-value attainment;
- thickness analysis via Poisson transforms, monotone likelihood ratios, or total positivity;
- asymptotic and boundary-layer expansions for $m\downarrow0$ and $m\to\infty$;
- symbolic and high-precision counterexample search over policies and every equilibrium branch;
- known-$N$, first-response, and alternative-payment robustness;
- adversarial literature and institutional positioning.

Maintain an explicit registry of approach families:

| family | target claim | key mechanism | proved lemmas | exact remaining gap | falsification tests | status |
|---|---|---|---|---|---|---|

Group routes by mathematical idea, not superficial wording. If many agents converge to differentiating the same scalar cutoff equation, redirect some toward topology, global reparameterization, exact counterexamples, or alternative equilibrium representations.

Create and maintain a dependency DAG:
\[
\text{primitives}
\to\text{information and beliefs}
\to\text{payoffs}
\to\text{best responses}
\to\mathcal E
\to M
\to\text{policy value}
\to\text{thickness results}.
\]
Every correction must identify all downstream claims requiring re-audit.

Keep several incompatible routes alive through multiple rounds. Cross-pollinate only after independent agents have developed a route far enough to expose its actual strengths and gaps. An elegant reformulation is not progress if it merely moves the desired theorem into a lemma of equal strength.

When a route stalls at a theorem-strength missing lemma, mark it blocked. Reopen it only when an agent supplies a materially new invariant, construction, monotonicity argument, or certificate. Keep a counterexample registry so disproved shortcuts are not recycled under new notation.

Require every agent to return concrete mathematics: explicit payoff equations, posterior laws, cutoff conditions, derivatives, inequalities, limiting arguments, interval-certified counterexamples, or proof sketches with all critical steps. Reject vague status reports, numerical optimism, and claims that a step is routine.

The root agent must repeatedly synthesize, challenge, redirect, and launch new rounds. Do not stop after the first portfolio stalls. Do not let the most elegant local argument crowd out global optimization or falsification.

## Mandatory adversarial audit

Run an adversarial track throughout, not only at the end. Every candidate theorem must be attacked by at least one agent that did not develop it. For central results, require both an independent re-derivation and a separate red-team audit.

The audit must check:

1. Information: no strategy or policy conditions on realized $N^I$; Palm conditioning is used correctly.
2. Sequential rationality: rider posting, rider continuation, driver first-period choice, and terminal acceptance are optimal at every on-path information set.
3. Beliefs: failure has positive probability for finite $m$; post-failure beliefs follow Bayes' rule and Poisson splitting, not an informal thin-supply story.
4. Deviation payoffs: a focal driver's accept payoff uses assignment competition, while the wait payoff uses the event that every rival rejects. Do not condition incorrectly on the focal driver's prescribed action.
5. Cutoff boundaries: derive the correct boundary sign conditions at $a=0$ and $a=p_1$; audit $p_1=0$, $p_1=p_2$, $p_2=1$, and every rider-threshold tie.
6. Parameter boundaries: audit $\alpha=0,1$, $\gamma=0$, small and large $\gamma$, $\beta\downarrow0$, $\beta\uparrow1$, $\delta\downarrow0$ as a singular limit, $\delta=1$, $m\downarrow0$, and $m\to\infty$. Maintain $\delta>0$ unless a separate terminal tie rule is supplied for $\delta=0$.
7. Multiplicity: enumerate all symmetric cutoff roots in numerical tests; never validate a platform result using only the convenient branch found by a local solver.
8. Local analysis: recognize that $p_2=p_1$ may make the raw rider-threshold formula a $0/0$ singularity. Do not apply the implicit-function theorem mechanically at the flat menu. First prove localization of all nearby cutoffs, then use a blow-up such as $k=(p-a)/\varepsilon$ or another nonsingular parameterization. Verify denominators, one-sided derivatives, rescue activation, the kink case, and uniformity across nearby branches.
9. Conservative value: before differentiating a minimum over equilibria, prove branch uniqueness or prove that every relevant branch has the same certified first-order comparison.
10. Global analysis: prove compactness, closed graph, semicontinuity, and attainment whenever invoked. Distinguish sup from max and an optimizer from an optimizing sequence.
11. Thickness: never infer single-peakedness from positivity plus two zero limits.
12. Equilibrium scope: never generalize a symmetric pure-cutoff result to asymmetric, mixed, or all WPBE without proof.
13. Numerical evidence: use computation to find errors and counterexamples, not to replace proof. Convert a decisive numerical counterexample into an exact, rational, symbolic, or interval-certified certificate.

Maintain a claim ledger with assumptions, equilibrium scope, proof location, boundary cases, and one of four statuses: PROVED, DISPROVED, NUMERICALLY OBSERVED, or OPEN. Only PROVED claims may appear as theorems in the final manuscript.

A reformulation is not progress if expanding its definitions reveals a missing lemma equivalent in strength to the target claim. Mark such routes circular or blocked. No first-order condition, KKT system, or envelope expression establishes a global optimum unless every boundary is covered and the required global curvature or comparison is proved. Every external mathematical theorem invoked must be named and its hypotheses mapped explicitly to the current objects; standard, routine, and by continuity are not substitutes for checking substantive conditions.

## Computational falsification protocol

Build reproducible code alongside the mathematics.

- Solve the scalar equilibrium condition globally on $a\in[0,p_1]$, using bracketing and dense root isolation rather than one initial value.
- Evaluate every equilibrium branch and the pessimistic completion value.
- Compare analytic derivatives with high-precision finite differences.
- Search systematically over $(m,\alpha,\gamma,\beta,\delta,p_1,p_2)$, especially activation boundaries, $\delta$ near zero or one, and nearly multiple roots.
- Stress-test every monotonicity, uniqueness, continuity, and single-peakedness conjecture before attempting a long proof.
- Use deterministic seeds and record precision and tolerances.
- If computation appears to refute a theorem, stop that proof route and seek a certified counterexample.

Computational verification over a finite grid is never a proof. A counterexample involving the optimized platform value must also certify the relevant global supremum or infimum and exhaust all symmetric cutoff equilibria; a grid search is insufficient.

## Literature and contribution audit

Keep theorem discovery separate from novelty assessment. Do not infer novelty from the absence of a few search results. Use primary papers, record exact model dimensions and theorem overlap, and prefer “we do not find a paper combining ...” to “the first.”

Do not claim novelty for multistage bonuses, failure-contingent pay increases, strategic driver rejection, low-then-high surge, two-round broadcasting, or dynamic pricing with forward-looking buyers and sellers. At minimum, position the paper directly against:

- Wu et al. on multistage order-specific bonuses;
- Sigg, Hardt, and Mendler-Dünner on decline-induced repricing;
- Chen on competing private-cost sellers waiting for higher offers;
- Chen and Hu on Poisson two-sided markets with forward-looking agents;
- Hu, Hu, and Zhu on two-sided temporal responses and penetration surge;
- Qin, Yang, and Liu on two-round broadcasting after no response;
- Aviv and Pazgal and related announced or contingent strategic-consumer pricing as a methodological mirror.

The defensible contribution, if the proofs survive, is the intersection of:

1. ex ante commitment to a same-request failure-triggered rescue payment;
2. simultaneous accept-now or wait decisions by private-cost incumbents;
3. an unobserved realized Poisson rival pool;
4. universal rejection as both trigger and endogenous public signal;
5. distinct rider and incumbent-driver discounting, with fresh entry kept contemporaneous;
6. rider post, abandon, repeat, and rescue decisions;
7. completion design over the full symmetric-cutoff WPBE correspondence relative to an optimized flat benchmark.

Do not call the Palm identity itself a contribution. Do not use Aviv (2008) as the sole or closest substantive neighbor.

## Paper requirements

The final paper must use a clean professional OM style and contain:

1. an abstract with exactly scoped results;
2. an introduction centered on the announced-rescue commitment problem;
3. three-part literature positioning: multistage and broadcast operations, strategic supplier rejection and procurement, and announced or two-sided dynamic pricing;
4. complete model, timing, information, beliefs, and equilibrium definition;
5. the reduced extensive-form figure;
6. arbitrary-menu equilibrium characterization;
7. the flat benchmark;
8. the local escalation theorem and exact mechanism decomposition;
9. global menu and thickness results, including counterexamples or limitations where necessary;
10. a known-$N$ or public-supply benchmark if it materially identifies the latent-supply mechanism;
11. managerial interpretation and institutional scope;
12. appendices containing every proof and auxiliary lemma;
13. a bibliography with verified primary-source metadata.

Avoid decorative notation, theorem boxes, unexplained regularity assumptions, and claims stronger than the mathematics. Use WPBE consistently. State whether every result concerns a fixed menu, an optimized flat policy, or the globally optimized dynamic menu.

## Completion and stopping rules

Do not return merely because several approaches fail, agents report hard gaps, or a large numerical search supports a conjecture. Continue launching new rounds and reopen blocked routes only when there is a genuinely new mechanism.

A major conjecture is resolved only by:

1. a complete proof that survives independent re-derivation and adversarial audit; or
2. an exact or interval-certified counterexample followed by a proved corrected statement with clearly identified maximal scope.

Never manufacture an affirmative theorem because the intended paper would benefit from it. If a global question remains unresolved after sustained, materially diverse search, label it as a conjecture or limitation, identify the exact mathematical gap, and remove every downstream claim that depends on it. The final paper itself must nevertheless be complete and correct: no theorem may rest on the unresolved gap.

Do not return a reduction to an equally strong missing lemma, a convenient equilibrium branch, a finite-grid pattern, or an endpoint argument presented as single-peakedness. Compilation success is not mathematical verification.

## Required deliverables

Create at least:

- announced_escalation_theory_overhaul.tex — the standalone full-English paper;
- announced_escalation_theory_overhaul.pdf — a clean compiled PDF;
- proof_claim_ledger.md — every claim, assumptions, proof location, equilibrium scope, and audit status;
- approach_and_counterexample_registry.md — live, blocked, circular, and falsified routes;
- reproducible source code for root isolation, optimization, derivative checks, and counterexample search.

The code and claim ledger must treat $\delta=1$ as a backward-compatibility
benchmark, not as the maintained model by accident. Include regression tests
showing that incentive discounting is not incorrectly applied to physical
period-2 completion or to fresh entrants.

Compile the LaTeX at least twice. Resolve undefined references, missing citations, compilation errors, and substantive layout failures. Check that the extensive-form figure path works from the output directory.

In the final response, report only:

- the strongest theorem package that survived audit;
- which initially desired claims were corrected or refuted;
- links to the .tex, .pdf, claim ledger, registry, and code;
- the exact scope of any remaining conjecture.

Do not describe the work as complete merely because the files compile. Mathematical audit, equilibrium audit, and falsification are the completion criteria.

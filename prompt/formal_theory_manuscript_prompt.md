# Prompt: theory-only formal manuscript for announced rescue pricing

You are revising the formal journal manuscript in
`paper/formal/main.tex`.  The group-meeting note in `group_meeting/` is a
separate artifact and must not be edited, copied into the paper, or used as
the journal template.

## Format

Use the official Management Science template at
<https://www.overleaf.com/latex/templates/template-for-management-science-journal/bjpqpdqhbshy>:

```latex
\documentclass[mnsc,blindrev]{informs3}
```

Keep the repository's `paper/informs3.cls` and `paper/informs2014.bst`.
Follow the reference papers only for theory-paper architecture and literature
positioning.  Do not cite an unrelated reference paper merely because its
format was supplied.

## Scope

Write a self-contained theory paper.  Do not create an empirical section,
future-data table, estimation plan, identification ledger, calibration
protocol, `DATA REQUIRED` marker, or counterfactual placeholder.  Numerical
work is model-generated evidence used to illustrate proved results or label
conjectures; it is not a substitute for a theorem.

The maintained institution has two response windows.  The platform commits
before types and supply are realized to an initial payment `p_1` and a
failure-contingent payment `p_2`, with `p_1 <= p_2`.  Universal rejection is
the only nonterminal public history.  A private-value rider chooses whether to
post and, after failure, whether to abandon, repeat `p_1`, or activate `p_2`.
Incumbent drivers have private persistent costs, may accept immediately or
wait, survive with probability `alpha`, and discount delayed payoff by
`delta`.  Fresh drivers enter at mean `gamma*m` and are unscreened.

Define the primitives once and cleanly:

```text
m       public expected incumbent thickness
alpha   incumbent survival probability
gamma   fresh-entry intensity relative to m
beta    rider continuation factor
delta   incumbent waiting-payoff discount
F       driver-cost CDF
G       rider-value CDF
```

State explicitly that `alpha` and `delta` do not conflict: `alpha` changes
physical availability and competition, while `delta` changes the incumbent's
intertemporal payoff.

## Required architecture

1. **Introduction**
   - Open with one or two concrete service-failure or driver-rejection events.
   - Use news only as motivation, not as proof of the model.
   - State the mechanism, main results, three contributions, and roadmap.
   - Do not use rhetorical questions or self-question-and-answer prose.

2. **Related Literature**
   - Organize by mechanisms: procurement clocks and contingent pricing;
     strategic waiting and platform intervention; latent supply, Poisson
     games, and market thickness; search with surviving incumbents and new
     entrants.
   - Each stream must end with: what it establishes, which primitive differs
     here, and why that difference changes the result.
   - Do not claim novelty from two periods, Poisson supply, entry, or strategic
     delay alone.

3. **Model and Timing**
   - Give the complete timing and information structure.
   - State the zero-payoff rule: whenever posting yields zero, the rider posts
     if and only if `v >= p_1`.
   - Explain why every deterministic public-history payment rule in this
     two-window, no-report institution is represented by `(p_1,p_2)`.  Call
     this institutional completeness, not optimality among arbitrary
     mechanisms.

4. **Equilibrium under an Arbitrary Menu**
   - Begin with continuous, strictly increasing, full-support `F,G`.
   - Do not assume a cutoff.  Allow anonymous symmetric independently mixed
     driver strategies and prove that every such WPBE is almost everywhere a
     pure cutoff.
   - Characterize the nonempty compact cutoff set, rider regions, failure
     posterior, completion probability, and flat benchmark.
   - Do not claim uniqueness for general distributions.

5. **Beyond Uniformity**
   - Prove the smooth no-entry local rescue theorem and its positive
     selection-robust completion derivative.
   - State convex-`F` global same-`p_1` dominance.
   - Give a concave-`F` counterexample and a continuous full-support
     multiple-cutoff counterexample.

6. **Exact Core**
   - Announce the specialization `F(c)=c`, `G(v)=v`, `gamma=0`.
   - Present the exact one-driver benchmark.
   - Then solve the latent-Poisson model: unique cutoff, fixed-`p_1` tangent
     rescue, Lambert-`W` continuation price, one-dimensional global design,
     policy attainment, same-`p_1` improvement, and rider-patience threshold.

7. **Market Thickness**
   - Define at the same fixed `m`
     `V(m)=M_R^*(m)-M_F^*(m)`.
   - Explain that this is the value of rescue pricing as thickness varies, not
     the marginal value of adding drivers.
   - Prove continuity, endpoint rates, and existence of a finite positive
     maximizer in the uniform no-entry core.
   - Label strict single-peakedness and uniqueness of the maximizer as open;
     any plotted peak is numerical evidence only.

8. **Surviving Incumbents and Fresh Entry**
   - Reintroduce `gamma>0` and distinguish screened surviving incumbents from
     unscreened entrants.
   - State the local activity condition, optimized-flat dominance condition,
     and supply-composition comparative statics.
   - Do not claim a globally solved mixed-supply menu problem.

9. **Discussion, Scope, and Conclusion**
   - Separate institutional representation from general mechanism design.
   - State equilibrium, distributional, and entry boundaries where they
     arise, not as a blanket disclaimer at the end.

10. **Appendix**
    - Order proofs exactly as results appear in the main text.
    - Put long algebra, counterexample certification, and equilibrium-selection
      topology in the appendix.

## Claim discipline

Maintain a visible distinction among:

- proved theorem;
- model-generated numerical illustration;
- conjecture or open question;
- counterexample delimiting a theorem.

Safe claims include endogenous cutoff and existence for general continuous
types, local improvement for smooth no-entry distributions, convex-`F`
same-payment dominance, and exact global design under uniform no entry.

Unsafe claims include uniqueness for general `F,G`, a general-distribution
shape theorem for `V(m)`, two-price optimality among arbitrary direct
mechanisms, pessimistic policy attainment from closed graph alone, or a global
optimal menu with fresh entry.

## Verification

Before completion:

1. regenerate theoretical outputs with `make formal-figures`;
2. compile with `make formal`;
3. run the theory tests with `make test`;
4. verify no undefined references, citation errors, duplicate PDF anchors, or
   overfull boxes;
5. render every PDF page and inspect theorem breaks, equations, tables,
   figures, references, and appendix pages;
6. confirm that `group_meeting/` is unchanged;
7. commit the coherent theory-paper revision without pushing unless the user
   explicitly authorizes a push.

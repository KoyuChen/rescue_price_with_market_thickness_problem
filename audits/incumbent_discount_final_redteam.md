# Final integration red-team: incumbent discount

Audited source: `announced_escalation_theory_overhaul.tex` after integration
of the incumbent discount \(\delta\in(0,1]\).  The audit compared the main
text and appendix against `incumbent_discount_global_audit.md`, rederived the
public-\(n\) local formulas, checked every explicit tag/label/reference, and
compiled the paper in an isolated output directory.

## Final verdict after repair: **PASS — no remaining mandatory issue**

The two defects recorded below were repaired in the current manuscript and
then independently rechecked. Equations (54a)--(54b) now supply the missing
fourth-order certificate, and the thick-market statement now gives the correct
uniformity over all \(\delta\in(0,1]\) for fixed positive \((\alpha,\beta)\).
An isolated three-pass build has no unresolved references, label drift,
warnings, or box errors. The numbered sequence is (54), (54a), (54b), (55).

## Original pre-repair verdict: **FAIL pending two mandatory thickness repairs**

The discounted cutoff geometry, fixed-\(p\) solution, outer scalar reduction,
optimized dominance, patience comparative static, all \(\delta<1\) thin
formulas, and the public-\(n\) benchmark are correctly integrated.  The only
mandatory defects are:

1. the theorem falsely says the thick-market estimate is nonuniform as
   \(\delta\downarrow0\); and
2. the appendix claims the \(\beta=1/2,\delta=1\) fourth-order coefficient
   from a “previously displayed” expansion that is not present.  Equation
   (54), with only an \(O(m^4)\) remainder, cannot prove an exact \(m^4\)
   coefficient.

No manuscript file was edited by this red-team agent.

## Mandatory repair 1: the thick estimate is uniform in \(\delta\)

### Current overclaim

The theorem following (50) says that the thick limits are not uniform when
\(\alpha\), \(\beta\), **or \(\delta\)** approaches zero with \(m\).  The
appendix repeats that fixed positive \(\delta\) “explains” this
nonuniformity.

The \(\delta\) part is false.  For fixed positive \((\alpha,\beta)\), the
dynamic-loss estimate is uniform over every sequence
\(\delta_m\in(0,1]\):

- the policy-uniform lower bound uses only
  \(P_m^\delta(a)\ge a\) and (55), so it contains no lower bound on
  \(\delta\);
- for the feasible upper construction,
  \(R_\delta=\delta R_1\) implies
  \(P_m^\delta(a)\le P_m^1(a)\).  Hence
  \(P_m^\delta(a)-a\) is bounded by the \(\delta=1\) construction, uniformly
  for \(0<\delta\le1\).  The continuation term \(T_m(a)\) is independent of
  \(\delta\).

Thus

\[
 \sup_{0<\delta\le1}
 \left|\frac{m[1-D_{\alpha,\delta,0}^*(m)]}{\log\log m}-1\right|
 \longrightarrow0
\]

for fixed positive \((\alpha,\beta)\).  The flat loss is independent of
\(\delta\), so the value-gain rate is also uniform in \(\delta\).

### Exact textual repair

Replace the sentence after (50) by:

> For each fixed positive \((\alpha,\beta)\), the estimates establishing
> (50) are uniform over the full policy/cutoff domain and uniformly over
> \(\delta\in(0,1]\).  They are not uniform over primitive sequences with
> \(\alpha\downarrow0\) or \(\beta\downarrow0\).

Replace the last sentence of the thick-limit appendix proof by the same
uniformity argument; do not list \(\delta\) among the nonuniform primitives.

## Mandatory repair 2: restore the missing fourth-order certificate

### Proof gap

For \(\beta=1/2\), equation (54) states

\[
 J_m^\delta(1/2-cm)
 =\frac m4-\frac{m^2}{16}
 +m^3\left\{\frac1{96}+\frac c8-A_\delta c^2\right\}
 +O(m^4).
\]

This proves the cubic formula (47) whenever \(\delta<1\), because its cubic
coefficient differs strictly from the flat coefficient.  At \(\delta=1\),
however, the cubic difference is zero.  An unspecified \(O(m^4)\) remainder
cannot identify the coefficient \(\alpha/2048\) in (48).  The appendix then
refers to a “previously displayed compact argmax expansion,” but no
fourth-order display occurs in the current source.

### Exact mathematical repair

Restore the \(\delta=1\) rescaled expansion

\[
 \begin{aligned}
 J_m^1(1/2-cm)
 &=\frac m4-\frac{m^2}{16}
   +m^3 f_2(c)+m^4 f_3(c)+o(m^4),\\
 f_2(c)&=\frac{11}{768}-\left(c-\frac1{16}\right)^2,\\
 f_3(c)&=-\frac1{768}-\frac c{24}+\frac{c^2}{4}
          +2\alpha c^3,
 \end{aligned}
\]

uniformly for bounded \(c\), together with

\[
 F_0^*(m)
 =\frac m4-\frac{m^2}{16}
  +\frac{11}{768}m^3-\frac3{1024}m^4+o(m^4).
\]

The strict quadratic loss in \(f_2\) and local Lipschitz control of \(f_3\)
give

\[
 \max_c\{f_2(c)+mf_3(c)+o(m)\}
 =f_2(1/16)+mf_3(1/16)+o(m),
\]

where

\[
 f_3(1/16)=-\frac3{1024}+\frac{\alpha}{2048}.
\]

Subtracting the flat expansion proves (48) without assuming a higher-order
expansion of the optimizer.  This is the missing certificate and also fixes
the appendix's dangling “previously displayed” reference.

## Discounted main-text/appendix consistency: PASS

The following chains match exactly.

### General and fresh-entry equilibrium

- Waiting payoff in (5), the affine margin (6), cutoff margin (7), and
  equilibrium correspondence (8) all carry the factor \(\delta\) in the
  incentive terms but not in physical completion (9).
- The flat menu remains at cutoff \(a=p\), and its physical completion
  (12)--(13) is correctly independent of \(\delta\).
- In (L3)--(L4), both the cutoff coefficient and localization bound contain
  \(\delta\).  The derivative factorization (L5)--(L6) is correct:
  \[
  T_\delta=T_1+(1-\delta)R\alpha\ell
  \{1-\rho+\rho E(1+\gamma)\}>0
  \]
  under active rescue.  The appendix proves this relation, and the stated
  outside-activity counterexample remains negative at \(\delta=1/2\).

### Global no-entry geometry

- The cutoff scalar (17) is
  \((p-a)h(a)-\delta K_{p,q}(a)\).
- The repeat-branch exclusion (18) and global downward-crossing proof remain
  valid because \(0<\delta\le1\).
- The positive-cutoff identity (20), reject-all inequality (21), and local
  derivative (23)--(24) have the correct discount factors.
- The fixed-\(p\) cutoff equation (30), implementability equation (31),
  \(p_z\) in (29), \(R_\delta\), the lower root \(P_\delta\) in (33), and
  \(J_\delta\) in (34) agree with the appendix.
- The outer maximum (35), strict dominance (37), and the pointwise discount
  comparative static (38a) are valid.  In particular,
  \(\partial_\delta P_\delta>0\) and
  \(\partial_\delta J_\delta<0\) at an interior target cutoff.

### Patience threshold

**PASS.**  The single upper gain interval, bounds (41), scalar test (42), and
nested-threshold result (42a) follow from fixed-menu monotonicity, scalar
continuity, and pointwise monotonicity in \(\delta\).  The inequality direction
is correct:

\[
 0<\delta_1<\delta_2\le1
 \quad\Longrightarrow\quad
 \beta_c(m,\alpha,\delta_1)
 \le\beta_c(m,\alpha,\delta_2).
\]

## Thin-market theorem: PASS except for mandatory repair 2

- **\(\beta>1/2,\delta<1\): PASS.**  The limiting lower root and objective in
  (44) are correct, \(G_{\alpha,\beta,\delta}>1/4\), and (45) correctly gives
  an order-\(m\) equality with the exact optimized coefficient.
- **\(\beta>1/2,\delta=1\): PASS.**  Equation (46) correctly restores the
  order-\(m^2\) boundary result.
- **\(\beta=1/2,\delta<1\): PASS.**  The localization
  \(a=1/2-cm\), expansion (54), and quadratic maximization establish the
  claimed equality
  \[
  V_{\alpha,\delta,0}(m)
  \sim\frac{\alpha(1-\delta)}
  {512\{1-\alpha(1-\delta)/2\}}m^3.
  \]
  This is not merely a feasible lower bound.
- **\(\beta=1/2,\delta=1\): formula correct, proof incomplete.**  Repair 2
  supplies the missing coefficient proof.
- **\(\beta<1/2\): PASS.**  The uniform limiting bound is strictly below
  \(1/4\), so the exact initial equality in (49) follows.

## Public-\(n\) benchmark: PASS

The discounted indifference equation (59) implies

\[
 M_n=(1-p_1)n s_n(a)
 \left[a+\frac{p_1-a}{\delta}\right],
\]

so (60) is correct.  The localized affine equation gives exactly

\[
 \kappa_n=
 \frac{\delta(1-p)^{n-1}\alpha\rho(p)}
 {s_n(p)-\delta(1-p)^{n-1}\alpha\rho(p)}.
\]

Differentiating (60) along
\(a_\varepsilon=p-\kappa_n\varepsilon+o(\varepsilon)\) yields (62):

\[
 (1-p)n\kappa_n
 \left\{\frac{1-\delta}{\delta}s_n(p)-p s_n'(p)\right\}.
\]

Therefore the derivative is strictly positive for every \(n\ge1\) when
\(\delta<1\); at \(\delta=1\), it is positive exactly for \(n\ge2\) and zero
for \(n=1\).  The appendix's all-equilibrium localization and \(C^1\)
one-crossing proof continue to justify local uniqueness.

## Tags, references, and clean build

**PASS.**  Automated source checks found:

- 76 explicit equation tags and no duplicate tag;
- 26 labels and no duplicate label;
- no reference to a missing label;
- the hard-coded equation references from the discounted global section
  through public \(n\) point to the intended formulas.

Three consecutive PdfLaTeX passes were run in an isolated temporary output
directory.  The final pass completed successfully with no unresolved
citation, reference, label, overfull-box, underfull-box, or compilation
warning.

## Final mandatory-fix checklist

1. Remove \(\delta\downarrow0\) from the thick-market nonuniformity claim and
   state the correct uniformity over \(\delta\in(0,1]\), in both theorem and
   appendix.
2. Restore the displayed \(\delta=1,\beta=1/2\) fourth-order expansion and
   compact-argmax argument needed for the coefficient \(\alpha/2048\).

After these two repairs, the integrated discounted manuscript is **PASS with
no further mandatory fix**.

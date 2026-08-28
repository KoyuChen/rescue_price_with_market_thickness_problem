# Three-regime cutoff-WPBE model

## 1. Supply regimes

The two response windows have equal length and the core footprint has unit
area. The first-window incumbent cohort and second-window fresh core cohort are

\[
N_1\sim\operatorname{Pois}(m),\qquad
N_2^C\sim\operatorname{Pois}(m),\qquad N_1\perp N_2^C.
\]

Thus \(m\) is a per-window cohort flow, not a stationary stock counted twice.
The platform separately solves:

1. **Incumbents only** \(r=I\): retained first-window rejectors, policy
   \((p_1,p_2)\).
2. **Fixed footprint with arrivals** \(r=A\): retained rejectors plus
   \(N_2^C\), policy \((p_1,p_2)\).
3. **Expanded search** \(r=E\): the same core supply plus an outer annulus in
   rescue, policy \((p_1,p_2,s)\).

Regimes \(I\) and \(A\) are supply benchmarks, not nested mechanism sets.
Regime \(A\) is nested in \(E\), because \(s=1\) exactly reproduces the
fixed footprint.

## 2. Incumbent exit and terminal supply

Rider value and persistent driver order cost are \(v,c\sim U[0,1]\). Let
\(\omega\in[0,1]\) be the exogenous probability that a first-window rejector
remains physically available for the terminal lottery. It is independent of
cost and the terminal action. For first-window cutoff \(a\) and terminal
action \(j\in\{1,2\}\), where 1 is repeat and 2 is rescue,

\[
I_j^\omega(a)=\omega m[F(p_j)-F(a)]_+.
\]

Fresh volunteer intensities are

\[
e_j^I=0,
\qquad
e_j^A=mF(p_j),
\]

\[
e_1^E=mF(p_1),
\qquad
e_2^E=mF(p_2)+m\int_1^sF(p_2-d(u))\,du.
\]

Hence

\[
\Lambda_j^r(a)=I_j^\omega(a)+e_j^r,
\qquad
C_j^r(a)=1-e^{-\Lambda_j^r(a)}.
\]

The same \(\omega\) multiplies the focal rejector's continuation payoff, so
the model treats pool attrition and individual waiting value consistently. The
main calibration uses \(\omega=.8\); exit is therefore active, not merely an
unused primitive.

## 3. Expanded-search multiplier and pickup cost

Normalize the core radius to \(R_0\). Search multiplier \(s\ge1\) expands
the rescue footprint to

\[
R(s)=R_0\sqrt{s}.
\]

Spatial Poisson independent increments give

\[
N_2^O(s)\sim\operatorname{Pois}((s-1)m),
\qquad
N_2^O(s)\perp N_2^C.
\]

Let \(u=(\ell/R_0)^2\) be area rank. Core pickup is absorbed into \(c\); an
outer winner pays

\[
d(u)=\tau(\sqrt u-1)_+
\]

only after assignment. A fresh driver's response payoff is

\[
h(\Lambda)[p-c-d(u)],
\qquad
h(z)=\frac{1-e^{-z}}{z},\quad h(0)=1.
\]

Thus the assignment probability scales the payoff but does not affect its
sign:

\[
\text{volunteer}\iff c+d(u)\le p.
\]

This produces Poisson thinning, not a fresh-entry fixed point.

## 4. Rider continuation

After universal rejection, the rider observes failure but not realized
incumbent retention, future arrivals, or volunteer counts. Given the
equilibrium cutoff, she compares

\[
0,\qquad C_1^r(a)(\beta v-p_1),\qquad
C_2^r(a)(\beta v-p_2).
\]

Let

\[
\eta_j^r(a)
=\Pr(A=j\mid v\ge p_1,\text{ first-window failure};a)
\]

for abandon, repeat, and rescue actions \(j=0,1,2\).

## 5. Complete cutoff-WPBE

Under a proposed aggregate cutoff, a type-\(c\) incumbent's
accept-minus-wait payoff is

\[
D_r(c;a)
=h(mF(a))(p_1-c)
-\delta\omega e^{-mF(a)}
\sum_{j=1}^2\eta_j^r(a)h(\Lambda_j^r(a))[p_j-c]_+.
\]

Together with rider and fresh-driver strategies, \(a\) is a cutoff-WPBE iff
on-path beliefs obey Bayes' rule and

\[
D_r(c;a)\ge0\quad\forall c<a,
\qquad
D_r(c;a)\le0\quad\forall c>a,
\]

with indifference at an interior cutoff. The payoff difference is piecewise
affine in type, so the solver checks the full type domain at the affine
interval endpoints and certifies the root set under grid refinement.

### Unique cutoff in the maintained model

For the maintained uniform-cost, type-independent-retention, and
assignment-contingent-pickup specification, every admissible policy in all
three regimes induces exactly one cutoff-WPBE. The key restrictions are that
fresh volunteer intensity is independent of the conjectured incumbent cutoff
and that terminal incumbent retention is the constant `omega`.

Let

\[
\mathcal A(a)=h(ma)(p_1-a),\qquad
Y_j(a)=e^{-ma}h(\Lambda_j(a))(p_j-a).
\]

At every nondegenerate holdout root,

\[
h(\Lambda_2)(p_2-a)>h(\Lambda_1)(p_1-a).
\]

On an active repeat--rescue branch the rescue mass is weakly increasing in
the proposed cutoff. Together with

\[
-\omega Y_j'(a)\le e^{-ma},
\qquad
-\mathcal A'(a)>e^{-ma},
\]

this makes the cutoff residual cross zero strictly downward at every root.
Two roots are therefore impossible. Existence follows from the endpoint
signs. Consequently the equilibrium set below is a singleton and the
conservative and optimistic selections coincide analytically; numerical root
certification remains an implementation audit.

## 6. Completion and search-resource objective

Posting probability is \(1-p_1\) and first-window universal rejection
probability is \(e^{-mF(a)}\). Completion is

\[
M_r(\mu,a)
=(1-p_1)\left[
1-e^{-mF(a)}
+e^{-mF(a)}\{\eta_1^rC_1^r+\eta_2^rC_2^r\}
\right].
\]

For uniform riders, terminal self-selection can also be integrated out
exactly. Define

\[
q=e^{-ma},\qquad
\rho_j=1-\frac{p_j}{\beta},\qquad
A_j=\rho_j C_j.
\]

Then every cutoff-WPBE outcome satisfies

\[
M=(1-p_1)(1-q)+q\max\{0,A_1,A_2\},
\]

and, when `C_2>C_1`, expected executed outer contacts are

\[
Q_E^{\mathrm{ex}}
=q m(s-1)\frac{[A_2-A_1]_+}{C_2-C_1}.
\]

The max formula removes rider-composition notation from completion, but the
composition remains economically relevant in the incumbent incentive
constraint and in search-resource use.

Driver-paid pickup cost affects willingness but is not a platform search cost.
The maintained platform resource is the failure-contingent capacity needed to
honor the promised outer footprint, purchased after first-window failure but
before the rider's terminal action:

\[
Q_E^{\mathrm{com}}(\mu,a)
=(1-p_1)e^{-mF(a)}m(s-1),
\qquad Q_I^{\mathrm{com}}=Q_A^{\mathrm{com}}=0.
\]

The maintained outer objective is

\[
J_r(\mu,a)=B M_r(\mu,a)-\kappa Q_r^{\mathrm{com}}(\mu,a).
\]

This is completion net of committed search capacity, not platform profit.
Unlike \(Q^{\mathrm{ex}}\), it does not vanish at a rider rescue-activation
boundary. Core notifications are treated as installed infrastructure and
normalized to zero incremental cost. The executed-contact specification is
retained only as a robustness objective. If core activation is also a platform
choice, use

\[
J_{\kappa_C,\kappa_O}
=BM-\kappa_CQ^C-\kappa_OQ^{\mathrm{com}},
\qquad
Q^C=(1-p_1)e^{-mF(a)}(\eta_1+\eta_2)m.
\]

## 7. Outer equilibrium-constrained mechanism design

For each regime and environment \(\theta=(m,\beta,\delta;\tau,\omega)\),

\[
V_r(\theta)
=\max_{\mu_r\in\mathcal M_r}
\min_{a\in\mathcal E_r^{\mathrm{WPBE}}(\mu_r;\theta)}
J_r(\mu_r,a).
\]

The inner set is a singleton in the maintained model. The unique cutoff is
continuous in policies and primitives, so the equilibrium-reduced objective
is continuous. Compact policy sets and Berge's maximum theorem imply that the
outer optimum exists and that each optimized value is continuous in the
environment.

The computation literally fixes \(p_1\), optimizes the allowed \(p_2,s\)
while re-solving the complete WPBE at every evaluation, and then optimizes
\(p_1\). Conservative equilibrium selection minimizes \(J_r\), the same
objective used in the outer problem. A deterministic-seed differential-
evolution pass independently searches the equivalent normalized joint policy
domain. Its candidates and the nested-profile candidates are all re-ranked
using a denser cutoff grid and grid-doubling WPBE certification. This guards
against a missed policy basin; it does not turn numerical search into an
analytic proof of global optimality.

For computation, the active continuation branch imposes \(p_2\le\beta\)
without loss: because \(v\le1\), a rescue payment above \(\beta\) gives every
rider negative delayed surplus. The inactive branch \(p_1\ge\beta\) is solved
separately.

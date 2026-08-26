# Numerical falsification report: discounted incumbent continuation payoff

## Scope and verdict

This audit studies the corrected model in which a surviving incumbent
driver's period-2 net payoff is

\[
\delta(p-c),\qquad 0<\delta\le 1,
\]

while a fresh entrant receives the contemporaneous payoff \(p-c\). The
baseline engine and manuscript were not edited. The independent extension is
in code/discount_model.py, with deterministic scans in
code/run_discount_falsification.py.

The correction cannot be implemented by replacing \(\alpha\) everywhere with
\(\delta\alpha\). Discounting changes an incumbent's incentive to wait, but
does not discount physical continuation supply or completion.

| Object | Finding |
|---|---|
| Flat cutoff \(a=p\) | Survives for every \(0<\delta\le1\) |
| Local active-rescue gain | Survives and becomes weakly larger as \(\delta\) falls |
| Optimized-flat dominance for \(\beta\ge1/2\) | Survives |
| Cutoff uniqueness | No counterexample in 150,800 policy scans or 80 MP cross-checks |
| Thin, \(\beta>1/2\), old \(V=\Theta(m^2)\) | False for fixed \(\delta<1\); a feasible menu gives order \(m\) |
| Thin, \(\beta=1/2\), old \(\alpha m^4/2048\) | False for fixed \(\delta<1\); a feasible menu gives order \(m^3\) |
| Thin, \(\beta<1/2\), zero plateau | Survives |
| Thick rates | The old leading rates survive uniformly over \(\delta\in(0,1]\) for fixed \(\alpha,\beta>0\) |
| Patience and thickness topology | No new interval reversal or multiple-peak signature |

The two thin-market failures below have algebraic feasible-menu certificates;
they are not inferred only from fitted slopes.

## 1. Corrected equilibrium and completion formulas

Let

\[
\lambda_j(a)=m\{\alpha(p_j-a)+\gamma p_j\},\qquad
C_j(a)=1-e^{-\lambda_j(a)},\qquad
\phi(x)=\frac{1-e^{-x}}{x}.
\]

The rider switch and repeat/rescue masses \(r(a)\) and \(e(a)\) are unchanged.
A focal incumbent obtains

\[
A(c;a)=\phi(ma)(p_1-c)
\]

from accepting immediately, and

\[
W_\delta(c;a)=
\delta\alpha e^{-ma}
\left\{
r(a)\phi(\lambda_1)[p_1-c]^+
+e(a)\phi(\lambda_2)[p_2-c]^+
\right\}
\tag{1}
\]

from waiting. Thus the corrected cutoff residual is

\[
f_\delta(a;p_1,p_2)=A(a;a)-W_\delta(a;a).
\tag{2}
\]

Physical completion has no direct discount factor:

\[
M(a;p_1,p_2)
=(1-p_1)\left[
1-e^{-ma}+e^{-ma}\{r(a)C_1(a)+e(a)C_2(a)\}
\right].
\tag{3}
\]

The implementation keeps (1) and (3) separate. At \(\delta=1\), regression
tests reproduce the original residual and completion to binary64 roundoff.

## 2. Flat cutoff and local escalation

For a flat menu \((p,p)\), the residual below \(p\) factors as

\[
f_\delta(a;p,p)
=(p-a)\left[
\phi(ma)-\delta\alpha e^{-ma}\rho(p)
\phi\!\left(m\{\alpha(p-a)+\gamma p\}\right)
\right].
\tag{4}
\]

The bracket is strictly positive at \(\delta=1\), and reducing \(\delta\)
only increases it. Hence the unique numeric cutoff remains \(a=p\). The flat
completion function is unchanged:

\[
F_\gamma(m,p)
=(1-p)(1-e^{-mp})
+e^{-mp}[1-p/\beta]^+(1-e^{-\gamma mp}).
\tag{5}
\]

The deterministic flat grid covered 2,304 policies over
\(\delta\in\{1,.5,.01,10^{-6}\}\), \(m\in\{10^{-4},.1,10,10^4\}\),
four \(\alpha\)'s, three \(\beta\)'s, three \(\gamma\)'s, and four prices.
Every equilibrium set was \(\{p\}\), and every value matched (5).

For a flat base price \(0<p<\beta\), define

\[
R=e^{-mp},\quad E=e^{-\gamma mp},\quad
\sigma=\phi(mp),\quad \ell=\phi(\gamma mp),\quad
\rho=\frac{1-p/\beta}{1-p}.
\]

When limiting rescue is active with mass \(\eta^0>0\), the corrected cutoff
displacement is

\[
\kappa_\delta
=\frac{R\delta\alpha\ell\eta^0}
{\sigma-R\delta\alpha\rho\ell}.
\tag{6}
\]

The completion derivative can be written

\[
L_\delta
=m(1-p)R\eta^0
\frac{T_\delta}{\sigma-R\delta\alpha\rho\ell},
\tag{7}
\]

where

\[
T_\delta
=E(\alpha+\gamma)\sigma
-\delta R\alpha\ell
\{1-\rho+\rho E(1+\gamma)\}.
\tag{8}
\]

Since

\[
T_\delta-T_1
=(1-\delta)R\alpha\ell
\{1-\rho+\rho E(1+\gamma)\}\ge0,
\tag{9}
\]

the audited positive sign at \(\delta=1\) implies positivity for every
\(0<\delta\le1\) in the active region.

Finite differences at \(\varepsilon=10^{-7}\) independently match (7):

| \((m,\alpha,\beta,\gamma,\delta;p)\) | Corrected derivative | Quotient | Old \(\delta=1\) coefficient |
|---|---:|---:|---:|
| \((2,.8,.7,0,.5;.3)\) | 0.418370652801171 | 0.418370487698105 | 0.259022397696287 |
| \((.1,1,.9,0,.1;.3)\) | 0.0643614699128738 | 0.0643614577605645 | 0.0156160651525307 |
| \((2,.8,.8,.3,.5;.3)\) | 0.466672419491855 | 0.466672223642384 | 0.369853589839566 |
| \((.3,.5,.9,2,.2;.3)\) | 0.210047179213602 | 0.210047102211508 | 0.180139821356110 |

Thus the old coefficient is quantitatively wrong under discounting, even
though the sign conclusion survives.

## 3. Corrected no-entry geometry

For \(\gamma=0\), set \(k=\alpha m\). For a target cutoff
\(a\in[0,\beta]\), let \(Q(a)\) maximize

\[
S(a,q)=(\beta-q)\{1-e^{-k(q-a)}\}.
\]

The tangent rescue price is unchanged and solves

\[
e^{k(Q-a)}-1=k(\beta-Q).
\tag{10}
\]

Write \(S(a)=S(a,Q(a))\) and

\[
h_m(a)=\frac{e^{ma}-1}{a},\qquad h_m(0)=m.
\]

The implementing first price becomes the lower root

\[
(1-P_\delta)(P_\delta-a)
=\frac{\delta S(a)}{\beta h_m(a)},
\tag{11}
\]

namely

\[
P_\delta(a)
=\frac{1+a-\sqrt{(1-a)^2-4\delta S(a)/[\beta h_m(a)]}}{2}.
\tag{12}
\]

The physical scalar objective is

\[
J_\delta(a)
=(1-P_\delta(a))(1-e^{-ma})
+e^{-ma}\frac{S(a)}{\beta}.
\tag{13}
\]

At a positive equilibrium cutoff, the corrected completion identity is

\[
M_\delta(p,q;a)
=(1-p)m\phi(ma)
\left[a+\frac{p-a}{\delta}\right].
\tag{14}
\]

For \(a<p\), both the bracket in (14) and the assignment share dominate
their flat counterparts. The zero-cutoff boundary inequality gives the same
strict comparison. Hence every active no-entry strict menu beats the flat
menu with the same first price. Applying this at the optimized flat price
\(p_F(m)<1/2\) preserves global dominance for \(\beta\ge1/2\).

Twenty thousand random geometry points used
\[
m\in[10^{-5},10^6],\quad
\alpha\in[10^{-8},1],\quad
\beta\in(.01,.99),\quad
\delta\in[10^{-6},1].
\]

They produced no ordering failure of
\(a\le P_\delta(a)<Q(a)<\beta\), maximum cutoff residual
\(3.89\times10^{-16}\), and maximum difference between (3) and (13)
\(3.33\times10^{-16}\).

## 4. Algebraic thin-market counterexamples

### 4.1 Patient riders: the order changes from \(m^2\) to \(m\)

As \(m\downarrow0\), define

\[
U(a)=\frac{\alpha(\beta-a)^2}{4\beta}.
\]

Let \(P_{0,\delta}(a)\) be the lower root of

\[
(1-p)(p-a)=\delta U(a).
\tag{15}
\]

The leading physical completion per unit thickness is

\[
\Lambda_\delta(a)
=(1-P_{0,\delta}(a))a+U(a).
\tag{16}
\]

Take the exact tuple

\[
\alpha=1,\qquad \beta=\frac{9}{10},\qquad
\delta=\frac12,\qquad a=\frac3{10}.
\]

Then

\[
U(a)=\frac1{10},\qquad
P_{0,\delta}(a)=\frac{13-\sqrt{29}}{20},
\]

and

\[
\Lambda_\delta(a)-\frac14
=\frac{3\sqrt{29}-9}{200}
=0.03577747210701756046876065737\ldots>0.
\tag{17}
\]

The tangent menu at this cutoff is feasible for all sufficiently small
positive \(m\). Thus the candidate exact lower certificate is

\[
\liminf_{m\downarrow0}\frac{V(m)}{m}
\ge\frac{3\sqrt{29}-9}{200}>0.
\tag{18}
\]

High-precision evaluations of this one feasible menu are:

| \(m\) | \((J_\delta-F^*)/m\) |
|---:|---:|
| \(10^{-1}\) | 0.03554220951036278460303671666 |
| \(10^{-2}\) | 0.03575701334685787807059445968 |
| \(10^{-3}\) | 0.03577545820837919850013087124 |
| \(10^{-4}\) | 0.03577727103826381601420924264 |
| \(10^{-5}\) | 0.03577745200335462671988114588 |

This rules out the old \(V=\Theta(m^2)\) rate. The natural corrected
conjecture for fixed \(\delta<1\) and \(\beta>1/2\) is

\[
V(m)\sim m
\left\{
\max_{a\in[0,\beta]}\Lambda_\delta(a)-\frac14
\right\}.
\tag{19}
\]

### 4.2 Critical riders: the order changes from \(m^4\) to \(m^3\)

Put

\[
A_\delta=1-\frac{\alpha(1-\delta)}2>0,
\qquad a=\frac12-cm.
\]

A formal Taylor expansion of (10)--(13), uniform for bounded fixed \(c\),
gives

\[
\frac{J_\delta(a)}m
=\frac14-\frac m{16}
+\left\{
\frac1{96}+\frac c8-A_\delta c^2
\right\}m^2+O(m^3).
\tag{20}
\]

The quadratic is maximized at \(c=1/(16A_\delta)\). Comparing it with the
flat coefficient \(11/768=1/96+1/256\) yields the corrected conjecture

\[
V(m)\sim
\frac{\alpha(1-\delta)}
{512\{1-\alpha(1-\delta)/2\}}m^3,
\qquad \beta=\frac12,\quad \delta<1.
\tag{21}
\]

Equality in (21) needs the usual uniform rescaled-argmax proof. The feasible
cutoff already supplies a lower bound that refutes the old \(m^4\) rate.

For \((\alpha,\delta)=(1,1/2)\), one has
\(A_\delta=3/4\), \(c=1/12\), and coefficient \(1/768\):

| \(m\) | \((J_\delta-F^*)/m^3\) | \((J_\delta-F^*)/m^4\) |
|---:|---:|---:|
| \(10^{-2}\) | 0.0012980944515318440 | 0.1298094451531844 |
| \(10^{-3}\) | 0.0013016853706564296 | 1.301685370656430 |
| \(10^{-4}\) | 0.0013020435464139507 | 13.02043546413951 |
| \(10^{-5}\) | 0.0013020793547349719 | 130.2079354734972 |
| \(10^{-6}\) | 0.0013020829354744331 | 1302.082935474433 |

The cubic ratio converges to
\(1/768=0.0013020833333333\ldots\), while the fourth-order ratio diverges.
At \(\delta=1\), the cubic term vanishes and the original
\(\alpha m^4/2048\) layer is recovered.

### 4.3 Impatient riders

For \(\beta<1/2\), \(P_{0,\delta}(a)\ge a\), so

\[
\Lambda_\delta(a)
\le a(1-a)+\frac{(\beta-a)^2}{4\beta}.
\tag{22}
\]

The right side is increasing on \([0,\beta]\) when \(\beta\le1/2\), and
its endpoint is \(\beta(1-\beta)<1/4\) for \(\beta<1/2\). Uniform
convergence therefore preserves an exact initial interval on which the flat
policy wins and \(V(m)=0\). This plateau continues to disprove strict
single-peakedness for \(\beta<1/2\).

## 5. All-root search and high-precision checks

The fast path uses uniform and cosine cutoff nodes, analytic endpoint
conditions, Brent sign brackets, and searches for same-sign tangent roots.
The MP path recursively excludes boxes using monotone factor enclosures. Any
same-sign box that cannot be excluded is retained as unresolved. These are
interval-style safeguards, not formal directed-rounding certificates.

Full results:

- 100,800 structured menus: no multiple cutoff and no negative same-first-price
  completion gain;
- 50,000 log-random menus: no multiple cutoff and no negative same-first-price
  completion gain;
- 80 independent MP box-isolation checks: no mismatch and no unresolved box;
- sampled ranges included \(\delta\in[10^{-6},1]\),
  \(m\in[10^{-4},10^4]\), and \(\gamma\in[0,100]\).

The minimum structured same-price gain was
\(-1.11\times10^{-16}\), on a flat menu, and is binary64 subtraction error.

Very thick markets with small \(\delta\) create roots less than one
binary64 ulp below \(p\). The fast path labels these as near-p limits rather
than upper-boundary equilibria. There were 1,986 structured and 7,410 random
cases.

A clean 100-digit example is

\[
(m,\alpha,\beta,\gamma,\delta;p,q)
=(150,.36,.88,0,10^{-5};.84,.85).
\]

It has

\[
f(p-10^{-60})=6.8100\times10^{-63}>0,
\]

but

\[
f(p-10^{-65})=-1.1264\times10^{-63}<0.
\]

Thus the exact interior root satisfies
\(p-a\in(10^{-65},10^{-60})\). This is an underflow/coalescence signature,
not multiplicity.

For the moderate tuple

\[
(m,\alpha,\beta,\gamma,\delta;p,q)=(2,.8,.7,0,.5;.3,.5),
\]

the unique MP sign-changing root is bracketed by

\[
\begin{aligned}
a_{\rm lo}&=0.2770918415344208269360504503306944874561,\\
a_{\rm hi}&=0.2770918415344208269360504503325877536286.
\end{aligned}
\]

The endpoint residuals have opposite signs,
\(9.95\times10^{-32}\) and \(-1.19\times10^{-30}\), and completion is
\(0.3470651084518902670024156348061879\).

## 6. Patience and thickness

### Patience scan

Ninety no-entry patience curves used

\[
m\in\{.01,.1,1,10,100\},\quad
\alpha\in\{.01,.1,1\},\quad
\delta\in\{1,.9,.5,.1,.01,10^{-4}\},
\]

with 99 \(\beta\) nodes per curve. Every improvement set was a single upper
interval. There was no pointwise decrease in gain as \(\delta\) fell.

The coarse threshold marker moved only near the thin critical layer. For
\(m=.01,\alpha=.01\), the markers were
\(.52,.51,.51,.51,.51,.51\) as \(\delta\) decreased. For
\(m=.01,\alpha=.1\), they were
\(.51,.51,.50,.50,.50,.50\). These are grid markers, not threshold
certificates.

### Thickness profiles

The full search used 108 profiles:

\[
\delta\in\{1,.9,.5,.1,.01,10^{-4}\},\quad
\alpha\in\{1,.1,.001\},\quad
\beta\in\{.2,.49,.5,.51,.7,.9\},
\]

with 101 logarithmic nodes on \(m\in[10^{-5},10^6]\). It found:

- no down-then-up reversal in \(V(m)\);
- no multiple numerical thickness peak;
- no scalar cutoff objective with multiple stationary maxima;
- no dominance violation for \(\beta\ge1/2\).

Boundary samples were kept separate from stationary maxima, and near-duplicate
cutoff/value candidates were tolerance-deduplicated. This search does not
prove single-peakedness for \(\beta\ge1/2\).

### Thick-market diagnostics

Writing \(x=ma\) and \(T=S/\beta\), (11) and (13) imply

\[
1-J_\delta(a)
=P_\delta(a)(1-e^{-x})+(1-T)e^{-x}.
\tag{23}
\]

This is the same-form loss decomposition as at \(\delta=1\). The geometry
supports

\[
1-D_\delta^*(m)\sim\frac{\log\log m}{m},
\qquad
V_\delta(m)\sim\frac{\log m}{m}
\tag{24}
\]

uniformly over \(\delta\in(0,1]\) for fixed \(\alpha,\beta>0\). Indeed,
\(P_\delta(a)\ge a\) supplies the discount-free lower loss bound,
\(P_\delta(a)\le P_1(a)\) supplies a feasible upper comparison, and
\(T=S/\beta\) is independent of \(\delta\). Hence even sequences
\(\delta_m\downarrow0\) do not alter the rates in (24).

For \((\alpha,\beta)=(1,.9)\), the ratio
\(m(1-D^*)/\log\log m\) was:

| \(\delta\) | \(10^4\) | \(10^6\) | \(10^8\) | \(10^{10}\) | \(10^{12}\) |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.6428 | 1.5144 | 1.4482 | 1.4069 | 1.3781 |
| .5 | 1.5974 | 1.4838 | 1.4251 | 1.3882 | 1.3624 |
| .01 | 1.5512 | 1.4527 | 1.4016 | 1.3693 | 1.3466 |
| \(10^{-6}\) | 1.5503 | 1.4521 | 1.4011 | 1.3689 | 1.3462 |

All rows drift slowly toward the conjectured coefficient one. For
\(\delta=.5\), the companion ratios \(mV/\log m\) were
\(.7234,.7904,.8289,.8543,.8725\).

The maintained game still excludes \(\delta=0\). At that boundary all
incumbent terminal net payoffs are zero, so terminal acceptance needs a new
tie rule; this exclusion does not weaken the uniform \(\delta\downarrow0\)
rate statement above.

## 7. Reproduction and limitations

Run the nine regression tests:

    PYTHONPATH=announced_escalation_overhaul/code \
    python -m unittest -v \
      announced_escalation_overhaul/code/test_discount_model.py

Run each full deterministic section:

    for section in formulas roots exact thickness; do
      PYTHONPATH=announced_escalation_overhaul/code \
      python announced_escalation_overhaul/code/run_discount_falsification.py \
        --full --section "$section"
    done

The seed is 20260825. Replacing --full with --quick runs a smoke scan.

Numerical patterns are not proofs:

1. The MP enclosure code is interval-style, not a verified
   directed-rounding implementation.
2. No-multiplicity and no-multiple-peak findings apply only to sampled
   regions.
3. Equality in the general critical asymptotic (21) requires a uniform
   argmax/localization proof, although its feasible-menu lower bound already
   refutes the old \(m^4\) claim.
4. General \(\gamma>0\) scans test follower roots and same-first-price menu
   gains. They do not supply a global fresh-entry optimizer theorem.

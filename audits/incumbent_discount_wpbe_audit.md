# Incumbent-driver discounting: WPBE reconstruction and replacement audit

## Verdict and notation

Introduce an incumbent discount factor

\[
 0<\delta_D\le1.
\]

If an incumbent waits, survives, accepts the terminal payment `p_j`, and is
selected, her period-0 payoff is

\[
 \delta_D(p_j-c).
\]

A fresh entrant makes the period-2 comparison `p_j-c` at that date.  The
subscript on `delta_D` avoids confusion with the cutoff displacement
`p-a` used in local proofs.

The arbitrary-menu cutoff WPBE, equilibrium existence/compactness, strict
single crossing, and unique flat numeric cutoff all survive.  The fresh-entry
local theorem also survives and remains strictly positive whenever rescue is
active.  Its correct coefficient is obtained by discounting the incumbent
wait terms, **not** by replacing physical survival `alpha` everywhere.

### Audit against the current TeX

The latest snapshot has now completed almost all of the migration.

- **PASS:** the primitive description, arbitrary-menu WPBE, flat benchmark,
  fresh-entry theorem and its appendix proof, global no-entry reduction and
  its appendix proofs, the new thickness formulas, and the public-count
  benchmark all agree with the independent derivation below.
- **FIXED during audit (logical wording):** activity had been called
  *equivalent* to `rho>t/(t+x E A)`.  Only implication holds; the exact
  equivalence is `rho(1-p)>t/(t+x E A)`.  The latest appendix now correctly
  says that activity implies the weaker displayed bound.
- **FIXED during audit (notation):** equations (20)--(21) now label completion
  `M_m^{alpha,delta,0}`, consistently with (11), (22), and (35).
- **FIXED during audit (conditioning statement):** the sentence following
  (41) now fixes `(m,alpha,delta)`, not only `(m,alpha)`.

There is no remaining substantive discrepancy in the latest snapshot.

Thus the formulas below are both a derivation and a replacement audit.  I use
`delta_D` for the primitive denoted `delta` in the current TeX.

The distinction is fundamental:

- physical terminal supply, rider beliefs, and rider coverage continue to use
  `alpha`;
- an incumbent's period-1 waiting payoff uses `delta_D alpha`;
- fresh entrants are not multiplied by `delta_D` in their terminal acceptance
  condition or in coverage;
- platform completion is not directly discounted.

Consequently, every no-entry scalar derived from cutoff indifference must use
the rescaling below.  The latest main text and appendices now do so.

## 1. Strategies and beliefs that do not change

Fix a menu `0<=p_1<=p_2<=1` and a conjectured incumbent cutoff
`a in [0,p_1]`.  Poisson splitting and Palm conditioning are unaffected by
utility discounting.  Define exactly as in the current paper

\[
 \lambda_j(a)=m\{\alpha(p_j-a)+\gamma p_j\},
 \qquad C_j(a)=1-e^{-\lambda_j(a)},              \tag{D1}
\]

and

\[
 \phi(x)=\begin{cases}(1-e^{-x})/x,&x>0,\\1,&x=0.
 \end{cases}
\]

After failure, the rider's three payoffs remain

\[
 0,\qquad C_1(a)(\beta v-p_1),\qquad
 C_2(a)(\beta v-p_2).
\]

Consequently, if `C_2>C_1`, the repeat--rescue switch is

\[
 v^M(a)=\frac{C_2(a)p_2-C_1(a)p_1}
 {\beta[C_2(a)-C_1(a)]};
\]

if `C_2=C_1`, set `v^M=+infinity`.  Conditional on posting,

\[
 \eta^R(a)=
 \frac{[\min\{v^M(a),1\}-p_1/\beta]^+}{1-p_1},\qquad
 \eta(a)=\frac{[1-v^M(a)]^+}{1-p_1},
\]

and

\[
 \eta^R(a)+\eta(a)=\rho(p_1)
 =\frac{[1-p_1/\beta]^+}{1-p_1}.
\]

The strict-positive repeat--rescue tie is assigned to rescue, while a
zero-valued continuation follows the manuscript's repeat/abandon priority.
None of these objects contains `delta_D`, because they are rider payoffs.

Before posting, the rider's expected payoff is

\[
 (1-e^{-ma})(v-p_1)+e^{-ma}
 \max\{0,C_1(\beta v-p_1),C_2(\beta v-p_2)\}.
\]

It is never positive below `p_1` (and is strictly negative there whenever
initial completion has positive probability) and is nonnegative at and above
`p_1`.  The maintained tie convention therefore gives the stated posting
strategy `v>=p_1`.  Conditional on posting, `v` is uniform on `[p_1,1]`; because
supply and driver actions are independent of `v`, public failure leaves this
posterior unchanged.

Palm conditioning gives a focal incumbent an independent
`Pois(m)` rival count.  Universal rejection says that no rival mark lies
below `a`; independent Poisson increments leave the above-`a` process
unchanged.  Survival and fresh-entry thinning then yield (D1).  These beliefs
and all rider strategies are therefore unchanged by incumbent discounting.

At the terminal driver node:

- a surviving incumbent accepts iff
  `delta_D(p_j-c)>=0`, equivalently iff `c<=p_j`;
- a fresh entrant accepts iff `p_j-c>=0`, also iff `c<=p_j`.

Therefore terminal acceptance, coverage `C_j`, and assignment share
`phi(lambda_j)` do not change.  Discounting changes only the period-0 value
of the incumbent's option to wait.

## 2. Period-1 incumbent payoffs

Immediate acceptance is unchanged:

\[
 A_D(c;a)=\phi(ma)(p_1-c).                       \tag{D2}
\]

Waiting becomes

\[
 \boxed{
 W_D(c;a)=\delta_D\alpha e^{-ma}\left\{
 \eta^R(a)\phi(\lambda_1(a))[p_1-c]^+
 +\eta(a)\phi(\lambda_2(a))[p_2-c]^+
 \right\}.}                                    \tag{D3}
\]

The factor `alpha` is the probability that the focal incumbent survives;
`delta_D` converts a selected terminal surplus to period-0 utility.  Neither
factor belongs inside `lambda_j` as a substitute for the other.

For `c<=p_1`, write

\[
 A_D(c;a)-W_D(c;a)=B_D(a)(p_1-c)-D_D(a),         \tag{D4}
\]

where

\[
 \begin{aligned}
 B_D(a)&=\phi(ma)-\delta_D\alpha e^{-ma}
 \{\eta^R(a)\phi(\lambda_1(a))
   +\eta(a)\phi(\lambda_2(a))\},\\
 D_D(a)&=\delta_D\alpha e^{-ma}\eta(a)
 \phi(\lambda_2(a))(p_2-p_1).
 \end{aligned}                                  \tag{D5}
\]

## 3. Strict single crossing

Because `phi(lambda_j)<=1`, `eta^R+eta=rho<=1`, and
`delta_D alpha<=1`,

\[
 B_D(a)\ge\phi(ma)-\delta_D\alpha e^{-ma}\rho
 \ge\phi(ma)-e^{-ma}\ge0.                      \tag{D6}
\]

For `p_1>0` the inequality is strict:

- if `a>0`, then `phi(ma)>e^{-ma}`;
- if `a=0`, then `rho(p_1)<1`, so
  `delta_D alpha rho<1`.

Hence the accept-minus-wait margin is strictly decreasing in cost on
`[0,p_1]`.  A type above `p_1` rejects because immediate acceptance has
negative expected payoff while waiting is nonnegative.  Thus every symmetric
best response is a genuine cutoff.  Driver discounting strengthens, rather
than weakens, the single-crossing inequality.

## 4. Discounted cutoff margin and all boundary conditions

Define

\[
 \boxed{
 \begin{aligned}
 f_D(a;p_1,p_2)
 ={}&\phi(ma)(p_1-a)\\
 &-\delta_D\alpha e^{-ma}\left\{
 \eta^R(a)\phi(\lambda_1(a))(p_1-a)
 +\eta(a)\phi(\lambda_2(a))(p_2-a)
 \right\}.
 \end{aligned}}                                 \tag{D7}
\]

For `0<p_1<1`, the exact cutoff conditions are

\[
 \begin{array}{c|c|c}
 \text{candidate}&\text{condition}&\text{cutoff-type action}\\ \hline
 a=0&f_D(0)\le0&c=0\text{ rejects},\\
 0<a<p_1&f_D(a)=0&c=a\text{ is indifferent},\\
 a=p_1&f_D(p_1)\ge0&c=p_1\text{ accepts}.
 \end{array}                                    \tag{D8}
\]

At the upper boundary,

\[
 f_D(p_1)=
 -\delta_D\alpha e^{-mp_1}\eta(p_1)
 \phi(\lambda_2(p_1))(p_2-p_1)\le0.            \tag{D9}
\]

Thus upper-boundary eligibility again means equality.  Because
`delta_D>0`, its parameter characterization is unchanged:

\[
 a=p_1\text{ is eligible}
 \quad\Longleftrightarrow\quad
 \alpha\eta(p_1)(p_2-p_1)=0.                   \tag{D10}
\]

At `p_1=0`, the only aggregate cutoff is zero and the lower-boundary action
must be carried explicitly.  At `(p_1,p_2)=(1,1)`, the natural completion of
the off-path subgame remains cutoff one and ex ante completion zero.

## 5. Existence and compactness

The discounted equilibrium set is

\[
 \begin{aligned}
 \mathcal E_D(p_1,p_2)
 ={}&\{0:f_D(0)\le0\}\\
 &\cup\{a\in(0,p_1):f_D(a)=0\}\\
 &\cup\{p_1:f_D(p_1)\ge0\},
 \end{aligned}                                  \tag{D11}
\]

with the separately stated `p_1=0,1` conventions.

For fixed policy, `f_D` is continuous.  It is the original continuous wait
payoff multiplied by the constant `delta_D`; rider interval masses remain
continuous in the cutoff away from null switch types, and the coalescing-price
limits give the same driver payoff under either rider label.  Also
`f_D(p_1)<=0`.  Therefore:

1. if `f_D(0)<=0`, reject-all is an equilibrium;
2. if `f_D(0)>0>f_D(p_1)`, the intermediate value theorem gives an interior
   zero;
3. if `f_D(0)>0=f_D(p_1)`, the upper boundary is an equilibrium.

Endpoint limits of eligible roots remain eligible, so the set is closed in
`[0,p_1]`, hence compact.  The arbitrary-menu existence and compactness
proposition survives with `f_m` replaced by `f_D`.

Completion conditional on any equilibrium cutoff is still

\[
 M(p_1,p_2;a)=(1-p_1)\left[1-e^{-ma}+e^{-ma}
 \{\eta^R(a)C_1(a)+\eta(a)C_2(a)\}\right].     \tag{D12}
\]

There is no `delta_D` in (D12); discounting affects completion only through
the equilibrium cutoff correspondence.

## 6. Flat policy

Set `p_1=p_2=p>0`.  Rescue is a duplicate label, and for every `a<p`,

\[
 f_D(a;p,p)=(p-a)\left[
 \phi(ma)-\delta_D\alpha e^{-ma}\rho(p)
 \phi\bigl(m\{\alpha(p-a)+\gamma p\}\bigr)
 \right]>0.                                     \tag{D13}
\]

The proof is exactly the strict single-crossing bound in (D6).  Hence no
cutoff below `p` is sustainable, while `a=p` is an upper-boundary equilibrium.
The unique numeric cutoff remains

\[
 \boxed{a=p.}                                   \tag{D14}
\]

After a flat-price failure, surviving incumbents have costs above `p` and do
not accept the same payment later.  Only fresh entrants can complete.  Thus
the flat completion function and its optimizer are **unchanged**:

\[
 Q^F_\gamma(m,p)
 =(1-p)(1-e^{-mp})
 +e^{-mp}[1-p/\beta]^+(1-e^{-\gamma mp}),       \tag{D15}
\]

and `F^*_gamma(m)=max_p Q^F_gamma(m,p)`.

## 7. Fresh-entry local equilibrium

Fix `0<p<beta` and the nearby menu `(p,p+epsilon)`.  Retain the current
physical-supply notation

\[
 x=mp,\quad R=e^{-x},\quad E=e^{-\gamma x},\quad
 \sigma=\phi(x),\quad \ell=\phi(\gamma x),\quad
 \rho=\frac{1-p/\beta}{1-p}.                    \tag{D16}
\]

The limiting rider switch and active rescue mass are unchanged:

\[
 \bar v=\frac1\beta\left[p+
 \frac{1-E}{mE(\alpha+\gamma)}\right],
 \qquad
 \eta^0=\frac{1-\bar v}{1-p}.                  \tag{D17}
\]

This is an important nonreplacement: `alpha+gamma` in (D17) is physical
supply and must **not** become `delta_D alpha+gamma`.

Let `d_epsilon=p-a_epsilon`.  The two physical terminal intensities remain

\[
 \lambda_1=m(\alpha d_\varepsilon+\gamma p),
 \qquad
 \lambda_2=\lambda_1+m(\alpha+\gamma)\varepsilon. \tag{D18}
\]

If `eta_epsilon` is rescue mass, an interior discounted cutoff solves

\[
 \begin{aligned}
 \phi(ma)d_\varepsilon
 =\delta_D\alpha e^{-ma}\{&
 (\rho-\eta_\varepsilon)\phi(\lambda_1)d_\varepsilon\\
 &+\eta_\varepsilon\phi(\lambda_2)
 (d_\varepsilon+\varepsilon)\}.
 \end{aligned}                                  \tag{D19}
\]

### Uniform localization

Rearrange (D19).  The coefficient on `d_epsilon` is at least

\[
 e^{-ma}(1-\delta_D\alpha\rho)>0.
\]

The right side is at most
`delta_D alpha e^{-ma} rho epsilon`.  The same weak inequality handles a
reject-all candidate.  Hence every equilibrium cutoff satisfies

\[
 \boxed{
 0\le p-a_\varepsilon
 \le\frac{\delta_D\alpha\rho}
 {1-\delta_D\alpha\rho}\varepsilon.}           \tag{D20}
\]

Thus discounting tightens the localization bound.

### Cutoff response

On the compact rescaling
`y=(p-a_epsilon)/epsilon`, the rider switch still converges to `bar v` and
rescue mass to `eta^0`.  Dividing (D19) by `epsilon` gives the affine limit

\[
 [\sigma-R\delta_D\alpha\rho\ell]y
 -R\delta_D\alpha\eta^0\ell=0.                \tag{D21}
\]

Its slope satisfies

\[
 \sigma-R\delta_D\alpha\rho\ell>sigma-R>0.
\]

Consequently, when `bar v<1`, the unique small-escalation cutoff has

\[
 \boxed{
 a_\varepsilon=p-\kappa_D\varepsilon+o(\varepsilon),
 \qquad
 \kappa_D=
 \frac{R\delta_D\alpha\ell\eta^0}
 {\sigma-R\delta_D\alpha\rho\ell}.}           \tag{D22}
\]

The `C^1` rescaled-margin argument proving uniqueness is unchanged.  If
`alpha=0`, then `kappa_D=0` and the cutoff remains `p`, although fresh-entry
coverage can still make rescue valuable.  If `bar v>1`, rescue is locally
inactive and the unique cutoff is exactly `p`.  The knife edge `bar v=1`
still requires a second-order expansion.

For fixed primitives with `alpha eta^0>0`, `kappa_D` is increasing in
`delta_D`; discounting reduces strategic waiting and keeps the cutoff closer
to the flat cutoff.

## 8. Fresh-entry completion derivative

Physical continuation coverage remains

\[
 S_\varepsilon=\rho C_1+
 \eta_\varepsilon(C_2-C_1).
\]

Along `a_epsilon=p-kappa_D epsilon+o(epsilon)`, its derivative is

\[
 S'_0=mE\{\rho\alpha\kappa_D+
 \eta^0(\alpha+\gamma)\}.                      \tag{D23}
\]

Notice that both occurrences of `alpha` in (D23) are physical survival
effects and are **not** multiplied by `delta_D`.

Define the unchanged physical cutoff-loss coefficient

\[
 B_m=1-\rho+\rho E(1-\alpha).                  \tag{D24}
\]

Direct differentiation of platform completion gives

\[
 L_D=m(1-p)R\left[
 E(\alpha+\gamma)\eta^0-\kappa_D B_m
 \right].                                      \tag{D25}
\]

Substitute (D22).  The exact factorization is

\[
 \boxed{
 L_D=m(1-p)R\eta^0
 \frac{T_D}{\sigma-R\delta_D\alpha\rho\ell},} \tag{D26}
\]

where

\[
 \boxed{
 T_D=E(\alpha+\gamma)\sigma
 -R\delta_D\alpha\ell
 \{1-\rho+\rho E(1+\gamma)\}.}                \tag{D27}
\]

The algebra uses

\[
 E(\alpha+\gamma)\rho+B_m
 =1-\rho+\rho E(1+\gamma).
\]

### Positivity

First note the monotonic reduction.  Let `T_1` denote (D27) evaluated at
`delta_D=1`.  The bracket

\[
 1-\rho+\rho E(1+\gamma)
\]

is positive.  Therefore

\[
 T_D=T_1+(1-\delta_D)R\alpha\ell
 \{1-\rho+\rho E(1+\gamma)\}>0.                \tag{D28}
\]

All other factors in (D26) are positive under active rescue.  Hence the
fresh-entry local theorem remains true for every `0<delta_D<=1`, with (D20),
(D22), and (D27) replacing the current formulas.  Incumbent discounting can
only improve the sign margin relative to the undiscounted-driver case.

For completeness, here is an independent proof that `T_1>0`; no displayed
positivity claim in the manuscript is being assumed.  If `gamma=0`, activity
and `alpha+gamma>0` imply `alpha>0`, and

\[
 T_1=\alpha(\sigma-R)>0
\]

by `e^x>1+x`.  Now let `gamma>0`, and put

\[
 u=e^x-1,\quad t=1-E,\quad A=\alpha+\gamma,\quad
 \Delta=1-E(1+\gamma),\quad
 B=1-\rho\Delta.
\]

Since `sigma=Ru/x` and `ell=t/(gamma x)`, the sign of `T_1` is the sign of

\[
 Q=E\gamma A u-\alpha tB.                       \tag{D28a}
\]

There are three exhaustive regions.

1. If `Delta<=0`, then `B<=E(1+gamma)`, while `gamma u>t` and
   `A>=alpha(1+gamma)` because `alpha<=1`.  Hence
   `Q>=E{gamma A u-alpha t(1+gamma)}>0`.
2. If `Delta>0` and `0<gamma<=1`, convexity gives
   `e^(gamma x)<=1+gamma(e^x-1)`, or `t<=E gamma u`.  Since
   `B<=1`,
   `Q>=alpha(E gamma u-t)+E gamma^2 u>0`.
3. Suppose `Delta>0` and `gamma>1`.  The activity condition `bar v<1`
   implies

   \[
    \rho>\frac{t}{t+xEA}.                       \tag{D28b}
   \]

   Indeed, with `s=(beta-p)/beta=rho(1-p)`, activity is
   `t/(xEA)<s/(1-s)`, and `rho>s`.  Since `B=1-rho Delta`, (D28b) gives

   \[
    Q\ge\frac{E}{t+xEA}I(\alpha),\qquad
    I(\alpha)=\gamma Au(t+xEA)
      -\alpha t\{xA+t(1+\gamma)\}.              \tag{D28c}
   \]

   The coefficient on `alpha^2` in `I` is
   `x{gamma E u-t}<0`, because for `gamma>1`, strict convexity gives
   `e^(gamma x)-1>gamma(e^x-1)`.  Thus `I` is concave on `[0,1]`, so it
   suffices to check its endpoints.  Clearly
   `I(0)=gamma^2 u(t+xE gamma)>0`.  At `alpha=1`, let
   `H=t+xE(1+gamma)` and `d=gamma u-t`.  Then

   \[
    \frac{I(1)}{1+\gamma}=dH-tx\Delta.           \tag{D28d}
   \]

   Write `y=gamma x`.  Here `Delta>0` implies
   `y>log(1+gamma)`.  On this half-line
   `Delta=1-(1+gamma)e^(-y)<y/2`: the minimum of
   `y/2-1+(1+gamma)e^(-y)` occurs at
   `log(2(1+gamma))` and is positive for `gamma>1`.
   Also `u>x+x^2/2` and `t<gamma x`, so
   `d>gamma x^2/2=xy/2>x Delta`.  Since `H>t`, (D28d) is positive.
   Hence both endpoints, and therefore every `I(alpha)`, are positive.

This proves `T_1>0` in all cases.  Equation (D28) then proves
`T_D>0` for every `0<delta_D<=1`.  Activity remains essential when
`gamma>1`; discounting weakens the negative term but does not make an
unconditional sign claim valid.

At `gamma=0`, `E=ell=1`, `eta^0=rho`, and the local formulas reduce to

\[
 \kappa_D=
 \frac{R\delta_D\alpha\rho}
 {\sigma-R\delta_D\alpha\rho},                 \tag{D29}
\]

and

\[
 \boxed{
 L_D=
 \frac{m(1-p)R\alpha\rho
 (\sigma-\delta_D R)}
 {\sigma-R\delta_D\alpha\rho}>0.}             \tag{D30}
\]

## 9. No-entry global section: derivation and verification

The global reduction uses a cancellation between an incumbent's wait payoff
and physical terminal coverage.  Driver discounting scales that cancellation
by `delta_D`; it is not innocuous.  Equations (17)--(42) and their latest
appendix proofs agree with the derivation below, subject to two notation
repairs listed after (D40).

Keep the current no-entry definitions

\[
 C(x)=1-e^{-\alpha m x},\quad h(a)=\frac{e^{ma}-1}{a},
 \quad K_{p,q}(a)=
 \frac{\max\{A_p(a),A_q(a)\}}{\beta(1-p)}.
\]

The sign-equivalent cutoff scalar is

\[
 \boxed{
 \mathcal D^D_{p,q}(a)=(p-a)h(a)-\delta_D K_{p,q}(a).}     \tag{D31}
\]

The repeat-branch inequality strengthens to

\[
 (p-a)h(a)>
 \delta_D\frac{A_p(a)}{\beta(1-p)}.             \tag{D32}
\]

At an active zero,

\[
 u h(a)=\delta_D\frac{b}{B}C(z).
\]

Thus `u<delta_D C(z)/m<=C(z)/m`; the current logarithmic-derivative proof
still makes every zero a strict downward crossing.  Global numeric-cutoff
uniqueness therefore survives.

### Modified completion identity

No-entry physical coverage satisfies

\[
 \alpha\phi(m\alpha(p_j-a))(p_j-a)=\frac{C_j(a)}m.
\]

Discounted cutoff indifference is consequently

\[
 \phi(ma)(p-a)=
 \frac{\delta_D e^{-ma}}m K_{p,q}(a).
\]

At a positive equilibrium,

\[
 e^{-ma}K_{p,q}(a)=
 \frac{m\phi(ma)(p-a)}{\delta_D}.
\]

The discounted equation (20), correctly shown in the latest main text, is

\[
 \boxed{
 M_D(p,q;a)=(1-p)m\phi(ma)
 \left[a+\frac{p-a}{\delta_D}\right],
 \qquad a>0.}                                  \tag{D33}
\]

At a reject-all equilibrium, actual completion remains

\[
 M_D(p,q;0)=
 \left(1-\frac q\beta\right)(1-e^{-\alpha m q}),
\]

but its equilibrium lower bound becomes

\[
 M_D(p,q;0)\ge
 \frac{(1-p)mp}{\delta_D}.                     \tag{D34}
\]

The expression in (D33) is strictly decreasing in a positive cutoff: both
`phi(ma)` and

\[
 a+\frac{p-a}{\delta_D}
 =\frac p{\delta_D}-
 \frac{1-\delta_D}{\delta_D}a
\]

are nonincreasing, and `phi` is strictly decreasing.  A strict-menu cutoff
below `p` therefore still gives strictly more completion than the same flat
first payment.  The optimized-flat dominance argument survives.

### Fixed-p and outer scalar replacements

The physical rescue envelope `Q(a)` and `S(a)` is unchanged.  Define

\[
 p_{z,D}=\frac{1-
 \sqrt{1-4\delta_D S_0/(\beta m)}}2.             \tag{D35}
\]

Reject-all is feasible exactly in the corresponding lower region
`p<=p_{z,D}`.  The positive-cutoff tangent equation becomes

\[
 \boxed{
 (p-a)h(a)=
 \frac{\delta_D S(a)}{\beta(1-p)}.}             \tag{D36}
\]

Equivalently, if the current paper uses

\[
 R(a)=\frac{S(a)}{\beta h(a)},
\]

then

\[
 (1-p)(p-a)=\delta_D R(a).                     \tag{D37}
\]

The lower branch becomes

\[
 \boxed{
 P_D(a)=\frac{1+a-
 \sqrt{(1-a)^2-4\delta_D R(a)}}2.}              \tag{D38}
\]

The outer completion scalar must be

\[
 \boxed{
 J_D(a)=
 (1-P_D(a))m\phi(ma)
 \left[a+\frac{P_D(a)-a}{\delta_D}\right].}    \tag{D39}
\]

At zero, its continuous extension is

\[
 J_D(0)=\frac{m p_{z,D}(1-p_{z,D})}{\delta_D}
 =\frac{S_0}{\beta}.                            \tag{D40}
\]

The latest main-text equations (20)--(21) now write
`M_m^{alpha,delta,0}`, and the sentence following (41) now fixes
`(m,alpha,delta)`.  These two notation inconsistencies found during the audit
have been repaired.

At `a=beta`, it equals the flat endpoint value.  The envelope one-crossing,
lower-branch, fixed-`p` maximum, and compact outer-attainment arguments retain
their structure with (D35)--(D40).  In the thickness notation of the current
equations (49)--(50), replace

\[
 B_m(a)\quad\text{by}\quad
 B_{m,D}(a)=\delta_D B_m(a),\qquad
 P_{m,D}(a)=
 \frac{1+a-\sqrt{(1-a)^2-4B_{m,D}(a)}}2
\]

and replace the old scalar by

\[
 J_{m,D}(a)=m(1-P_{m,D}(a))\phi(ma)
 \left[a+\frac{P_{m,D}(a)-a}{\delta_D}\right]. \tag{D40a}
\]

The old thin-market coefficients cannot be carried over.  The latest snapshot
has correctly re-expanded them.  For example, uniformly as `m` tends to zero,

\[
 B_{m,D}(a)\longrightarrow
 \frac{\delta_D\alpha(\beta-a)^2}{4\beta},
\]

but the leading objective is no longer `P_0(1-P_0)`.  It is

\[
 (1-P_{0,D}(a))
 \left[a+\frac{P_{0,D}(a)-a}{\delta_D}\right]. \tag{D40b}
\]

This already proves the abstract's claimed order change when
`beta>1/2` and `delta_D<1`.  Let the expression in (D40b) be `H_D(a)`.
The limiting map `P_{0,D}` is continuous and strictly increasing from a
point below `1/2` to `beta>1/2`, so there is a unique `a_hat<1/2` with
`P_{0,D}(a_hat)=1/2`.  At that point,

\[
 H_D(a_{\rm hat})
 =\frac14+\frac12\left(\frac1{\delta_D}-1\right)
   \left(\frac12-a_{\rm hat}\right)>\frac14.    \tag{D40b'}
\]

Uniform convergence of `J_{m,D}/m` to `H_D` and of the flat value divided by
`m` to `1/4` therefore gives the rigorous first-order statement

\[
 \frac{V_{\alpha,\delta_D,0}(m)}m\longrightarrow
 \max_{a\in[0,\beta]}H_D(a)-\frac14>0
 \qquad(m\downarrow0).                         \tag{D40b''}
\]

At `delta_D=1`, `H_D=P_0(1-P_0)` and this first-order coefficient vanishes,
which is why the old second-order calculation applies only on that boundary.

The latest `beta=1/2` expansion also checks independently.  Put
`a=1/2-cm`.  The envelope equation gives

\[
 z=\frac{\alpha c}{2}m^2+O(m^4),\quad
 T_m=\frac{\alpha c^2}{2}m^3+O(m^5),\quad
 P_{m,D}=a+\delta_D\alpha c^2m^2+O(m^3).
\]

Substitution in the exact objective gives

\[
 J_{m,D}=\frac m4-\frac{m^2}{16}
 +m^3\left\{\frac1{96}+\frac c8-
 \left[1-\frac{\alpha(1-\delta_D)}2\right]c^2\right\}
 +O(m^4).
\]

Thus the current maximizing
`c^*=1/[16{1-alpha(1-delta_D)/2}]` and cubic gain coefficient
`alpha(1-delta_D)/[512{1-alpha(1-delta_D)/2}]` are correct.  For
`beta<1/2`, the current uniform upper bound on `H_D` is also valid and leaves
a strict gap below `1/4`.

The thick-market identity is a useful exception.  Let `x=ma`, let
`T_m=S(a)/beta` be the current physical envelope object, and let
`p=P_{m,D}(a)`.  The discounted implementation equation is

\[
 (1-p)(p-a)=\delta_D\frac{aT_m}{e^x-1}.
\]

Substitution into (D40a) gives exactly

\[
 J_{m,D}=(1-p)(1-e^{-x})+T_m e^{-x},\qquad
 1-J_{m,D}=p(1-e^{-x})+(1-T_m)e^{-x}.            \tag{D40c}
\]

Thus the current thick-market loss identity survives in form after replacing
`P_m` by `P_{m,D}`;
the lower-bound argument for the thick rate is unchanged, and the same
feasible scale gives the upper bound for each fixed `delta_D>0`.  The
`(log m)/m` optimized-gain rate therefore survives.  The latest thickness
theorem uses (D40a)--(D40c) and the new leading objective (D40b), and passes
this audit.

The patience-threshold theorem does survive for fixed `delta_D>0`.  A higher
rider patience raises the active coverage coefficient, the unique cutoff
moves left, and (D33) decreases with the cutoff; at a zero cutoff the value
`(1-q/beta)C(q)` increases strictly.  Joint continuity follows after the
same fixed-coordinate change `a=beta x`, because (D38)--(D40) have continuous
endpoint extensions and a uniformly positive discriminant.  Thus, with

\[
 \beta_c(m,\alpha,\delta_D)
 :=\inf\{\beta:D^*_{\alpha,\delta_D,0}(m;\beta)>F_0^*(m)\},
\]

the strict-gain set is the same kind of open upper interval, and

\[
 0<-\frac1m\log(1-F_0^*(m))
 \le\beta_c(m,\alpha,\delta_D)\le p_F(m)<\frac12.
\]

The scalar test uses `max_a J_D(a)>F_0^*(m)`.  The bounds are unchanged: the
lower one is physical, while for `beta>p_F` a strict menu at `p_F` beats the
same flat payment by (D33).  The threshold itself generally depends on
`delta_D` and must not be written as `beta_c(m,alpha)` unless discounting is
fixed in the notation.

## 10. Public known-n benchmark replacements

If the deterministic public-count benchmark remains in scope, its incumbent
wait payoff also receives `delta_D`.  Cutoff indifference becomes

\[
 s_n(a)(p_1-a)=
 \delta_D(1-a)^{n-1}\alpha
 \sum_j\eta_j(a)s_n(\theta_j(a))(p_j-a).        \tag{D41}
\]

Using the unchanged physical coverage identity gives

\[
 \boxed{
 M_{n,D}(p_1,p_2;a)=
 (1-p_1)n s_n(a)
 \left[a+\frac{p_1-a}{\delta_D}\right].}       \tag{D42}
\]

The local cutoff coefficient becomes

\[
 \boxed{
 \kappa_{n,D}=
 \frac{\delta_D(1-p)^{n-1}\alpha\rho}
 {s_n(p)-\delta_D(1-p)^{n-1}\alpha\rho}.}      \tag{D43}
\]

Differentiating (D42) gives

\[
 \boxed{
 \left.\frac{dM_{n,D}}{d\varepsilon}\right|_{0+}
 =-(1-p)n\kappa_{n,D}\left[
 p s_n'(p)+\left(1-\frac1{\delta_D}\right)s_n(p)
 \right].}                                     \tag{D44}
\]

For `n>=2` and `alpha>0`, this is strictly positive.  At `n=1`, it is zero
when `delta_D=1`, but strictly positive when `delta_D<1` and `alpha>0`.
Thus the known-one interpretation changes under incumbent discounting.  The
latest main text and appendix now record exactly this distinction.

## 11. Formula-by-formula replacement map for the current TeX

Using the equation labels in
`announced_escalation_theory_overhaul.tex`:

| Current item | Discounted-driver action |
|---|---|
| Model primitives | **Already correct:** the current text distinguishes incumbent `delta_D(p_j-c)` from a fresh entrant's contemporaneous payoff. |
| (1)--(4) | Unchanged. |
| (5) | **Already correct:** the current main text multiplies the entire incumbent wait payoff by driver `delta`. |
| (6) | **Already correct:** current `B,D` agree with (D5), and the appendix displays the sharp `delta alpha rho` bound. |
| (7)--(8) | **Already correct:** current `f_m` agrees with (D7); equilibrium-set form is unchanged. |
| Upper-boundary display below (8) | **Already correct:** it contains `delta`; eligibility characterization is unchanged because `delta>0`. |
| (9)--(13) | **Already correct:** completion and flat objective are not discounted; flat cutoff remains `p`. |
| (L1)--(L2) | Unchanged physical-supply and rider objects. |
| (L3)--(L6), main text | **Already correct** in the current snapshot and agree with (D20), (D22), and (D26)--(D27). |
| Appendix (A1)--(A6) | **Now correct** after renaming displacement to `d`, inserting driver `delta`, and stating activity as implying the weaker bound used in the proof. |
| Global (14)--(16), (25)--(28) | Physical coverage/envelope objects unchanged. |
| Global (17)--(19), main text | **Already correct** in the latest snapshot and agree with (D31)--(D32); (18) is an unchanged stronger inequality. |
| Global (20)--(24), main text | **Now correct** and agree with (D29)--(D34), including `delta` in the superscript of `M`. |
| Global (29)--(35), main text | **Already correct** and agree with (D35)--(D40). |
| Patience (39)--(42), main text | **Now correct:** the threshold and the fixed-parameter statement both include `delta`. |
| Global-design appendix | **Now correct:** it uses `/delta_D`, the bound `(1-p)mp/delta_D`, the discounted envelope, and `R_D,P_D,J_D`. |
| Thickness (43)--(56) | **Now correct:** the lower root and objective agree with (D40a), the thin limit with (D40b), the `beta=1/2` expansion checks directly, and the thick identity is (D40c). |
| Known-n physical identities (57)--(58) | Unchanged. |
| Known-n (59)--(62) | **Now correct** and agree with (D41)--(D44); the appendix has also been updated. |

## 12. Final assessment

1. **General cutoff WPBE:** valid after multiplying only incumbent waiting
   payoffs by `delta_D`; beliefs and rider strategies are unchanged.
2. **Single crossing:** remains strict and becomes easier.
3. **Existence and compactness:** unchanged in structure, with discounted
   cutoff margin `f_D`.
4. **Flat policy:** unique numeric cutoff and completion benchmark are
   unchanged.
5. **Fresh-entry local theorem:** remains valid and strictly positive under
   the same active condition.  The correct replacements are (D20), (D22),
   and (D26)--(D27).
6. **Global no-entry design:** qualitative one-crossing, fixed-price, lower-
   branch, attainment, and same-flat dominance arguments survive with
   (D33)--(D40); the latest substantive formulas pass.
7. **Endpoint asymptotics and public-n benchmark:** materially affected, but
   the latest replacements pass the independent checks above.  The three
   discrepancies found during the audit have been repaired in the current
   snapshot.

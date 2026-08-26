# Red-team audit of `thickness_topology.md`

## Scope and verdict

This audit treats the exact no-entry scalar reduction in
`global_noentry_geometry.md` as an input and attacks the downstream thickness
claims without using a finite grid as proof.  Numerical calculations were used
only as falsification checks.

The short verdict is:

| target claim | verdict | principal qualification |
|---|---|---|
| Thin market, \(\beta>1/2\) | **CAN ENTER** | Add one sentence establishing a uniformly positive limiting discriminant before invoking uniform Taylor expansion. |
| Critical layer, \(\beta=1/2\) | **NEEDS A SHORT REPAIR** | The coefficient \(\alpha/2048\) is correct, but the current jump from \(\delta=O(m)\) to \(\delta=cm+dm^2\) does not prove the optimized remainder. A uniform rescaled-argmax argument below repairs it. |
| Thin market, \(\beta<1/2\) | **CAN ENTER** | The conclusion is exact equality on a nonempty interval, not merely an asymptotic statement. |
| Thick-market matching rates | **CAN ENTER for fixed primitives** | The lower bound is uniform over all policy cutoffs. It is not uniform as \(\alpha\downarrow0\) or \(\beta\downarrow0\) jointly with \(m\). |
| Value continuity and policy attainment | **CAN ENTER** | Berge directly proves the scalar argmax properties. The stated upper hemicontinuity of the *full original-menu* optimizer correspondence needs a direct argument or narrower wording. |

No exact counterexample was found to the five substantive value claims.  One
genuine overreach is parameter-uniform interpretation of the thick-market
rate; an explicit varying-\(\alpha\) counterexample is given below.  A second
issue is a proof gap, rather than a false coefficient, in the critical
boundary-layer optimization.

## 1. Patient thin markets: \(\beta>1/2\)

### 1.1 Limiting policy geometry

The envelope equation implies, uniformly for \(a\in[0,\beta]\),

\[
 y_m(a)\longrightarrow\frac{\beta-a}{2},
 \qquad
 B_m(a)\longrightarrow
 B_0(a)=\frac{\alpha(\beta-a)^2}{4\beta}.
\]

The limiting lower root \(P_0(a)\) solves

\[
 (1-P_0)(P_0-a)=B_0(a).
\]

The discriminant remains uniformly separated from zero.  A convenient
certificate is the limiting analogue of Lemma 1: with
\(Q_0(a)=(a+\beta)/2\),

\[
 B_0(a)< (1-Q_0(a))(Q_0(a)-a),
 \qquad 0\le a<\beta,
\]

and at \(a=\beta\) the discriminant is \((1-\beta)^2>0\).  Continuity and
compactness then give a positive uniform minimum.  This justifies uniform
Taylor expansion of the lower square-root branch; pointwise strictness for
each \(m>0\) alone would not have been enough.

The map \(P_0\) is strictly increasing.  For \(\beta>1/2\), its unique
crossing of \(1/2\) is \(a_0\in(0,1/2)\), characterized exactly by

\[
 \alpha(\beta-a_0)^2=\beta(1-2a_0).              \tag{R1}
\]

Thus the leading objective

\[
 H_0(a):=P_0(a)(1-P_0(a))
\]

has the unique maximizer \(a_0\).

### 1.2 Uniform argmax audit

Uniformly on \([0,\beta]\),

\[
 H_m(a):=\frac{J_m(a)}m
 =H_0(a)+m h_1(a)+o(m).
\]

At \(a_0\), the contribution from the first-order movement of \(P_m\)
vanishes because

\[
 \frac{d}{dp}\{p(1-p)\}\bigg|_{p=1/2}=0.
\]

Only the expansion \(\phi(ma)=1-ma/2+O(m^2)\) remains, giving

\[
 h_1(a_0)=-\frac{a_0}{2}\frac14=-\frac{a_0}{8}. \tag{R2}
\]

The uniform argmax conclusion is valid.  To make the value step explicit, if
\(a_m\) is any maximizer, uniqueness of the maximizer of \(H_0\) gives
\(a_m\to a_0\).  Optimality relative to \(a_0\) then gives

\[
 H_0(a_m)-H_0(a_0)=o(m),
\]

so

\[
 D^*(m)=\frac m4-\frac{a_0}{8}m^2+o(m^2).
\]

The flat expansion

\[
 F^*(m)=\frac m4-\frac1{16}m^2+o(m^2)
\]

is standard and follows directly from the unique flat first-order condition.
Therefore

\[
 \boxed{
 V(m)=\frac{1-2a_0}{16}m^2+o(m^2)
 =\frac{\alpha(\beta-a_0)^2}{16\beta}m^2+o(m^2).} \tag{R3}
\]

The second equality is exactly (R1).  The coefficient is positive because
\(a_0<1/2\).

**Verdict:** the claim and constant are correct and can enter.  The recommended
addition is the compactness argument giving a uniformly positive limiting
discriminant.

## 2. Critical patience: \(\beta=1/2\)

### 2.1 Algebraic coefficient audit

Put \(a=1/2-\delta\).  The limiting objective has a quadratic boundary loss:

\[
 \frac14-P_0(a)(1-P_0(a))=\delta^2+O(\delta^3).  \tag{R4}
\]

The first finite-\(m\) tilt is \(m\delta/8\), so the proposed scale
\(\delta\asymp m\) is correct.

On setting \(\delta=cm+dm^2\), the displayed expansion in the target note is
algebraically consistent.  Its \(m^2\) coefficient is

\[
 f_2(c)=\frac1{96}+\frac c8-c^2
 =\frac{11}{768}-\left(c-\frac1{16}\right)^2,   \tag{R5}
\]

with unique maximizer \(c_0=1/16\).  At \(c_0\), the coefficient multiplying
\(d\) is

\[
 \frac18-2c_0=0,                                 \tag{R6}
\]

and the next coefficient is

\[
 -\frac1{768}-\frac{c_0}{24}+\frac{c_0^2}{4}
 +2\alpha c_0^3
 =-\frac3{1024}+\frac{\alpha}{2048}.             \tag{R7}
\]

The flat coefficient is \(-3/1024\).  Thus, **conditional on legitimate
optimization of the expansion**, the cancellation and the claimed coefficient
are exact:

\[
 V(m)=\frac{\alpha}{2048}m^4+o(m^4).             \tag{R8}
\]

Independent high-precision falsification checks agree with (R8), including
for very small \(\alpha\), but those calculations are not part of the proof.

### 2.2 The actual gap in the written proof

The target note states that every optimizer has \(\delta=O(m)\), and then
writes \(\delta=cm+dm^2\).  The first assertion alone does not imply that the
optimizer admits such an expansion with bounded \(d\).  In particular, it
does not by itself rule out

\[
 \delta/m=c_0+m^{1/2},
\]

whose loss in (R5) is of the same order as the \(m^3\) coefficient being
reported for \(H_m=J_m/m\).  Cancellation of the formal \(d\)-coefficient is
helpful but is not a substitute for a uniform optimized-remainder argument.

### 2.3 Short rigorous repair

The gap is repairable without solving for the second-order displacement.

First, uniform smooth expansion on the fixed interval gives

\[
 H_m(a)=H_0(a)+m h_1(a)+O(m^2).                  \tag{R9}
\]

Near \(a=1/2\), (R4) gives

\[
 H_0(1/2)-H_0(1/2-\delta)\ge c_1\delta^2,
\]

while smoothness gives

\[
 |h_1(1/2-\delta)-h_1(1/2)|\le c_2\delta.
\]

Comparing any maximizer with the feasible endpoint \(a=1/2\) yields

\[
 c_1\delta_m^2\le c_2m\delta_m+c_3m^2,
\]

and hence \(\delta_m=O(m)\).  A fixed leading gap handles points away from
the endpoint.

Now put \(c=\delta/m\), which lies in a fixed compact interval for every
optimizer.  Analyticity of the exact formulas on that rescaled compact set
gives, uniformly in bounded \(c\),

\[
 H_m(1/2-cm)
 =\frac14-\frac m{16}
 +m^2 f_2(c)+m^3 f_3(c)+O(m^4),                 \tag{R10}
\]

where

\[
 f_3(c)=-\frac1{768}-\frac c{24}+\frac{c^2}{4}
 +2\alpha c^3.                                   \tag{R11}
\]

Because (R5) is an exact strictly concave quadratic and \(f_3\) is Lipschitz
on the compact localization set,

\[
 \max_c\{f_2(c)+m f_3(c)+O(m^2)\}
 =f_2(c_0)+m f_3(c_0)+O(m^2).                   \tag{R12}
\]

For example, the upper bound follows from

\[
 f_2(c)+m f_3(c)
 \le f_2(c_0)-(c-c_0)^2
 +m f_3(c_0)+mL|c-c_0|,
\]

whose last two displacement terms have maximum \(O(m^2)\).  Evaluation at
\(c_0\) gives the matching lower bound.  Equations (R7), (R10)--(R12), and the
flat expansion prove (R8) with a valid optimized remainder.

**Verdict:** the coefficient is correct, but the present proof should not enter
unchanged.  The rescaled compact-argmax repair above is sufficient; this is a
closed proof gap, not an open mathematical question.

## 3. Impatient thin markets: \(\beta<1/2\)

Here \(P_0(a)\le P_0(\beta)=\beta<1/2\).  Since \(P_0\) is increasing and
\(p(1-p)\) is increasing below \(1/2\),

\[
 \max_{a\in[0,\beta]}P_0(a)(1-P_0(a))
 =\beta(1-\beta)<\frac14.                       \tag{R13}
\]

Uniform convergence of \(J_m(a)/m\) to the left side of (R13) preserves a
fixed leading-order gap from the unrestricted flat value, whose normalized
limit is \(1/4\).  Also the unique flat optimizer satisfies
\(p_F(m)\to1/2\), so \(p_F(m)>\beta\) for all sufficiently small \(m\).
Consequently the restricted flat term \(p\in[\beta,1]\) in the exact outer
reduction contains the unrestricted flat optimizer, while the entire cutoff
term is strictly smaller.  Therefore

\[
 \boxed{D^*(m)=F^*(m),\qquad V(m)=0}
\]

for every \(m\) in some interval \((0,m_0(\alpha,\beta))\).

**Verdict:** correct and manuscript-ready.  This is an exact equality because
the flat policy remains in the feasible policy class; uniform convergence is
being used to identify which of two attained maxima wins, not to replace an
exact objective by an approximation.

## 4. Thick markets

### 4.1 Exact loss identity

With \(x=ma\), the implementation equation gives

\[
 (1-p)(p-a)=\frac{aT}{e^x-1}.
\]

Substituting it into \(J=m p(1-p)\phi(x)\) yields exactly

\[
 J=(1-p)(1-e^{-x})+Te^{-x},
\]

and hence

\[
 \boxed{1-J=p(1-e^{-x})+(1-T)e^{-x}.}            \tag{R14}
\]

Both losses are nonnegative.  This identity checks out.

### 4.2 Feasible upper bound

Take \(x=\log\log m\), \(a=x/m\).  Uniformly for this candidate,

\[
 q-a\le\frac{\log(1+\alpha m\beta)}{\alpha m},
\]

so \(q=O(\log m/m)=o(1)\), \(y=\beta-q\sim\beta\), and

\[
 p-a=O(ae^{-x}).                                  \tag{R15}
\]

Moreover

\[
 1-T=\frac q\beta+
 \frac{y}{\beta(1+\alpha my)}
 =O(\log m/m).                                    \tag{R16}
\]

Using \(e^{-x}=1/\log m\) in (R14),

\[
 1-J
 =\left(1+o(1)\right)\frac{\log\log m}{m}
 +O(1/m).
\]

Thus

\[
 1-D^*(m)\le(1+o(1))\frac{\log\log m}{m}.       \tag{R17}
\]

The leading constant one is correctly retained.

### 4.3 Policy-uniform lower bound

Split the entire cutoff domain by \(q\le\beta/2\) versus
\(q>\beta/2\).

If \(q\le\beta/2\), then \(y\ge\beta/2\), and the envelope identity gives

\[
 q\ge\frac{\log(1+\alpha m\beta/2)}{\alpha m}.
\]

Since \(1-T\ge q/\beta\), \(p\ge a=x/m\), (R14) implies, uniformly over
every such policy cutoff,

\[
 m(1-J)\ge x(1-e^{-x})+C_m e^{-x},
 \qquad
 C_m=\frac{\log(1+\alpha m\beta/2)}{\alpha\beta}. \tag{R18}
\]

The right side is

\[
 g_{C_m}(x)=x+(C_m-x)e^{-x}.
\]

Its unique minimizer \(r_m\) satisfies

\[
 e^{r_m}=1+C_m-r_m,
\]

and

\[
 \min_x g_{C_m}(x)=r_m+1-e^{-r_m}
 \sim\log C_m\sim\log\log m.                    \tag{R19}
\]

If \(q>\beta/2\), the uniform bound

\[
 q-a\le\frac{\log(1+\alpha m\beta)}{\alpha m}=o(1)
\]

gives \(a>\beta/4\) for all sufficiently large \(m\).  Then the first term
in (R14) is bounded below by a positive constant, much more than
\((\log\log m)/m\).  The escalation-irrelevant flat region \(p\ge\beta\)
has the same property.  Therefore (R18)--(R19) are a genuinely uniform lower
bound over the full policy domain, not merely over an optimizing sequence.

Combining with (R17) gives

\[
 \boxed{1-D^*(m)\sim\frac{\log\log m}{m}.}       \tag{R20}
\]

### 4.4 Flat comparison and value

For the flat optimizer \(x_F=mp_F\),

\[
 e^{x_F}=1+m-x_F,
\]

and direct substitution gives the exact identity

\[
 1-F^*(m)=\frac{x_F+1-e^{-x_F}}m.                \tag{R21}
\]

Since \(x_F\sim\log m\),

\[
 1-F^*(m)\sim\frac{log m}{m}.                   \tag{R22}
\]

Equations (R20)--(R22) imply

\[
 \boxed{V(m)\sim\frac{log m}{m}.}              \tag{R23}
\]

The leading constant is one.

### 4.5 Uniformity qualification and counterexample

The proof is uniform over **all policies/cutoffs** for each fixed
\((\alpha,\beta)\in(0,1]\times(0,1)\).  It is not uniform over primitive
sequences approaching the boundary.  This distinction must be explicit.

For example, let \(\alpha_m=m^{-2}\), with fixed \(\beta>0\).  Then
\(k_m=\alpha_m m=m^{-1}\to0\), not infinity.  The construction behind
(R16) no longer has \(T\to1\).  In fact, for every scalar policy,

\[
 T=\frac{k_my^2}{\beta(1+k_my)}\le k_m\beta\le\frac1m.
\]

Thus (R14), \(p\ge a=x/m\), and \(1-e^{-x}\ge0\) give

\[
 m(1-J)\ge x(1-e^{-x})+(m-1)e^{-x}
 =x+(m-1-x)e^{-x}.                              \tag{R24}
\]

The minimum of the right side is asymptotic to \(\log m\), by the same
calculus as (R19).  The flat policy supplies the matching
\(O(\log m/m)\) upper bound.  Hence along this primitive sequence
\(1-D^*=\Theta(\log m/m)\), not \(\log\log m/m\).  Thus no estimate of the form

\[
 \sup_{0<\alpha\le1}
 \left|\frac{m(1-D_{\alpha,0}^*(m))}{\log\log m}-1\right|
 \longrightarrow0
\]

can hold.  Similar nonuniformity occurs as \(\beta\downarrow0\) with \(m\).

**Verdict:** the matching rates and their constants are correct for fixed
positive \(\alpha,\beta\).  The lower bound is policy-uniform.  Any claim of
uniformity over primitives, or any interchange of the large-\(m\) limit with
\(\alpha\downarrow0\), would be false.

## 5. Continuity, policy attainment, and optimal thickness

### 5.1 Value continuity and attainment

The fixed cutoff coordinate \(a\in[0,\beta]\) is valid for every \(m>0\).
The inverse envelope map, discriminant, lower root, and objective are jointly
continuous in \((m,a)\).  Therefore

\[
 \max_{a\in[0,\beta]}J_m(a)
\]

is continuous in \(m\) and attained.  The restricted flat term is likewise a
continuous attained maximum.  Their maximum is exactly \(D^*(m)\), so
\(D^*\), \(F^*\), and \(V=D^*-F^*\) are continuous on \((0,\infty)\), and
the original policy supremum is attained by mapping a scalar maximizer back to
\((P_m(a),Q_m(a))\), or by taking the maximizing flat policy.

This proof is sound and does not require continuity of the pessimistic menu
value at every off-optimum policy.

### 5.2 Optimizer-correspondence wording

Berge directly gives nonempty compactness and upper hemicontinuity of:

* the scalar cutoff argmax \(\arg\max_{a\in[0,\beta]}J_m(a)\); and
* the restricted and unrestricted flat argmax correspondences.

It also gives a continuous selected map from any cutoff maximizer to one
optimal original menu.  It does **not by itself** establish upper
hemicontinuity of the complete original-menu argmax correspondence, because
the scalar map deliberately selects only one representative of some
outcome-equivalent menu sets.  For example, the reject-all fixed-price plateau
contains original menus not represented separately by the single coordinate
\(a=0\).

This is not a counterexample to upper hemicontinuity; it is a gap between the
stated conclusion and the cited proof.  The safe manuscript wording is to
claim upper hemicontinuity for the scalar/flat argmax correspondences.  To
claim it for every original-menu optimizer, add a direct proof of joint
continuity (or the needed closed-graph property) of the original pessimistic
menu objective across the flat, reject-all, and rider-kink boundaries.

### 5.3 Attained best thickness

The audited thin results give \(V(m)\to0\) as \(m\downarrow0\); (R23) gives
\(V(m)\to0\) and strict positivity for all sufficiently large finite \(m\).
Together with continuity, this localizes the global maximum to a compact
subinterval of \((0,\infty)\).  Hence a positive, finite maximizing thickness
exists and is attained.

**Verdict:** value continuity, policy attainment, and existence of an attained
best thickness can enter.  Qualify or separately prove the claim about the
full original-menu optimizer correspondence.

## 6. Recommended claim ledger

| claim | red-team status | action before manuscript |
|---|---|---|
| \(V\sim(1-2a_0)m^2/16\), \(\beta>1/2\) | **PROVED** | Add uniform limiting-discriminant sentence. |
| \(V\sim\alpha m^4/2048\), \(\beta=1/2\) | **CORRECT, PROOF NEEDS REPAIR** | Replace the formal bounded-\(d\) step with (R9)--(R12). |
| \(V=0\) for all sufficiently small \(m\), \(\beta<1/2\) | **PROVED** | No substantive change. |
| \(1-D^*\sim\log\log m/m\) | **PROVED for fixed primitives** | State policy-uniform but not primitive-uniform. |
| \(V\sim\log m/m\) | **PROVED for fixed primitives** | Same qualification. |
| Continuity of \(D^*,F^*,V\) | **PROVED** | No substantive change. |
| Attainment of original policy value | **PROVED** | No substantive change. |
| UHC of scalar optimizer sets | **PROVED** | No substantive change. |
| UHC of complete original-menu optimizer set | **NOT PROVED HERE** | Narrow wording or add direct original-objective argument. |
| Finite attained maximizer of \(V(m)\) | **PROVED** | No substantive change. |

## 7. Bottom line

The topology note's principal mathematical discoveries survive adversarial
audit.  The patient and impatient thin-market regimes, both thick-market
matching rates, continuity, policy attainment, and existence of a finite best
thickness are ready for use with the qualifications above.  The critical
\(\beta=1/2\) coefficient is not false; its current derivation is simply one
uniform-argmax lemma short.  Equations (R9)--(R12) close that gap without any
uniqueness assumption about the global thickness maximizer.

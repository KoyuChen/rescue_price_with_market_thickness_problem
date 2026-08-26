# Incumbent-discount audit for the global no-entry problem

This note studies the uniform no-entry model after multiplying an incumbent
driver's entire period-2 net surplus by an independent discount factor. To
avoid confusing it with cutoff displacements, write \(d\) for the
question's \(\delta\):

\[
 d\in(0,1].
\]

Thus a surviving incumbent who is assigned at terminal payment \(z\) receives
\(d(z-c)\), while immediate net surplus remains \(p-c\). Because \(d>0\),
discounting does **not** change which terminal types accept; it changes only
the value of waiting. This distinction is essential. The conclusions below
would not apply to a specification such as \(dz-c\), which changes terminal
eligibility.

Throughout,

\[
 m>0,\qquad 0<\alpha\le1,\qquad 0<\beta<1,
 \qquad \gamma=0,
\]

and \((p,q)\), \(p\le q\), denotes the announced menu. The rider side,
continuation supply, and tie-breaking convention are otherwise unchanged.

## Executive verdict

The discount does **not** destroy the global geometry. Flat menus still have
the unique cutoff \(a=p\); every strict active menu still has a unique cutoff
below \(p\); every such menu still strictly beats the flat menu with the same
first payment; the fixed-\(p\) problem is still solved by the same rescue
envelope; the outer problem is still one-dimensional and attained; optimized
dominance for \(\beta\ge1/2\) and the single patience threshold both survive.

What fails is the old positive-cutoff completion identity. It becomes

\[
 M_d(p,q;a)
 =(1-p)m\phi(ma)
 \left[a+\frac{p-a}{d}\right],                 \tag{1}
\]

not \((1-p)mp\phi(ma)\). This changes the thin-market asymptotics
singularly. For every fixed \(d<1\):

- when \(\beta>1/2\), the gain is generically order \(m\), not order
  \(m^2\);
- when \(\beta=1/2\), the gain is order \(m^3\), not order \(m^4\);
- when \(\beta<1/2\), the exact initial zero interval survives;
- as \(m\to\infty\), the original \(\log\log m/m\) and \(\log m/m\)
  rates survive with the same leading constants.

The limits \(m\downarrow0\) and \(d\uparrow1\) therefore do not commute at
the first nonzero order.

## 1. Discounted cutoff equation

Put

\[
 k=\alpha m,\qquad C(x)=1-e^{-kx},\qquad
 h(a)=\begin{cases}(e^{ma}-1)/a,&a>0,\\m,&a=0.\end{cases}
\]

For \(0\le a\le p<q<\beta\), define

\[
 A_z(a)=(\beta-z)C(z-a),\quad z\in\{p,q\},
 \qquad B_p=\beta(1-p).
\]

The rider's repeat-rescue calculation is unaffected by driver discounting.
Continuation coverage conditional on posting is still

\[
 K_{p,q}(a)=\frac{\max\{A_p(a),A_q(a)\}}{B_p}.  \tag{2}
\]

Multiplying the discounted cutoff driver's accept-minus-wait payoff by
\(me^{ma}>0\) gives the scalar

\[
 \boxed{\mathcal D^d_{p,q}(a)
 =(p-a)h(a)-dK_{p,q}(a).}                       \tag{3}
\]

The boundary/root rules retain their directions:

\[
 a=0:\ \mathcal D^d(0)\le0,\qquad
 0<a<p:\ \mathcal D^d(a)=0,\qquad
 a=p:\ \mathcal D^d(p)\ge0.                   \tag{4}
\]

### 1.1 Flat menus still have cutoff \(a=p\)

The undiscounted strict flat inequality is

\[
 (p-a)h(a)>\frac{A_p(a)}{B_p},\qquad 0\le a<p.
\]

Since \(d\le1\),

\[
 (p-a)h(a)-d\frac{A_p(a)}{B_p}
 =\left[(p-a)h(a)-\frac{A_p(a)}{B_p}\right]
 +(1-d)\frac{A_p(a)}{B_p}>0.                   \tag{5}
\]

Hence neither a flat menu nor a repeat-only menu can sustain a cutoff below
\(p\). At \(a=p\), waiting coverage is zero. Therefore every flat menu
\((p,p)\), \(p>0\), still has the unique numeric cutoff

\[
 \boxed{a=p.}                                    \tag{6}
\]

Its completion and the optimized flat benchmark are unchanged:

\[
 F_m(p)=(1-p)(1-e^{-mp}),\qquad
 F_0^*(m)=\max_{p\in[0,1]}F_m(p).                \tag{7}
\]

### 1.2 Strict-menu uniqueness also survives

Equation (5) excludes the repeat branch and the rider kink from the zero set.
At an active-rescue zero, write

\[
 u=p-a,\qquad z=q-a,\qquad b=\beta-q,
 \qquad B=\beta(1-p).
\]

The root equation is

\[
 uh(a)=d\frac bB C(z).                           \tag{8}
\]

Because \(b<B\), \(d\le1\), and \(h(a)\ge m\),

\[
 u<\frac{C(z)}m.                                 \tag{9}
\]

For \(R(a)=uh(a)/C(z)\), exactly the old logarithmic-derivative argument
therefore applies:

\[
 \frac{R'(a)}{R(a)}
 =-\frac1u+\frac{h'(a)}{h(a)}
   +\frac{k}{e^{kz}-1}<0.                       \tag{10}
\]

Every zero crosses downward. Moreover

\[
 \mathcal D^d_{p,q}(p)
 =-d\frac{(\beta-q)C(q-p)}{B_p}<0.
\]

Consequently, for every \(0\le p<q<\beta\):

- if \(\mathcal D^d_{p,q}(0)\le0\), the unique cutoff is \(a=0\);
- if \(\mathcal D^d_{p,q}(0)>0\), there is a unique cutoff
  \(a\in(0,p)\).

Equality at zero cannot coexist with a positive root. Thus pessimistic
selection remains immaterial in this discounted no-entry model.

## 2. Completion identity and same-\(p\) dominance

At a positive cutoff, (3) gives

\[
 d e^{-ma}K_{p,q}(a)=m\phi(ma)(p-a).
\]

Substitution into physical completion—not discounted utility—gives (1):

\[
 \boxed{
 M_d(p,q;a)
 =(1-p)m\phi(ma)
 \left[a+\frac{p-a}{d}\right],\qquad a>0.}      \tag{11}
\]

This is an exact failure of the old cancellation. For \(d<1\) and
\(a<p\),

\[
 M_d(p,q;a)-(1-p)mp\phi(ma)
 =(1-p)m\phi(ma)\frac{1-d}{d}(p-a)>0.            \tag{12}
\]

At a reject-all equilibrium, active rescue is necessary and

\[
 M_d(p,q;0)=\frac{A_q(0)}\beta
 \ge\frac{(1-p)mp}{d},                           \tag{13}
\]

with equality precisely at lower-boundary indifference.

For fixed \(p\), define

\[
 G_{d,p}(a)=\phi(ma)\left[a+\frac{p-a}{d}\right].
\]

The bracket is nonincreasing in \(a\), strictly decreasing if \(d<1\), and
\(\phi(ma)\) is strictly decreasing for \(a>0\). Hence
\(G_{d,p}\) is strictly decreasing on \((0,p]\). The zero-cutoff value in
(13) is at least its continuous extension at zero. Completion is therefore
still ordered inversely by the cutoff.

In particular, every strict menu \(0<p<q<\beta\) has \(a<p\) and satisfies

\[
 \boxed{M_d(p,q)>F_m(p).}                        \tag{14}
\]

Thus the global same-first-payment comparison not only survives; discounting
adds the positive wedge in (12).

For reference, the local branch at \((p,p+\varepsilon)\), \(p<\beta\), has

\[
 \kappa_d=
 \frac{d e^{-mp}\alpha\rho(p)}
 {\phi(mp)-d e^{-mp}\alpha\rho(p)},             \tag{15}
\]

and

\[
 \left.\frac{dM_d}{d\varepsilon}\right|_{0+}
 =\frac{m(1-p)e^{-mp}\alpha\rho(p)
 [\phi(mp)-d e^{-mp}]}
 {\phi(mp)-d e^{-mp}\alpha\rho(p)}>0.           \tag{16}
\]

The old derivative is the boundary case \(d=1\).

## 3. Fixed first payment

For a target cutoff \(a<\beta\), the rescue envelope is unchanged:

\[
 A(a,q)=(\beta-q)[1-e^{-k(q-a)}],\qquad q\in[a,\beta].
\]

It is strictly concave, and its unique maximizer \(Q(a)\) satisfies

\[
 e^{k(Q(a)-a)}-1=k(\beta-Q(a)).                  \tag{17}
\]

Let

\[
 S(a)=A(a,Q(a)),\qquad Q_0=Q(0),\qquad S_0=S(0).
\]

Discounting changes implementability, but not the envelope price:

\[
 \boxed{dA(a,q)=\beta(1-p)(p-a)h(a)}             \tag{18}
\]

for a positive target cutoff, and

\[
 dA(0,q)\ge\beta(1-p)mp                         \tag{19}
\]

for reject-all.

For a positive target \(a<p\), strict concavity of \(A(a,\cdot)\) gives the
complete implementability trichotomy:

- if \(dS(a)<\beta(1-p)(p-a)h(a)\), no rescue price implements \(a\);
- at equality, the sole implementer is the tangent price \(Q(a)>p\);
- if \(dS(a)>\beta(1-p)(p-a)h(a)\), exactly two prices, one on each side of
  \(Q(a)\), implement \(a\).

The discounted strict-flat inequality makes every listed implementer strictly
active rather than a repeat/kink pseudo-solution. Consequently the
implementable cutoff set is \([0,p]\) for \(p\le p_z(d)\), and
\([a_d^*(p),p]\) for \(p_z(d)<p<\beta\).

Define

\[
 \boxed{
 p_z(d)=\frac{1-
 \sqrt{1-4dS_0/(\beta m)}}2.}                   \tag{20}
\]

The discriminant is positive and

\[
 0<p_z(d)<Q_0<\frac12,
\]

because \(dS_0\le S_0<\beta mQ_0(1-Q_0)\).

### The discounted fixed-\(p\) theorem

Let \(H_{m,d}(p)=\max_{q\in[p,1]}M_d(p,q)\). Then:

1. **Reject-all plateau.** If \(0\le p\le p_z(d)\), the unique optimal
   rescue is \(q=Q_0\), its cutoff is zero, and
   \[
   H_{m,d}(p)=\frac{S_0}{\beta}.                 \tag{21}
   \]
   The plateau height is independent of \(d\), while its right endpoint
   decreases as discounting becomes more severe.

2. **Positive cutoff.** If \(p_z(d)<p<\beta\), there is a unique
   \(a_d^*(p)\in(0,p)\) satisfying
   \[
   (p-a)h(a)=\frac{dS(a)}{\beta(1-p)}.           \tag{22}
   \]
   The unique optimal rescue remains
   \[
   q^*(p)=Q(a_d^*(p)),                           \tag{23}
   \]
   and its value is (11) evaluated at \(a_d^*(p)\).

3. **No active rescue.** If \(\beta\le p\le1\), every \(q\ge p\) is
   outcome-equivalent and
   \[
   H_{m,d}(p)=F_m(p).                            \tag{24}
   \]

The proof is the old envelope proof with \(S\) multiplied by \(d\). The
one-crossing lemma makes (22) the smallest implementable cutoff, and the
strict decrease of \(G_{d,p}\) makes that cutoff completion-maximizing. For
\(p\le p_z(d)\), every positive-cutoff value is strictly below
\((1-p)mp/d\le S_0/\beta\), while the zero-cutoff value is maximized uniquely
by \(Q_0\).

## 4. Discounted \(P/Q/J\) reduction

Put

\[
 R(a)=\frac{S(a)}{\beta h(a)}.
\]

The tangent equation is now

\[
 (1-p)(p-a)=dR(a).                              \tag{25}
\]

Its unique feasible root remains the lower quadratic branch:

\[
 \boxed{
 P_d(a)=\frac{1+a-
 \sqrt{(1-a)^2-4dR(a)}}2.}                      \tag{26}
\]

Indeed, the undiscounted strict flat inequality gives
\(g_a(Q(a))>R(a)\ge dR(a)\), while \(g_a(a)=0\), and
\(Q(a)<(1+a)/2\). Hence the feasible root lies in \((a,Q(a))\), below the
quadratic vertex. The same fixed-\(p\) one-crossing argument proves that
\(P_d\) is continuous and strictly increasing from
\([0,\beta]\) onto \([p_z(d),\beta]\).

It is useful to put

\[
 T(a)=\frac{S(a)}\beta.
\]

The scalar objective has two equivalent forms for \(a>0\):

\[
 \boxed{
 J_d(a)
 =(1-P_d(a))m\phi(ma)
 \left[a+\frac{P_d(a)-a}{d}\right]
 =(1-P_d(a))(1-e^{-ma})+T(a)e^{-ma}.}            \tag{27}
\]

The second form extends continuously to

\[
 J_d(0)=S_0/\beta,
 \qquad J_d(\beta)=(1-\beta)(1-e^{-m\beta}).
\]

The exact outer problem is therefore

\[
 \boxed{
 D_{\alpha,0,d}^*(m)=
 \max\left\{
 \max_{a\in[0,\beta]}J_d(a),
 \max_{p\in[\beta,1]}F_m(p)
 \right\}.}                                     \tag{28}
\]

All objects are continuous on fixed compact sets, so the original policy
supremum remains attained. The rescue map \(Q\) is unchanged; \(P\),
\(p_z\), and \(J\) must be replaced by (20), (26), and (27). Merely replacing
\(\alpha\) by \(d\alpha\) in the old objective is incorrect because physical
completion is not discounted.

### 4.1 A new exact discount comparative static

For \(0<a<\beta\), implicit differentiation of (25) gives

\[
 \frac{\partial P_d(a)}{\partial d}
 =\frac{R(a)}{1+a-2P_d(a)}>0.
\]

Since \(T(a)\) is independent of \(d\), (27) yields

\[
 \boxed{
 \frac{\partial J_d(a)}{\partial d}
 =-(1-e^{-ma})\frac{\partial P_d(a)}{\partial d}<0.}         \tag{29}
\]

Thus the optimized platform completion value is weakly decreasing in the
driver's discount factor. It is strictly decreasing whenever the optimum is
an interior strict menu. Lower period-2 utility lets the platform implement a
given cutoff with a lower first payment, increasing the posting mass while
holding terminal coverage fixed. This is a platform-completion comparative
static, not a welfare statement.

## 5. Optimized dominance and patience

The flat optimizer \(p_F(m)\) is unchanged and satisfies

\[
 0<p_F(m)<\frac12.
\]

If \(\beta\ge1/2\), then \(p_F<\beta\). By (14), any strict rescue at first
payment \(p_F\) beats the globally optimized flat value. Hence, for every
\(d\in(0,1]\),

\[
 \boxed{
 D_{\alpha,0,d}^*(m)>F_0^*(m)
 \quad\text{when }\beta\ge\frac12.}             \tag{30}
\]

Moreover, \(J_d(0)=S_0/\beta<F_0^*(m)\), and the restricted flat portion in
(28) never exceeds \(F_0^*\). Therefore every optimizer under
\(\beta\ge1/2\) is an interior strict menu

\[
 (p^*,q^*)=(P_d(a^*),Q(a^*)),
 \qquad a^*\in\arg\max_{a\in[0,\beta]}J_d(a)\subset(0,\beta).
\]

No uniqueness of the outer argmax is needed or asserted.

### 5.1 The patience threshold survives

For a fixed strict menu \(p<q\):

- its value equals \(F_m(p)\) when \(\beta\le q\);
- its value is continuous and strictly increasing in \(\beta\) on
  \((q,1)\).

To see the strict part, increasing \(\beta\) increases the active-rescue
coefficient in (3). Global downward crossing shifts the unique positive
cutoff strictly left, and (11) is strictly decreasing in the cutoff. Once the
cutoff is zero, completion is

\[
 (1-q/\beta)C(q),
\]

which is strictly increasing in \(\beta\).

Define

\[
 \beta_c(m,\alpha,d)
 =\inf\{\beta\in(0,1):D_{\alpha,0,d}^*(m;\beta)>F_0^*(m)\}.
\]

The same compact scalar continuity and reuse-of-a-strict-menu argument give

\[
 \boxed{
 D_{\alpha,0,d}^*(m;\beta)>F_0^*(m)
 \iff \beta>\beta_c(m,\alpha,d).}               \tag{31}
\]

Moreover, \(D_{\alpha,0,d}^*(m;\beta)=F_0^*(m)\) through the threshold and
is strictly increasing in \(\beta\) above it.

The old sharp general bounds are unchanged:

\[
 \boxed{
 0< -\frac1m\log(1-F_0^*(m))
 \le\beta_c(m,\alpha,d)
 \le p_F(m)<\frac12.}                           \tag{32}
\]

The lower bound uses only that an active no-entry menu has \(q<\beta\) and
completion below \(1-e^{-m\beta}\); the upper bound uses (14) at \(p_F\).
The exact scalar test is

\[
 \beta>\beta_c(m,\alpha,d)
 \iff \max_{a\in[0,\beta]}J_{d,\beta}(a)>F_0^*(m).           \tag{33}
\]

Equation (29) also gives the nested-threshold comparative static

\[
 0<d_1<d_2\le1
 \quad\Longrightarrow\quad
 \beta_c(m,\alpha,d_1)\le\beta_c(m,\alpha,d_2).              \tag{34}
\]

Thus the undiscounted model \(d=1\) has the largest patience threshold within
this family. Strict inequality in (34) is not claimed globally.

## 6. Market-thickness asymptotics

Fix \((\alpha,\beta,d)\in(0,1]\times(0,1)\times(0,1]\) and write

\[
 V_d(m)=D_{\alpha,0,d}^*(m)-F_0^*(m).
\]

The scalar representation proves continuity of \(D^*\) and \(V_d\) on
\((0,\infty)\). The thin asymptotics split both at \(\beta=1/2\) and at the
discount boundary \(d=1\).

### 6.1 Uniform thin limit

As \(m\downarrow0\), uniformly in \(a\in[0,\beta]\),

\[
 Q_m(a)\longrightarrow\frac{a+\beta}{2},
 \qquad \frac{T_m(a)}m
 \longrightarrow\frac{\alpha(\beta-a)^2}{4\beta}.
\]

Define

\[
 P_{d,0}(a)
 =\frac{1+a-
 \sqrt{(1-a)^2-d\alpha(\beta-a)^2/\beta}}2,                 \tag{35}
\]

and

\[
 \Lambda_d(a)
 =(1-P_{d,0}(a))a+\frac{\alpha(\beta-a)^2}{4\beta}.         \tag{36}
\]

Then

\[
 \frac{J_{d,m}(a)}m\longrightarrow\Lambda_d(a)             \tag{37}
\]

uniformly. The limiting tangent equation is

\[
 (1-P_{d,0})(P_{d,0}-a)
 =\frac{d\alpha(\beta-a)^2}{4\beta},                       \tag{38}
\]

so (36) is equivalently

\[
 \Lambda_d(a)
 =(1-P_{d,0})
 \left[a+\frac{P_{d,0}-a}{d}\right]
 =P_{d,0}(1-P_{d,0})
 +\frac{(1-d)\alpha(\beta-a)^2}{4\beta}.                   \tag{39}
\]

The last positive term is the source of the singular change at \(d=1\).

### 6.2 Patient thin markets: \(\beta>1/2\)

If \(d=1\), the original result is unchanged. Let \(a_0\in(0,1/2)\) solve

\[
 \alpha(\beta-a_0)^2=\beta(1-2a_0).
\]

Then

\[
 V_1(m)\sim\frac{1-2a_0}{16}m^2.              \tag{40}
\]

If \(0<d<1\), put

\[
 \Lambda_d^*=\max_{a\in[0,\beta]}\Lambda_d(a).
\]

There is a unique \(a^\dagger\in(0,1/2)\) satisfying

\[
 d\alpha(\beta-a^\dagger)^2
 =\beta(1-2a^\dagger),                          \tag{41}
\]

which is exactly the point with \(P_{d,0}(a^\dagger)=1/2\). At that point,

\[
 \Lambda_d(a^\dagger)-\frac14
 =\frac{(1-d)\alpha(\beta-a^\dagger)^2}{4\beta}>0.
\]

Hence \(\Lambda_d^*>1/4\), every limiting maximizer is interior and lies to
the left of \(a^\dagger\), and

\[
 \boxed{
 D_{\alpha,0,d}^*(m)=m\Lambda_d^*+O(m^2),\qquad
 V_d(m)\sim\left(\Lambda_d^*-\frac14\right)m.}              \tag{42}
\]

No uniqueness of the maximizer of \(\Lambda_d\) is needed for (42).
For the location claim, \(P_{d,0}\) is strictly increasing, and differentiating
the last expression in (39) shows that \(\Lambda_d'(a)<0\) whenever
\(P_{d,0}(a)\ge1/2\). The endpoint values are below the value at
\(a^\dagger\).

An exact counterexample to the old \(m^2\) rate is

\[
 \alpha=1,\qquad d=\frac12,\qquad \beta=\frac34.
\]

Here

\[
 a^\dagger=\frac{-3+2\sqrt6}{4},
\]

and therefore

\[
 \liminf_{m\downarrow0}\frac{V_d(m)}m
 \ge\frac{(3-\sqrt6)^2}{24}>0.                \tag{43}
\]

The undiscounted claim would instead imply \(V_d(m)/m\to0\).

### 6.3 Critical patience: \(\beta=1/2\)

For \(0<d<1\), define

\[
 L_d=1-\frac{\alpha(1-d)}2>0.                   \tag{44}
\]

A quadratic localization puts every optimizer at
\(a=1/2-cm\) with bounded \(c\). Uniformly on compact \(c\)-sets,

\[
 \begin{aligned}
 J_{d,m}(1/2-cm)
 =&\ \frac m4-\frac{m^2}{16}\\
 &+m^3\left\{\frac1{96}+\frac c8-L_dc^2\right\}
 +O(m^4).                                       \tag{45}
 \end{aligned}
\]

The quadratic is uniquely maximized at

\[
 c_d^*=\frac1{16L_d},
\]

while

\[
 F_0^*(m)
 =\frac m4-\frac{m^2}{16}+\frac{11}{768}m^3+O(m^4).
\]

Since \(11/768=1/96+1/256\),

\[
 \boxed{
 V_d(m)\sim
 \frac{\alpha(1-d)}{512L_d}m^3,
 \qquad 0<d<1,\quad \beta=\frac12.}             \tag{46}
\]

At the boundary \(d=1\), the coefficient in (46) vanishes and the next order
is the original one:

\[
 \boxed{V_1(m)\sim\frac{\alpha}{2048}m^4.}       \tag{47}
\]

For example, \((\alpha,d,\beta)=(1,1/2,1/2)\) gives

\[
 V_d(m)\sim\frac1{768}m^3,
\]

an exact contradiction to mechanically retaining the \(m^4/2048\) formula.

### 6.4 Impatient thin markets: \(\beta<1/2\)

For \(a<\beta\), \(P_{d,0}(a)>a\), and

\[
 \Lambda_d(a)
 <a(1-a)+\frac{(\beta-a)^2}{4\beta}.
\]

The right side is strictly increasing on \([0,\beta]\) when
\(\beta<1/2\), with endpoint \(\beta(1-\beta)<1/4\). Thus the entire strict
scalar branch is uniformly below the flat leading coefficient \(1/4\).
Since \(p_F(m)\to1/2>\beta\), uniform convergence in (37) implies that for
some \(m_0(\alpha,\beta,d)>0\),

\[
 \boxed{
 D_{\alpha,0,d}^*(m)=F_0^*(m),\qquad
 V_d(m)=0,\qquad 0<m<m_0.}                    \tag{48}
\]

The exact initial no-gain interval therefore survives every fixed
\(d\in(0,1]\).

### 6.5 Thick markets

Let \(y=\beta-Q_m(a)\) and

\[
 T_m(a)=\frac{\alpha m y^2}{\beta(1+\alpha m y)}.
\]

The discounted tangent equation is

\[
 (1-P_d)(P_d-a)
 =d\frac{aT_m(a)}{e^{ma}-1}.                    \tag{49}
\]

Nevertheless, (27) gives the same exact nonnegative loss decomposition as in
the undiscounted model:

\[
 \boxed{
 1-J_d(a)
 =P_d(a)(1-e^{-ma})+[1-T_m(a)]e^{-ma}.}          \tag{50}
\]

Since \(P_d(a)\ge a\), the old policy-uniform lower bound is unchanged. If
\(Q_m(a)\le\beta/2\), putting \(x=ma\) gives

\[
 m[1-J_d(a)]\ge
 x(1-e^{-x})+
 \frac{\log(1+\alpha m\beta/2)}{\alpha\beta}e^{-x}.          \tag{51}
\]

Its minimum is asymptotic to \(\log\log m\). If
\(Q_m(a)>\beta/2\), then
\(Q_m(a)-a=O(\log m/m)\), so eventually \(a>\beta/4\) and the first loss
term in (50) is bounded away from zero.

For the matching upper bound, choose \(a=(\log\log m)/m\). Then
\(Q_m(a)=O(\log m/m)\), \(1-T_m(a)=O(\log m/m)\), and (49) gives
\(P_d-a=o(a)\), uniformly for \(d\in(0,1]\). Substitution in (50) yields the
matching leading constant. Therefore, for every fixed positive
\((\alpha,\beta,d)\),

\[
 \boxed{
 1-D_{\alpha,0,d}^*(m)\sim\frac{\log\log m}{m},\qquad
 1-F_0^*(m)\sim\frac{\log m}{m},\qquad
 V_d(m)\sim\frac{\log m}{m}.}                  \tag{52}
\]

The dynamic loss estimate is in fact uniform over discount sequences
\(d_m\in(0,1]\) when \(\alpha\) and \(\beta\) are fixed. As before, it is
not uniform when \(\alpha\downarrow0\) or \(\beta\downarrow0\).

## 7. Attainment in market thickness and threshold endpoints

Equations (28), (35)--(37), and (49)--(50) make \(D^*\), \(F^*\), and
\(V_d\) continuous in \(m>0\). All thin regimes give \(V_d(m)\to0\) as
\(m\downarrow0\), while (52) gives \(V_d(m)\to0\) and eventual strict
positivity as \(m\to\infty\). Hence there is at least one finite positive
maximizer

\[
 m^*\in\arg\max_{m>0}V_d(m),\qquad V_d(m^*)>0.               \tag{53}
\]

For \(\beta<1/2\), (48) still disproves strict single-peakedness. For
\(\beta\ge1/2\), neither the discounted reduction nor the endpoint expansions
prove a global shape theorem; uniqueness of \(m^*\) remains open.

The unchanged bounds in (32) also imply, for every fixed \(d\in(0,1]\),

\[
 \beta_c(m,\alpha,d)\to\frac12\quad(m\downarrow0),
 \qquad
 \beta_c(m,\alpha,d)\sim\frac{\log m}{m}\quad(m\to\infty). \tag{54}
\]

The first limit uses (48) below \(1/2\) and
\(\beta_c\le p_F\to1/2\); the second follows by squeezing between the two
bounds in (32).

## 8. Exact pass/fail map

| Undiscounted global claim | Status for \(d\in(0,1]\) | Exact change |
|---|---:|---|
| Flat menu has unique \(a=p\) | **PASS** | Discount strengthens the strict flat inequality. |
| Every strict active menu has one cutoff | **PASS** | Root equation gains a factor \(d\); the same downward crossing applies. |
| Positive-cutoff identity \(M=(1-p)mp\phi(ma)\) | **FAIL if \(d<1\)** | Replace by (11); the difference is exactly (12). |
| Every strict menu beats same-\(p\) flat | **PASS** | Follows from cutoff ordering under (11), globally rather than locally. |
| Fixed-\(p\) tangent rescue \(Q(a)\) | **PASS** | \(Q,S\) unchanged; implementability is scaled by \(d\). |
| Old \(p_z,P,J\) formulas | **FAIL literally** | Replace by (20), (26), and (27). |
| One-dimensional outer maximum and policy attainment | **PASS** | Exact representation is (28). |
| Optimized strict dominance for \(\beta\ge1/2\) | **PASS** | Same-\(p_F\) argument; every optimizer remains interior and strict. |
| Single upper patience region and bounds | **PASS** | Threshold becomes \(\beta_c(m,\alpha,d)\); bounds are unchanged. |
| \(\beta>1/2\) thin rate \(V\asymp m^2\) | **FAIL if \(d<1\)** | New exact leading rate is (42), of order \(m\). |
| \(\beta=1/2\) thin rate \(\alpha m^4/2048\) | **FAIL if \(d<1\)** | Replace by the order-\(m^3\) formula (46). |
| \(\beta<1/2\) exact small-\(m\) equality \(V=0\) | **PASS** | Equation (48). |
| Thick-market matching rates | **PASS** | Same leading constants; see (52). |
| Continuity and finite best thickness | **PASS** | Equation (53); no uniqueness or shape claim. |

The sharp conceptual boundary is \(d=1\) for the **thin expansion**, not for
the global policy geometry. For every fixed positive discount factor, all
global existence, uniqueness, scalar-reduction, dominance, and patience
results survive; only the completion identity and the endpoint orders must be
changed.

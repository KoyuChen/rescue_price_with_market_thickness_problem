# No-entry policy topology and market thickness

## 0. Scope and dependency

Fix

\[
 0<\alpha\leq 1,\qquad 0<\beta<1,\qquad \gamma=0.
\]

This note takes as its sole global-policy input the exact scalar reduction in
`global_noentry_geometry.md`: a strict active menu has a unique cutoff, the
fixed-first-price optimum is the tangent rescue menu, and the lower quadratic
branch implements it.  Everything below is a downstream topology,
optimization, or asymptotic argument.  In particular, none of the results
below repairs the proof if that scalar reduction is later withdrawn.

The main conclusions are:

1. the scalar policy problem lives on the **fixed compact interval**
   \([0,\beta]\), and the original policy supremum is attained;
2. \(D_{\alpha,0}^*(m)\) and
   \(V_{\alpha,0}(m)=D_{\alpha,0}^*(m)-F_0^*(m)\) are continuous in
   \(m>0\);
3. the optimized thin-market gain has three distinct regimes:

   \[
   \begin{array}{c|c}
   \text{patience} & V_{\alpha,0}(m),\quad m\downarrow0\\ \hline
   \beta>1/2 & \displaystyle
     \frac{1-2a_0}{16}m^2+o(m^2)\\[5pt]
   \beta=1/2 & \displaystyle
     \frac{\alpha}{2048}m^4+o(m^4)\\[5pt]
   \beta<1/2 & 0\quad\text{for every sufficiently small }m;
   \end{array}
   \]

4. at the thick-market endpoint,

   \[
   1-F_0^*(m)\sim\frac{\log m}{m},\qquad
   1-D_{\alpha,0}^*(m)\sim\frac{\log\log m}{m},
   \]

   and consequently

   \[
   V_{\alpha,0}(m)\sim\frac{\log m}{m};
   \]

5. continuity, strict positivity somewhere, and endpoint vanishing imply that
   \(V\) has an attained global maximum at a finite positive thickness;
6. strict single-peakedness is false for \(\beta<1/2\), and remains open for
   \(\beta\geq1/2\).  A broad numerical attack found no robust counterexample
   in the latter region, but this is not a proof.

## 1. A fixed compact cutoff coordinate

Put \(k=\alpha m\).  For \(a\in[0,\beta]\), let \(z_m(a)\) be the unique
nonnegative solution of

\[
 z+\log(1+z)=k(\beta-a).                                      \tag{1}
\]

Define

\[
 y_m(a)=\frac{z_m(a)}k,
 \qquad
 Q_m(a)=\beta-y_m(a)
       =a+\frac{\log(1+z_m(a))}{k}.                            \tag{2}
\]

Then \(Q_m(a)\) is exactly the rescue-price envelope, because

\[
 e^{k(Q_m(a)-a)}=1+k\{\beta-Q_m(a)\}.                         \tag{3}
\]

For later use, write

\[
 T_m(a)
 :=\frac{k y_m(a)^2}{\beta[1+k y_m(a)]},                      \tag{4}
\]

and, with the continuous convention \(a/(e^{ma}-1)=1/m\) at
\(a=0\),

\[
 B_m(a):=\frac{a}{e^{ma}-1}T_m(a).                            \tag{5}
\]

The implementing first payment is

\[
 P_m(a)
 =\frac{1+a-\sqrt{(1-a)^2-4B_m(a)}}2.                        \tag{6}
\]

Finally define

\[
 J_m(a)=mP_m(a)[1-P_m(a)]\phi(ma),
 \qquad
 \phi(x)=\frac{1-e^{-x}}x,\qquad \phi(0)=1.                  \tag{7}
\]

At \(a=\beta\), these formulas give

\[
 Q_m(\beta)=P_m(\beta)=\beta,\qquad
 J_m(\beta)=(1-\beta)(1-e^{-m\beta}),                        \tag{8}
\]

so the flat endpoint is included without taking an open-set supremum.

### Lemma 1 (the discriminant and ordering never fail)

For every \(m>0\) and every \(0\leq a<\beta\),

\[
 a<P_m(a)<Q_m(a)<\beta,                                      \tag{9}
\]

and the discriminant in (6) is strictly positive.

#### Proof

Let \(q=Q_m(a)\), \(y=\beta-q\), and \(s=q-a\).  Equation (3) gives

\[
 T_m(a)=\frac y\beta(1-e^{-ks}).                             \tag{10}
\]

Since \(a/(e^{ma}-1)\leq1/m\), \(1-e^{-ks}<ks\),
\(k/m=\alpha\leq1\), and \(q>0\),

\[
 \begin{aligned}
 B_m(a)
 &<\alpha\frac y\beta s\\
 &\leq\frac{\beta-q}{\beta}(q-a)\\
 &<(1-q)(q-a).                                                \tag{11}
 \end{aligned}
\]

The strictly concave quadratic

\[
 g_a(p)=(1-p)(p-a)
\]

vanishes at \(a\) and \(1\), while (11) says
\(g_a(q)>B_m(a)>0\).  Thus the equation \(g_a(p)=B_m(a)\) has
two distinct roots surrounding \(q\).  Its lower root is (6), so
\(a<P_m(a)<q\), and its discriminant is positive.  Equation (2) gives
\(a<q<\beta\).  \(\square\)

This elementary bound is useful because it removes a possible moving-domain
problem: the parameter set is always exactly the same compact interval
\([0,\beta]\).

## 2. Continuity and policy-value attainment

The map \(z\mapsto z+\log(1+z)\) is strictly increasing from
\([0,\infty)\) onto itself.  Its inverse is continuous and smooth away from
the origin.  Equations (1)--(6), Lemma 1, and the endpoint conventions imply
that

\[
 (m,a)\longmapsto(Q_m(a),B_m(a),P_m(a),J_m(a))                \tag{12}
\]

is jointly continuous on \((0,\infty)\times[0,\beta]\).

The exact global reduction can be written as

\[
 D_{\alpha,0}^*(m)
 =\max\left\{
      \max_{a\in[0,\beta]}J_m(a),
      \max_{p\in[\beta,1]}(1-p)(1-e^{-mp})
    \right\}.                                                 \tag{13}
\]

The point \(a=0\) in the first maximum contains the low-first-price
plateau from the fixed-price problem.  The second maximum contains every
region in which escalation is irrelevant.  Thus (13) omits no original
policy regime.

### Proposition 1 (attainment and continuity)

For every fixed \((\alpha,\beta)\in(0,1]\times(0,1)\):

1. the supremum defining \(D_{\alpha,0}^*(m)\) is a maximum in the
   original menu space;
2. \(D_{\alpha,0}^*(m)\), \(F_0^*(m)\), and
   \(V_{\alpha,0}(m)\) are continuous on \((0,\infty)\);
3. the scalar cutoff argmax and flat-price argmax correspondences are
   nonempty, compact valued, and upper hemicontinuous.

#### Proof

Both maximizations in (13) have continuous objectives and fixed compact
choice sets.  Berge's maximum theorem gives continuity of their values and
upper hemicontinuity and compactness of their argmax sets.  A cutoff maximizer
\(a^*\) maps to the feasible original menu
\((P_m(a^*),Q_m(a^*))\); a maximizer in the second term maps to a flat
menu.  Hence the original supremum is attained.  The optimized flat value is
the maximum of the continuous function

\[
 F_m(p)=(1-p)(1-e^{-mp})
\]

on the fixed compact interval \([0,1]\), so the same theorem applies.
Taking the difference proves continuity of \(V\).  \(\square\)

For \(\beta\geq1/2\), the global strict-improvement theorem sharpens (13) to

\[
 D_{\alpha,0}^*(m)=\max_{a\in(0,\beta)}J_m(a)>F_0^*(m),        \tag{14}
\]

and every cutoff maximizer lies in the open interval \((0,\beta)\).  This
interiority is not needed for continuity or attainment.

## 3. Thin-market optimization

The definitions have a useful joint extension to \(m=0\).  Let

\[
 r(x)=\frac{x}{e^x-1},\qquad r(0)=1.
\]

Since

\[
 B_m(a)
 =r(ma)\frac{\alpha y_m(a)^2}
                 {\beta[1+\alpha m y_m(a)]},                  \tag{15}
\]

and (1) implies \(y_m(a)\to(\beta-a)/2\) uniformly on
\([0,\beta]\),

\[
 Q_m(a)\longrightarrow Q_0(a)=\frac{\beta+a}{2},
 \qquad
 B_m(a)\longrightarrow B_0(a)
 =\frac{\alpha(\beta-a)^2}{4\beta}.                           \tag{16}
\]

Let \(P_0(a)\) be the lower root of

\[
 (1-p)(p-a)=\frac{\alpha(\beta-a)^2}{4\beta}.                 \tag{17}
\]

All convergence in (16), and the resulting convergence
\(P_m\to P_0\), is uniform.  The limiting discriminant is uniformly positive.
Indeed, the limiting version of Lemma 1 gives

\[
 B_0(a)<\{1-Q_0(a)\}\{Q_0(a)-a\},\qquad 0\le a<\beta,
\]

while at \(a=\beta\) it equals \((1-\beta)^2>0\).  Continuity and
compactness therefore give a strictly positive uniform minimum.  To see why
Taylor expansions below are also uniform, write

\[
 z+\log(1+z)=2z-\frac{z^2}{2}+O(z^3).
\]

Its local inverse is analytic and \(\sup_a z_m(a)=O(m)\).  Hence
\(Q_m,B_m,P_m\), and \(J_m/m\) admit joint Taylor expansions in \(m\) with
remainders uniform in \(a\in[0,\beta]\).

Moreover, \(P_0\) is strictly increasing.
Indeed, implicit differentiation of (17) gives

\[
 P_0'(a)
 =\frac{1-P_0(a)-\alpha(\beta-a)/(2\beta)}
        {1+a-2P_0(a)}>0,                                      \tag{18}
\]

where positivity follows from

\[
 \frac{\alpha(\beta-a)}{2\beta}
 \leq\frac{1-a}{2}\leq1-P_0(a),
\]

with strictness at any possible equality endpoint.

### 3.1 Patient riders: \(\beta>1/2\)

There is a unique \(a_0\in(0,1/2)\) such that \(P_0(a_0)=1/2\).
Equivalently,

\[
 \boxed{\alpha(\beta-a_0)^2=\beta(1-2a_0).}                  \tag{19}
\]

An explicit form is

\[
 a_0=
 \frac{\sqrt{\beta\{\alpha+\beta(1-2\alpha)\}}
       -\beta(1-\alpha)}{\alpha}.                             \tag{20}
\]

Existence and uniqueness also follow directly from strict increase of
\(P_0\): \(P_0(0)<1/2<P_0(\beta)=\beta\).

Put \(H_m(a)=J_m(a)/m\).  Uniform Taylor expansion gives

\[
 H_m(a)=P_0(a)[1-P_0(a)]+m h_1(a)+o(m),                       \tag{21}
\]

uniformly in \(a\).  The leading term has the unique maximizer \(a_0\).
At that point the derivative contribution from the perturbation of \(P_m\)
vanishes because \(1-2P_0(a_0)=0\), leaving

\[
 h_1(a_0)=-\frac{a_0}{2}P_0(a_0)[1-P_0(a_0)]
          =-\frac{a_0}{8}.                                   \tag{22}
\]

For completeness, the argmax step uses the following elementary perturbation
fact.  If \(f_m=f_0+mf_1+o(m)\) uniformly on a compact set and \(f_0\) has a
unique maximizer \(x_0\), then every maximizer of \(f_m\) converges to
\(x_0\), and

\[
 \max f_m=f_0(x_0)+mf_1(x_0)+o(m).
\]

Apply this fact to (21).  It yields

\[
 D_{\alpha,0}^*(m)
 =\frac m4-\frac{a_0}{8}m^2+o(m^2).                          \tag{23}
\]

For the optimized flat policy, the same argument around its unique limiting
optimizer \(p=1/2\) gives

\[
 F_0^*(m)=\frac m4-\frac1{16}m^2+o(m^2).                     \tag{24}
\]

Consequently,

\[
 \boxed{
 V_{\alpha,0}(m)
 \sim \frac{1-2a_0}{16}m^2
 =\frac{\alpha(\beta-a_0)^2}{16\beta}m^2.}                  \tag{25}
\]

The constant is strictly positive.  For example, when
\((\alpha,\beta)=(1,0.9)\), \(a_0=0.3\) and the constant is
\(1/40\).

### 3.2 Critical patience: \(\beta=1/2\)

At \(\beta=1/2\), equation (19) puts the limiting optimizer at the boundary
\(a_0=1/2\), and the coefficient in (25) is zero.  It is incorrect to write
\(V\sim0\cdot m^2\).

Write

\[
 a=\frac12-\delta,\qquad
 \delta=cm+dm^2.
\]

Uniform expansion of (15)--(17) in this boundary layer gives

\[
 P_m(a)
 =\frac12-cm+(\alpha c^2-d)m^2+O(m^3).                       \tag{26}
\]

Substitution in (7) yields

\[
 \begin{aligned}
 \frac{J_m(a)}m
 ={}&\frac14-\frac m{16}
 +\left(\frac1{96}+\frac c8-c^2\right)m^2\\
 &+\left[
   -\frac1{768}-\frac c{24}+\frac{c^2}{4}
   +2\alpha c^3+d\left(\frac18-2c\right)
  \right]m^3
 +O(m^4).                                                     \tag{27}
 \end{aligned}
\]

The optimization of this local expansion requires a uniform argmax step.
Write \(H_m=J_m/m\).  Uniform smooth expansion on the fixed cutoff interval
gives

\[
 H_m(a)=H_0(a)+m h_1(a)+O(m^2).                              \tag{27a}
\]

Near \(a=1/2\), there are constants \(c_1,c_2>0\) such that

\[
 H_0(1/2)-H_0(1/2-\delta)\ge c_1\delta^2,
 \qquad
 |h_1(1/2-\delta)-h_1(1/2)|\le c_2\delta.
\]

Comparing any maximizer with the feasible endpoint \(a=1/2\), and using a
fixed leading gap away from that endpoint, yields \(\delta_m=O(m)\).  Put
\(c=\delta/m\); every optimizer is now in a fixed compact interval of this
rescaled coordinate.  Analyticity of the exact formulas gives, uniformly for
bounded \(c\),

\[
 \begin{aligned}
 H_m(1/2-cm)
 ={}&\frac14-\frac m{16}+m^2 f_2(c)+m^3f_3(c)+O(m^4),        \tag{27b}\\
 f_2(c)={}&\frac{11}{768}-\left(c-\frac1{16}\right)^2,\\
 f_3(c)={}&-\frac1{768}-\frac c{24}+\frac{c^2}{4}
             +2\alpha c^3.
 \end{aligned}
\]

The exact quadratic \(f_2\) has the unique maximizer

\[
 c=\frac1{16}.                                                \tag{28}
\]

Since \(f_3\) is Lipschitz on the compact localization set,

\[
 \max_c\{f_2(c)+m f_3(c)+O(m^2)\}
 =f_2(1/16)+m f_3(1/16)+O(m^2).                              \tag{28a}
\]

For the upper bound, combine the quadratic loss
\(-(c-1/16)^2\) with the Lipschitz gain \(mL|c-1/16|\); their optimized
displacement contribution is \(O(m^2)\).  Evaluation at \(c=1/16\) gives
the matching lower bound.  This validates the optimized remainder without
assuming a second-order expansion of the optimizer.  Consistently, the
coefficient on \(d\) in the more detailed display (27) vanishes at
\(c=1/16\).
Thus

\[
 \frac{D_{\alpha,0}^*(m)}m
 =\frac14-\frac m{16}+\frac{11}{768}m^2
  +\left(-\frac3{1024}+\frac{\alpha}{2048}\right)m^3
  +o(m^3).                                                    \tag{29}
\]

Direct expansion of the flat first-order condition gives

\[
 p_F(m)=\frac12-\frac{m}{16}+\frac{m^2}{192}+O(m^3),
\]

and therefore

\[
 \frac{F_0^*(m)}m
 =\frac14-\frac m{16}+\frac{11}{768}m^2
  -\frac3{1024}m^3+o(m^3).                                   \tag{30}
\]

Therefore the first nonzero optimized gain is fourth order:

\[
 \boxed{V_{\alpha,0}(m)\sim\frac{\alpha}{2048}m^4,
 \qquad \beta=\frac12.}                                     \tag{31}
\]

### 3.3 Impatient riders: \(\beta<1/2\)

Here \(P_0(a)\leq P_0(\beta)=\beta<1/2\).  Hence
\(P_0(a)[1-P_0(a)]\) is maximized at \(a=\beta\), with value
\(\beta(1-\beta)<1/4\).  Uniform convergence gives a fixed leading-order
gap between every active-escalation scalar value and the optimized flat
value.  Also \(p_F(m)\to1/2>\beta\), so the maximizer of the restricted flat
term in (13) is the unrestricted flat optimizer for all sufficiently small
\(m\).  It follows that there is \(m_0(\alpha,\beta)>0\) such that

\[
 \boxed{D_{\alpha,0}^*(m)=F_0^*(m),\qquad
 V_{\alpha,0}(m)=0,\qquad 0<m<m_0.}                          \tag{32}
\]

This is an exact equality on an interval, not merely an asymptotic order.

## 4. Thick-market optimization

Let \(x=ma\), and abbreviate \(p=P_m(a)\), \(q=Q_m(a)\), and
\(T=T_m(a)\).  The implementing-root equation is

\[
 (1-p)(p-a)=\frac{aT}{e^x-1}.                                \tag{33}
\]

Using (33) in (7) gives the exact loss decomposition

\[
 \boxed{
 1-J_m(a)
 =p(1-e^{-x})+(1-T)e^{-x}.}                                  \tag{34}
\]

Both terms are nonnegative.  The first is the first-payment/posting loss;
the second is the residual continuation loss.

### 4.1 Matching bounds for the optimized dynamic loss

We first give a feasible upper bound on \(1-D^*\).  Choose

\[
 x_m=\log\log m,\qquad a_m=\frac{x_m}{m}.                    \tag{35}
\]

For all sufficiently large \(m\), this lies in \((0,\beta)\).  From (2),

\[
 q-a=\frac{\log(1+ky)}k
 \leq\frac{\log(1+k\beta)}k=o(1),                            \tag{36}
\]

so \(q=o(1)\), \(p<q=o(1)\), and (33) implies

\[
 p-a=O(ae^{-x_m}).                                            \tag{37}
\]

Moreover,

\[
 1-T
 \leq\frac q\beta+\frac1{1+ky}
 =O\left(\frac{\log m}{m}\right).                           \tag{38}
\]

Substituting (35)--(38) into (34) gives

\[
 1-D_{\alpha,0}^*(m)
 \leq1-J_m(a_m)
 \leq(1+o(1))\frac{\log\log m}{m}.                          \tag{39}
\]

The reverse bound must be uniform over the optimizing cutoff.  If
\(q\leq\beta/2\), then \(y\geq\beta/2\), and (2), (4) imply

\[
 1-T\geq\frac q\beta
 \geq\frac{\log(1+k\beta/2)}{k\beta}.                        \tag{40}
\]

Thus (34) and \(p\geq a=x/m\) give

\[
 m[1-J_m(a)]
 \geq x(1-e^{-x})+C_m e^{-x},
 \qquad
 C_m:=\frac{\log(1+\alpha m\beta/2)}{\alpha\beta}.          \tag{41}
\]

The right side is

\[
 g_{C_m}(x)=x+(C_m-x)e^{-x}.
\]

Its unique minimum is attained at \(r_m\) satisfying

\[
 e^{r_m}=1+C_m-r_m,                                          \tag{42}
\]

and the minimum equals

\[
 r_m+1-e^{-r_m}\sim\log C_m\sim\log\log m.                  \tag{43}
\]

If instead \(q>\beta/2\), (36) implies \(a>\beta/4\) for all sufficiently
large \(m\).  The first term in (34) is then bounded away from zero, which is
much larger than \((\log\log m)/m\).  Hence (41)--(43) give a uniform lower
bound over every \(a\in[0,\beta]\).  The irrelevant flat region
\(p\geq\beta\) has loss at least \(\beta+o(1)\), so it cannot weaken the
bound.  Combining with (39), for each fixed
\((\alpha,\beta)\in(0,1]\times(0,1)\),

\[
 \boxed{
 1-D_{\alpha,0}^*(m)
 \sim\frac{\log\log m}{m}.}                                  \tag{44}
\]

This is a matching optimized bound; it does not optimize a fixed menu and
then interchange that optimization with a limit.

### 4.2 Exact flat loss and the optimized gain

Let \(x_F=mp_F(m)\).  The flat first-order condition is

\[
 e^{x_F}=1+m-x_F.                                             \tag{45}
\]

It implies \(x_F\sim\log m\) and the exact identity

\[
 1-F_0^*(m)=\frac{x_F+1-e^{-x_F}}m.                           \tag{46}
\]

Therefore

\[
 \boxed{1-F_0^*(m)\sim\frac{\log m}{m}.}                     \tag{47}
\]

Since \(V=(1-F^*)-(1-D^*)\), equations (44) and (47) give

\[
 mV_{\alpha,0}(m)
 =\log m-(1+o(1))\log\log m,
\]

and, in particular,

\[
 \boxed{V_{\alpha,0}(m)\sim\frac{\log m}{m}.}               \tag{48}
\]

The leading constant is exactly one for every fixed
\((\alpha,\beta)\in(0,1]\times(0,1)\).  These parameters enter lower-order
terms and the optimal menu.  Convergence is uniform over policies for fixed
primitives, but not over primitive sequences approaching a boundary.  For
example, along \(\alpha_m=m^{-2}\), one obtains
\(1-D^*(m)=\Theta(\log m/m)\), not
\((\log\log m)/m\).

## 5. An attained best thickness

Equations (23), (29), and (32) show \(V(m)\to0\) as \(m\downarrow0\).
Equation (48) shows \(V(m)\to0\) as \(m\to\infty\), while also showing that
\(V(m)>0\) for all sufficiently large finite \(m\).  Together with
Proposition 1, this proves the following.

### Proposition 2 (existence, not uniqueness, of an optimal thickness)

For every \(0<\alpha\leq1\) and \(0<\beta<1\), there exists at least one
\(m^*\in(0,\infty)\) such that

\[
 V_{\alpha,0}(m^*)=\max_{m>0}V_{\alpha,0}(m)>0.               \tag{49}
\]

#### Proof

Choose one finite \(m_1\) with \(V(m_1)>0\).  Endpoint vanishing gives
\(0<\underline m<m_1<\overline m<\infty\) such that
\(V(m)<V(m_1)/2\) outside
\([\underline m,\overline m]\).  Continuity gives a maximizer on this compact
interval, and it is a global maximizer on \((0,\infty)\).  \(\square\)

## 6. Strict single-peakedness: one disproof and one open problem

Use the strong definition: there is an \(m^*>0\) such that \(V\) is strictly
increasing on \((0,m^*)\) and strictly decreasing on
\((m^*,\infty)\).

For \(\beta<1/2\), equation (32) gives a nondegenerate initial interval on
which \(V=0\).  Therefore:

\[
 \boxed{\text{Strict single-peakedness is false whenever }\beta<1/2.} \tag{50}
\]

For \(\beta\geq1/2\), the current evidence does not prove or disprove the
claim.  The exact obstruction can be stated cleanly.  Let

\[
 \mathcal A(m)=\arg\max_{a\in[0,\beta]}J_m(a).                \tag{51}
\]

At a thickness with a unique smooth interior optimizer \(a_m\), the envelope
formula is

\[
 V'(m)=\partial_mJ_m(a_m)-\frac{dF_0^*(m)}{dm}.               \tag{52}
\]

Even if \(J_{aa}(m,a_m)<0\),

\[
 V''(m)
 =J_{mm}-\frac{J_{ma}^2}{J_{aa}}-F^{*\prime\prime}(m),        \tag{53}
\]

whose sign is not fixed by the envelope construction or by monotonicity of
\(P_m(a)\) in \(a\).  At an optimizer switch, Danskin's theorem gives

\[
 D_+'(m)=\max_{a\in\mathcal A(m)}J_m^{(1,0)}(a),
 \qquad
 D_-'(m)=\min_{a\in\mathcal A(m)}J_m^{(1,0)}(a),              \tag{54}
\]

so the derivative can jump.  A proof of strict single-peakedness must either
rule out optimizer switches and prove that (52) crosses zero once, or control
all slopes in (54).  Continuity and the endpoint rates do neither.

### Numerical adversarial search

The reproducible falsifier is
`announced_escalation_overhaul/thickness_search.py`; the independent
high-precision local checker is
`announced_escalation_overhaul/thickness_decimal_check.py`.  The first uses a hybrid grid in
both \(a\) and \(x=ma\), brackets every visible local maximum, refines all
brackets, and subtracts the exact optimized-flat value.  It never assumes a
single local cutoff maximum.

A lattice attack used

\[
 \alpha\in\{.001,.003,.01,.03,.1,.3,1\},
 \quad
 \beta\in\{.5001,.51,.55,.7,.9,.99\},                        \tag{55}
\]

111 logarithmically spaced thicknesses from \(10^{-4}\) to \(10^7\), and a
500-point linear plus 500-point log-cutoff grid at every parameter point.
No robust down-up pattern was found.  Denser targeted scans extended the
thickness range to \([10^{-5},10^8]\).  The exact critical case
\(\beta=1/2\) was also scanned for
\(\alpha\in\{.001,.01,.1,1\}\), again without a robust down-up pattern.
An independent 60-decimal-digit
calculation at \((\alpha,\beta)=(1,.9)\) located the apparent peak at

\[
 \begin{aligned}
 m&\approx9.25480176444024,\\
 V(m)&\approx0.065685569530389,\\
 (a,p_1,p_2)&\approx
 (0.131770419185156,0.167064262100035,0.330189731012850).
 \end{aligned}                                                \tag{56}
\]

These calculations are useful falsification evidence only.  They cannot
exclude a narrow down-up interval between grid points, certify uniqueness of
the cutoff argmax for every \(m\), or establish the derivative one-crossing
needed in (52)--(54).  Accordingly:

\[
 \boxed{\text{Strict single-peakedness for }\beta\geq1/2
 \text{ remains OPEN.}}                                      \tag{57}
\]

## 7. Claim ledger for this note

| Claim | Status | Dependency / qualification |
|---|---|---|
| Fixed compact cutoff domain, continuity of \(P,Q,J\) | PROVED | Lemma 1 and inverse-map argument |
| Original policy-value attainment | PROVED conditional on exact scalar reduction | Equation (13) |
| Continuity of \(D^*\) and \(V\) in \(m>0\) | PROVED conditional on exact scalar reduction | Berge maximum theorem |
| Thin rate for \(\beta>1/2\) | PROVED conditional on exact scalar reduction | Uniform argmax expansion |
| Critical thin rate \(\alpha m^4/2048\) | PROVED conditional on exact scalar reduction | Boundary-layer expansion |
| Initial zero-gain interval for \(\beta<1/2\) | PROVED conditional on exact scalar reduction | Uniform limiting gap |
| \(1-D^*\sim(\log\log m)/m\) | PROVED conditional on exact scalar reduction | Uniform lower bound plus feasible construction |
| \(V\sim(\log m)/m\) | PROVED conditional on exact scalar reduction | Difference of matching losses |
| Attained finite positive maximizing thickness | PROVED conditional on exact scalar reduction | Continuity, positivity, endpoint limits |
| Strict single-peakedness, \(\beta<1/2\) | DISPROVED | Initial zero interval |
| Strict single-peakedness, \(\beta\geq1/2\) | OPEN | Numerical support only; derivative/switch obstruction unresolved |

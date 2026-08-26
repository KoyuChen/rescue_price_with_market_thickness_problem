# Red-team audit of the global no-entry geometry

## Scope and bottom line

This audit treats every result in `global_noentry_geometry.md` as a claim to
be proved or refuted.  It checks Lemma 2, Theorems 3--4, Lemma 5, the outer
`J` reduction and attainment argument, and Theorem 7.  It also independently
checks `flat_and_local_noentry_proof.md` and the public-count benchmark,
especially (N3).

**Bottom line:** I found no false substantive theorem in this set.  The global
fixed-`p` solution, lower quadratic branch, outer reduction, and patience-
threshold theorem survive independent derivation.  There are nevertheless
four repairs that should be made before importing the material into a paper:

1. distinguish the lower- and upper-boundary driver actions when `p=0`;
2. state explicitly why the envelope/root equations cannot create a
   repeat-only or rider-kink pseudo-implementer;
3. close the `a=0` endpoint in the injectivity proof for `P`;
4. expand the joint-continuity argument at `x=0,1` before invoking the maximum
   theorem.

These are proof/exposition repairs, not counterexamples to the advertised
results.

## Status ledger

| Item | Status | May enter the paper? | Required action |
|---|---|---|---|
| Lemma 2, downward crossing | **PASS** | Yes | Say the `a=0` right-derivative case presumes `p>0`; for `p=0`, `[0,p)` is empty. |
| Theorem 3, unique strict-menu cutoff | **PASS / REPAIR** | Yes after a boundary sentence | Uniqueness is of the numeric cutoff under the stated cutoff-type convention. Separate `p=0`, where lower and upper boundary labels coincide. |
| Fixed-`p` implementability, (27)--(28) | **PASS / REPAIR** | Yes | Insert the short `A_q>A_p` argument, so every solution of (27) is genuinely on the active-rescue branch. |
| Theorem 4, fixed-first-payment optimum | **PASS** | Yes | Keep the `p=0` boundary convention explicit. No hidden larger root or alternate implementing price was found. |
| Lemma 5, minus quadratic branch | **PASS / REPAIR** | Yes after one sentence | Extend the structural injectivity argument to exclude `P(a)=P(0)=p_z` for `a>0`. |
| Outer `J` reduction and attainment | **PASS** | Yes | Prefer maximizing on `[0,beta]` and then state the argmax is interior; this avoids an unnecessary open-set `max` notation. |
| Continuity in patience / maximum theorem | **PASS / REPAIR** | Yes after endpoint details | Verify the continuous extensions at `x=0` and `x=1` explicitly and then apply the elementary maximum theorem on fixed compact domains. |
| Theorem 7, one upper patience interval | **PASS** | Yes | State dependence on attainment and unique cutoff as hypotheses already proved. |
| Flat/local no-entry result | **PASS / REPAIR** | Yes | Add the uniform positive-denominator step proving `delta_epsilon=O(epsilon)`. |
| Known-`n` identity and (N3) | **PASS** | Yes | No correction to (N3); retain the `n=1` zero-gain qualification. |

No item receives **FAIL**.

## 1. Primitive checksum for the geometry

Let

\[
 k=\alpha m,\qquad C(x)=1-e^{-kx},\qquad
 h(a)=\frac{e^{ma}-1}{a},\quad h(0)=m.
\]

For `0<p<q<beta`, define

\[
 A_z(a)=(\beta-z)C(z-a),\qquad
 B_p=\beta(1-p).
\]

If rescue is active, substitution of the rider's switch type gives

\[
 K_{p,q}(a)=\frac{A_q(a)}{B_p};
\]

if rescue is inactive, continuation coverage is `A_p/B_p`.  Consequently

\[
 K_{p,q}(a)=\frac{\max\{A_p(a),A_q(a)\}}{B_p},
 \qquad
 D_{p,q}(a)=(p-a)h(a)-K_{p,q}(a).
\]

The branch criterion is exact:

\[
 A_q>A_p
 \quad\Longleftrightarrow\quad v^M<1.
\]

For later use, the repeat branch satisfies

\[
 (p-a)h(a)>\frac{A_p(a)}{B_p}\quad(0\le a<p).
 \tag{R1}
\]

At `a>0`, strictness follows from `phi(ma)>e^{-ma}`.  At `a=0`, the first
comparison is an equality, but overall strictness follows from
`rho(p)<1`.  This endpoint split is correctly made in the geometry note and
repairs the false strict chain identified in the earlier root note.

Equation (R1) has two important consequences that should be invoked every
time a rescue equation is used:

- a cutoff equilibrium below `p` cannot lie on the repeat branch or at its
  kink;
- if an equation of the form `A_q=B_p(p-a)h(a)` holds, then automatically
  `A_q>A_p`, so it is not a spurious solution obtained from the wrong rider
  branch.

## 2. Lemma 2: every active-rescue zero crosses downward

**Status: PASS.**

At an active-rescue zero put

\[
 u=p-a,quad z=q-a,quad b=\beta-q,quad B=\beta(1-p).
\]

The root equality is

\[
 uh(a)=\frac bB C(z).
\]

Because `B-b=q-beta p>0`, `b/B<1`.  Since `h(a)>=m`,

\[
 u<\frac{C(z)}m.                                  \tag{R2}
\]

For `R(a)=u h(a)/C(z)`, direct differentiation gives

\[
 \frac{R'}R=-\frac1u+\frac{h'}h+
             \frac{k}{e^{kz}-1}.                 \tag{R3}
\]

Using (R2),

\[
 \begin{aligned}
 \frac1u-\frac{k}{e^{kz}-1}
 &>\frac{m}{1-e^{-kz}}-
    \frac{k e^{-kz}}{1-e^{-kz}}\\
 &=m\frac{1-\alpha e^{-kz}}{1-e^{-kz}}
 \ge m>\frac{h'}h.
 \end{aligned}
\]

Thus `R'<0`.  Since

\[
 D=C(z)\left(R-\frac bB\right),
\]

the derivative of `D` at a zero has the sign of `R'`, hence is strictly
negative.  The sign in the lemma is correct; no missing minus sign was found
in the differentiation of `C(q-a)`.

At `a=0`, the same right-derivative calculation is valid when `p>0`, using
`h'(0)/h(0)=m/2`.  If `p=0`, the purported domain `[0,p)` is empty, so the
lemma is vacuous rather than a separate derivative case.

## 3. Theorem 3: uniqueness of the strict-menu cutoff

**Status: PASS / boundary repair.**

All zeros below `p` are strictly active by (R1), so Lemma 2 applies to every
zero of the actual piecewise function `D`.  Also

\[
 D(p)=-\frac{(\beta-q)C(q-p)}{B_p}<0.
\]

A continuous function cannot have two zeros at which it crosses strictly
from positive to negative: after the first downward crossing, returning to a
positive left neighborhood of a second one would require an upward or
tangential zero.  Therefore:

- `D(0)>0` gives exactly one interior zero by the intermediate value theorem;
- `D(0)<0` gives no interior zero and the lower boundary is the equilibrium;
- `D(0)=0` gives a strict rightward move into negative values and no later
  zero.

This proves the advertised equality case as well; a zero cutoff and a
positive cutoff cannot coexist.

The only repair is terminological at `p=0`.  The scalar `a=0` is both the
lower and upper endpoint.  Under a strict active menu the cost-zero driver
strictly prefers waiting, so the valid strategy is lower-boundary reject-all,
not the upper-boundary convention in which `c=p` accepts.  The theorem's
numeric cutoff conclusion is correct, but the paper should carry the cutoff
driver's action or treat `p=0` separately.

The other regimes also check:

- flat `q=p>0`: unique numeric cutoff `a=p`;
- `p<beta<=q`: rescue is unused by positive mass and (R1) forces `a=p`;
- `p>=beta`: no positive-mass continuation, hence `a=p`;
- `alpha=0`: waiting is worthless, hence `a=p` for `p>0`.

## 4. Fixed-p implementability

**Status: PASS / make branch validity explicit.**

For fixed target `a<p`,

\[
 A(a,q)=(\beta-q)C(q-a)
\]

has

\[
 A_{qq}=-e^{-k(q-a)}[2k+k^2(\beta-q)]<0.
\]

Its unique unconstrained maximizer `Q(a)` satisfies

\[
 e^{k(Q-a)}-1=k(\beta-Q).
 \tag{R4}
\]

The formula using the principal Lambert branch, the inequalities

\[
 a<Q(a)<\frac{a+\beta}{2},
\]

and the envelope identities

\[
 S=A(a,Q),\quad
 S=\frac{k(\beta-Q)^2}{1+k(\beta-Q)},\quad
 S'=-C(Q-a),\quad
 \frac{S'}S=-\frac1{\beta-Q}
\]

are all correct.

A positive target cutoff is implemented by a strict rescue exactly when

\[
 A(a,q)=B_p(p-a)h(a).                            \tag{R5}
\]

There is no branch error hidden in (R5): by (R1), its right side is strictly
larger than `A(a,p)=A_p`, so every solution has `A_q>A_p` and is active.
Strict concavity then gives zero, one tangent, or two implementing prices
according as the constrained envelope is below, equal to, or above the right
side.  Theorem 3 makes the implemented cutoff the unique equilibrium; (R5)
is not merely a necessary root equation.

At `a=0`, reject-all is implemented iff

\[
 A(0,q)\ge B_pmp.
\]

Again, the flat inequality gives `A_p<B_pmp` for `p>0`, so any qualifying
strict price is genuinely active.  At `a=p`, only the flat menu and
repeat-only prices implement the upper-boundary cutoff; a strict price below
`beta` gives the cutoff type a positive waiting option.

## 5. Theorem 4: exact fixed-first-payment optimizer

**Status: PASS.**

Let `Q_0=Q(0)` and `S_0=A(0,Q_0)`.  Applying (R1) at
`p=Q_0,a=0` yields

\[
 S_0<\beta m Q_0(1-Q_0)<\frac{\beta m}{4}.
\]

Hence

\[
 p_z=\frac{1-\sqrt{1-4S_0/(\beta m)}}2
\]

is real and satisfies `0<p_z<Q_0<1/2`.

### Reject-all region

When `p<=Q_0`, the best rescue numerator at zero is `S_0`, so reject-all is
feasible iff

\[
 p(1-p)\le \frac{S_0}{\beta m}.
\]

Only the lower quadratic interval is relevant because `p<=Q_0<1/2`; hence
this is exactly `p<=p_z`.  If `p>Q_0`, the constrained rescue maximum at zero
is the flat endpoint `q=p`, and (R1) rules out reject-all.  Thus zero is
implementable exactly for `p<=p_z`.

For `p<p_z`, every positive cutoff value is strictly below
`(1-p)mp<S_0/beta`, while a zero-cutoff policy has value
`A(0,q)/beta<=S_0/beta`, uniquely maximized by `q=Q_0`.  At `p=p_z`, the
middle inequality becomes equality only for the zero extension; every
positive cutoff remains strictly worse because `phi(ma)<1`.  This proves the
plateau and uniqueness of `Q_0`.

### Positive-cutoff region

For `p_z<p<beta`, the constrained-envelope margin is positive at zero and
negative at `p`.  Its zeros cross downward by the fixed-price version of
Lemma 2, so it has exactly one zero `a^*(p)`.  At that zero `Q(a)>p`, and its
equation is

\[
 (p-a)h(a)=\frac{S(a)}{\beta(1-p)}.
\]

For any other strict price with equilibrium cutoff `a_q`,

\[
 \overline D_p(a_q)\le0.
\]

Since the envelope margin is positive below its unique downward zero, this
implies `a_q>=a^*(p)`.  Flat/repeat-only menus have cutoff `p`.  Completion is
strictly decreasing in every positive cutoff, so the tangent price
`Q(a^*)` is uniquely optimal.  No fixed-`p` implementability gap or hidden
larger equilibrium root remains.

### Boundary regions

At `p=0`, only numeric cutoff zero is feasible and `Q_0` uniquely maximizes
value; explicitly call its driver action reject.  At `p>=beta`, all rescue
prices are outcome-equivalent and give the flat first-period value.  Thus the
fixed-`p` supremum is indeed a maximum for every `p`.

As a nonproof numerical checksum, 500 random parameter/fixed-`p` draws over
wide logarithmic ranges were solved both from the theorem and by direct
one-dimensional rescue-price optimization.  The largest value discrepancy
was below `4e-13`.

## 6. Implementable cutoff sets

**Status: PASS.**

The summaries following Theorem 4 are implied by the sign of the unique
envelope crossing:

- for `0<p<=p_z`, the envelope margin starts nonpositive and can have no
  later downward zero, so every positive target below `p` has the envelope
  strictly above the required level and therefore has two implementers;
- for `p_z<p<beta`, the implementable set is `[a^*(p),p]`, with one tangent
  implementer at its lower endpoint and two strict implementers in its
  interior;
- `p` itself is implemented by flat/repeat-only menus.

At `p=p_z`, zero has the single tangent implementer `Q_0`, while every
positive target has two.  At `p=0`, there are no positive target cutoffs.

## 7. Lemma 5: only the minus quadratic branch

**Status: PASS / one endpoint sentence needed.**

Set

\[
 R(a)=\frac{S(a)}{\beta h(a)},\qquad
 g_a(p)=(1-p)(p-a).
\]

Since `Q(a)<(1+a)/2`, `g_a` is strictly increasing from zero on
`(a,Q(a))`.  Applying (R1) to the flat candidate `p=Q(a)` gives

\[
 g_a(Q(a))>R(a)>g_a(a)=0.
\]

Therefore exactly one solution lies in `(a,Q(a))`, the discriminant is
strictly positive, and that solution is the minus root

\[
 P(a)=\frac{1+a-\sqrt{(1-a)^2-4R(a)}}2.
\]

The plus root lies above the quadratic vertex and cannot be a fixed-`p`
tangent optimum.

The structural monotonicity proof is valid for two positive arguments: if
`P(a_1)=P(a_2)`, the same fixed-`p` envelope has two zeros, contradicting
one-crossing.  The text should add the endpoint case.  If
`P(a)=P(0)=p_z` for some `a>0`, the `p_z` envelope would have its zero at
zero and another at `a`, the same contradiction.  With that sentence,
continuous injectivity and the endpoint limits prove that

\[
 P:[0,\beta)\to[p_z,\beta)
\]

is a strictly increasing bijection.  The claimed inverse
`p mapsto a^*(p)` is therefore correct.

## 8. Outer J reduction and attainment

**Status: PASS.**

At the tangent menu, completion is

\[
 J(a)=(1-P(a))P(a)\frac{1-e^{-ma}}a.
\]

The endpoint extensions are correct:

\[
 J(0)=mp_z(1-p_z)=S_0/\beta,
 \qquad
 J(\beta)=(1-\beta)(1-e^{-m\beta}).
\]

Because `P` is a bijection, `J` parameterizes exactly the fixed-`p` values
for `p in [p_z,beta]`; the lower region is the constant plateau `J(0)`, and
the upper region is the flat function.  Hence the original policy supremum
equals a maximum of continuous functions over compact intervals.  This is a
direct attainment proof and does not rely on lower hemicontinuity of a
set-valued equilibrium correspondence.

For `beta>=1/2`, the flat optimizer satisfies `p_F<1/2<=beta`, and every
strict menu at `p_F` improves on its flat value.  The two endpoint regions
are bounded by the optimized flat value, while the dynamic optimum is
strictly above it.  Therefore every outer maximizer is interior and has the
form

\[
 (p_1^*,p_2^*)=(P(a^*),Q(a^*)).
\]

No uniqueness or single-peakedness of `J` is needed.  For maximal formal
clarity, write

\[
 \max_{a\in[0,\beta]}J(a)
\]

and then state that its argmax lies in `(0,beta)`, rather than introducing a
`max` over the open interval first.

The displayed outer first-order condition also checks.  From

\[
 R'=-R\left(\frac1{\beta-Q}+\frac{h'}h\right)
\]

and `(1-P)(P-a)=R`,

\[
 P'=\frac{1-P+R'}{1+a-2P}.
\]

At an interior maximizer, logarithmic differentiation of `J` gives the
stated condition.  Since
`m/(e^{ma}-1)-1/a<0` and `P'>0`, it correctly implies `P(a^*)<1/2`.

## 9. Patience continuity and Theorem 7

### Lemma 6

**Status: PASS.**

For a fixed strict menu `p<q`, value is flat in patience while `beta<=q`,
because rescue is not used and repeat alone leaves cutoff `p`.  If
`beta_2>beta_1>q`, the coefficient

\[
 \frac{1-q/\beta}{1-p}
\]

strictly increases.  At the `beta_1` equilibrium rescue is active, so the
`beta_2` cutoff margin is strictly lower at the old cutoff.  Uniqueness and
downward crossing imply the new cutoff is strictly lower or becomes zero.
The positive-cutoff completion identity then gives strict improvement; at a
zero cutoff the explicit value

\[
 (1-q/\beta)C(q)
\]

has positive derivative.  The continuity argument as `beta` decreases to
`q` is also sound: any subsequential cutoff limit below `p` would violate
(R1), so the cutoff converges to `p`.

### Maximum-theorem step

**Status: PASS / expand endpoint verification.**

The reduction uses fixed compact choice domains by writing `a=beta x` and
`p=beta+(1-beta)s`.  For
`delta=beta(1-x)`, the equation

\[
 e^{ky}-1=k(\delta-y)
\]

has a unique solution because its left-minus-right side has strictly positive
derivative.  The solution is jointly continuous in `delta`, including
`y(0)=0`.  This gives joint continuity of `Q`, `S`, `R`, `P`, and `J` away
from their removable endpoints.

The paper should spell out those endpoints:

- at `x=0`, `h(0)=m`, `Q_beta(0)`, `S_0`, and
  `P_beta(0)=p_z(beta)` are continuous, with the discriminant strictly
  positive by the flat inequality;
- at `x=1`, `Q_beta(beta)=P_beta(beta)=beta`, `S=R=0`, and
  `J_beta(beta)=(1-beta)(1-e^{-m beta})`.

On every local rectangle
`[beta_-,beta_+] times [0,1]` inside `(0,1) times [0,1]`, these extensions
are uniformly continuous.  The elementary maximum theorem then proves
continuity of `D(beta)`.  Thus there is no hidden varying-domain error, but
the current phrase "the formulas show" is too compressed for a central
attainment/threshold theorem.

### Theorem 7

**Status: PASS.**

Flat policies imply `D(beta)>=F^*`.  If strict gain holds at `beta_1`, policy
attainment supplies an optimizing strict menu with `q<beta_1`; every flat or
repeat-only menu is bounded by `F^*`.  Reusing that menu at any larger
`beta_2` and applying Lemma 6 gives

\[
 D(\beta_2)>D(\beta_1)>F^*.
\]

Therefore the gain set is an upper interval and `D` is strictly increasing
inside it.  Continuity makes the gain set open.  It is nonempty because every
`beta>p_F(m)` permits a strict improvement at the flat optimizer, and its
lower endpoint is positive because any active menu has completion bounded by
`1-e^{-m beta}`.  Hence

\[
 \{\beta:D(\beta)>F^*\}=(\beta_c,1),
\]

with equality `D=F^*` at and below `beta_c` and strict increase above it.
The bounds

\[
 0<\beta_L(m)\le\beta_c(m,\alpha)\le p_F(m)<1/2
\]

also check.  The event bound uses `q<beta` only for active strict menus;
flat/repeat-only menus are separately bounded by `F^*`, as required.

The scalar necessary-and-sufficient test is valid because the second term in
the exact outer maximum is a restricted flat maximum and can never exceed
`F^*`.  Joint continuity of `J_beta(beta x)` makes its maximum continuous.

## 10. Audit of the flat and local no-entry proof

**Status: PASS / minor rigor repair.**

The flat objective

\[
 F_m(p)=(1-p)(1-e^{-mp})
\]

is strictly concave, its Lambert-`W` optimizer formula is correct, and
`p_F(m)<1/2` follows strictly from `e^{m/2}>1+m/2`.

The local equilibrium equation is the correct active-rescue equation.  Its
limit has no solution below `p` by (R1), so `a_epsilon` converges to `p`.
The claim `delta_epsilon=O(epsilon)` is correct but should not rest only on
`1-e^{-x} asymp x`.  Once localization is known, choose a neighborhood in
which

\[
 h_m(a)-r_\varepsilon m\alpha\ge c>0.
\]

Using `1-e^{-x}<=x` in (L1) then gives

\[
 c\,\delta_\varepsilon
 \le r_\varepsilon m\alpha\,\varepsilon,
\]

which proves the uniform order bound.  Every subsequential limit of
`delta_epsilon/epsilon` solves the same linear equation, establishing the
full-sequence limit and (L2).  Formula (L3), its strict sign, and the extension
of optimized-flat dominance to `beta=1/2` all check.

## 11. Audit of the public known-n benchmark, especially (N3)

**Status: PASS.**

With `n` public incumbents,

\[
 s_n(a)=\frac{1-(1-a)^n}{na}
\]

is the focal acceptor's assignment share.  Conditional on universal rival
rejection, a rival is a surviving eligible competitor at payment `p_j` with
probability

\[
 \theta_j=\frac{\alpha(p_j-a)}{1-a},
\]

so `C_{j,n}=n theta_j s_n(theta_j)`.  Substitution into cutoff indifference
correctly yields

\[
 M_n=(1-p_1)n p_1s_n(a).
\]

For `q=p+epsilon` and `a=p-delta`, active-rescue cancellation gives the exact
indifference form

\[
 s_n(a)\delta
 =\frac{(1-a)^n}{n}\,r_\varepsilon C_{q,n}(a).
\]

Since

\[
 C_{q,n}(a)
 =\frac{n\alpha(\varepsilon+\delta)}{1-p}
 +o(\varepsilon+\delta),
\]

division by `epsilon` yields

\[
 s_n(p)\kappa
 =(1-p)^{n-1}\alpha\rho(1+\kappa).
\]

Therefore (N3) is exactly

\[
 \boxed{
 \kappa_n=
 \frac{(1-p)^{n-1}\alpha\rho}
 {s_n(p)-(1-p)^{n-1}\alpha\rho}. }
\]

The denominator is positive because
`s_n(p)>=(1-p)^{n-1}` and `alpha rho<1`.  Differentiating the completion
identity gives (N4).  For `n>=2`, `s_n'<0`, so the local gain is positive;
for `n=1`, `s_1` is constant and the first-order gain is exactly zero.  No
missing factor of `n`, `1-p`, survival, or universal-rejection probability was
found.

## Recommended theorem import decision

The following substantive claims are ready for the manuscript after the
listed local repairs:

- global downward crossing and unique strict-menu cutoff;
- the complete fixed-`p` optimizer and implementable-cutoff correspondence;
- the lower-branch inversion and one-dimensional outer `J` reduction;
- policy-value attainment without any global single-peakedness assumption;
- strict dynamic improvement for `beta>=1/2`;
- the full upper-interval patience theorem and its scalar threshold test;
- the flat/local derivative result, including equality `beta=1/2`;
- the known-`n` local benchmark with (N3)--(N4).

Do **not** import claims of uniqueness or single-peakedness of the outer
argmax: none is proved here, and none is needed.  Also do not call the scalar
cutoff alone a unique pointwise pure strategy at a boundary tie unless the
cutoff driver's action convention is explicitly part of the equilibrium
definition.

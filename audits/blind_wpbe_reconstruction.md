# Blind reconstruction of the anonymous symmetric cutoff WPBE

This note derives the follower game from the primitives, without using the
manuscript's displayed equilibrium formulas.  The main conclusion is that the
core Poisson, payoff, cutoff, completion, and flat-policy formulas in the
current draft are correct.  There are, however, genuine formal gaps at rider
payoff ties and at the policy boundaries `p_1=0` and `p_1=1`; the tie gap can
change the equilibrium set on a positive-measure set of rider types if read
literally.

Throughout, fix `m>0`, `0<=p_1<=p_2<=1`, and a conjectured first-period
incumbent cutoff `a in [0,p_1]`.  Equality types have zero probability, but
their prescribed actions still matter for a pointwise WPBE and at the cutoff
boundaries.  Write

\[
 h(x):=\mathbb E\!\left[\frac1{1+Z_x}\right]
 =\begin{cases}(1-e^{-x})/x,&x>0,\\1,&x=0,\end{cases}
 \qquad Z_x\sim\operatorname{Pois}(x).
\]

The identity follows by integrating the Poisson probability-generating
function.  Two useful facts are `0<h(x)<=1` and

\[
 h(x)\ge e^{-x},
 \]

with equality only at `x=0`.  The latter is equivalent to
`e^x >= 1+x`.

## 1. Bayes beliefs and Poisson posteriors

Suppose all other incumbents accept in period 1 below `a` and reject above
`a`.  Poisson marking gives independent counts

\[
 N_{<a}\sim\operatorname{Pois}(ma),\qquad
 N_{>a}\sim\operatorname{Pois}(m(1-a)).
\]

Thus first-period failure has probability `e^{-ma}` conditional on a posted
request.  Conditional on failure, `N_{<a}=0`, while the law of `N_{>a}` is
unchanged; their costs are iid uniform on `(a,1)`.  This is a Poisson-splitting
posterior, not a posterior obtained by conditioning an ordinary finite sample
on nonemptiness.

For a focal incumbent, Palm conditioning says that the number of *rival*
incumbents is still `Pois(m)`.  Conditional on the focal driver rejecting, a
public failure occurs exactly when no rival has cost below `a`, an event with
probability `e^{-ma}`.  Conditional on that event, rival rejectors retain the
same split just described.  This distinction is useful:

- the rider forecasts a Poisson number of available acceptors;
- a surviving focal incumbent who accepts in period 2 faces that Poisson
  number as *competitors*, in addition to herself.

For `j in {1,2}`, define

\[
 \lambda_j(a)
 :=m\{\alpha(p_j-a)+\gamma p_j\},\qquad
 S_j(a):=1-e^{-\lambda_j(a)}.
\]

After failure, surviving incumbent costs in `(a,p_j]` form a Poisson group of
mean `alpha m(p_j-a)`, and acceptable fresh drivers form an independent
Poisson group of mean `gamma m p_j`.  Hence `S_j` is the rider's success
probability if payment `p_j` is activated.  Conditional on survival and
eligibility, a waiting focal incumbent's expected selection share is
`h(lambda_j)`.

For `p_1<1`, the posting strategy derived below implies

\[
 v\mid\{\text{post}\}\sim U[p_1,1].
\]

Supply and driver actions are independent of `v`, so first-period failure does
not further update this value distribution.  An observed active continuation
payment can reveal the interval containing `v`, but terminal acceptance is
optimal independently of that belief.  At `p_1=1`, posting has probability
zero, so Bayes' rule does not pin a driver belief after observing a request;
this boundary must be handled separately.

## 2. Terminal acceptance and the rider's continuation action

At the terminal driver node, accepting payment `q` gives a nonnegative payoff
exactly when `c<=q`; rejection gives zero.  Thus terminal drivers accept iff
`c<=q`, with acceptance at equality as a harmless tie convention.

After failure, a rider of type `v` obtains

\[
 0,\qquad S_1(a)(\beta v-p_1),\qquad
 S_2(a)(\beta v-p_2)
\]

from abandonment, repetition, and rescue, respectively.  Since
`S_2>=S_1`, rescue can beat repetition only at high values.  If `S_2>S_1`,
let

\[
 x(a):=\frac{S_2(a)p_2-S_1(a)p_1}
              {\beta\{S_2(a)-S_1(a)\}}.
\]

Then

\[
 \beta x(a)-p_2
 =\frac{S_1(a)(p_2-p_1)}{S_2(a)-S_1(a)}\ge0,
\]

so `x>=p_2/beta>=p_1/beta`.  If `S_2=S_1`, repetition weakly dominates
rescue; put `x=+infinity`.  Subject to the intended repeat-versus-abandon tie
rule, the rider therefore

\[
 \begin{cases}
 \text{abandons},&v<p_1/\beta,\\
 \text{repeats},&p_1/\beta\le v<x(a),\\
 \text{uses rescue},&v>x(a).
 \end{cases}
\]

The action at `v=x` requires an additional tie convention and is immaterial
for all aggregate expressions.  Conditional on posting, define

\[
 r(a):=\frac{[\min\{x(a),1\}-p_1/\beta]^+}{1-p_1},
 \qquad
 e(a):=\frac{[1-x(a)]^+}{1-p_1}.
\]

These are the repeat and rescue probabilities seen by a period-1 driver.  They
satisfy

\[
 r(a)+e(a)=\rho(p_1)
 :=\frac{[1-p_1/\beta]^+}{1-p_1}.
\]

The identity remains correct in the important case `S_1=0<S_2`: then
`x=p_2/beta`.  Riders in `[p_1/beta,p_2/beta)` are indifferent between
abandoning and a zero-success repeat, while rescue is strictly worse.  The
formulas above use the intended convention that these riders repeat.

## 3. Initial posting

The payoff from posting is

\[
 \Pi(v;a)=(1-e^{-ma})(v-p_1)
 +e^{-ma}\max\{0,S_1(\beta v-p_1),S_2(\beta v-p_2)\}.
\]

If `v<p_1`, then also `beta v<p_1<=p_2`, so the continuation maximum is zero.
Posting is strictly bad if `a>0` and is a zero-payoff tie if `a=0`; the stated
posting tie rule selects no post.  At `v=p_1`, posting yields zero and the rule
selects post.  If `v>p_1`, posting is strictly profitable when `a>0`; when
`a=0` and continuation is worthless it is again selected by the tie rule.
Consequently,

\[
 \boxed{\text{post iff }v\ge p_1},
\]

and the posting mass is `1-p_1` (zero at the endpoint `p_1=1`).

## 4. A focal incumbent's accept and wait payoffs

If a focal incumbent accepts in period 1, the number of accepting rivals is
`Pois(ma)`.  Her expected payoff is therefore

\[
 A(c;a)=h(ma)(p_1-c).
\]

If she rejects, the request fails against all rivals with probability
`e^{-ma}`.  She must then survive (probability `alpha`), the rider must choose
an active payment she is willing to accept, and she is selected against a
`Pois(lambda_j)` competitor count.  Hence

\[
 W(c;a)=\alpha e^{-ma}\left\{
 r(a)h(\lambda_1(a))[p_1-c]^+
 +e(a)h(\lambda_2(a))[p_2-c]^+
 \right\}.
\]

These are payoffs conditional on seeing the posted request; multiplying by the
posting probability would be incorrect in a driver's sequential decision.
Also, the failure factor is `e^{-ma}` for *rivals*: Palm conditioning is why a
focal driver is not counted inside that exponential.

## 5. Cutoff best response and single crossing

For `c<=p_1`, put `G(c;a):=A(c;a)-W(c;a)`.  Expanding the rescue term around
`p_1-c` gives the affine representation

\[
 G(c;a)=B(a)(p_1-c)-D(a),
\]

where

\[
 \begin{aligned}
 B(a)&:=h(ma)-\alpha e^{-ma}
 \{r(a)h(\lambda_1(a))+e(a)h(\lambda_2(a))\},\\
 D(a)&:=\alpha e^{-ma}e(a)h(\lambda_2(a))(p_2-p_1)\ge0.
 \end{aligned}
\]

Because `h(lambda_j)<=1`, `r+e=rho<=1`, and `alpha<=1`,

\[
 B(a)\ge h(ma)-e^{-ma}\ge0.
\]

In fact `B(a)>0` whenever `p_1>0`: if `a>0`, the last displayed inequality is
strict; if `a=0`, then `rho(p_1)<1` because `beta<1`.  Therefore `G` is
strictly decreasing in cost on `[0,p_1]` for every positive first payment.
For `c>p_1`, immediate acceptance is strictly loss-making while waiting is
nonnegative.  Thus a best response to any rival cutoff is itself a cutoff.

More explicitly, for `p_1>0`, the best-response cutoff to rivals' cutoff `a`
is reject-all if `B(a)p_1-D(a)<=0`, is the unique interior value

\[
 p_1-\frac{D(a)}{B(a)}
\]

if `0<D(a)<B(a)p_1`, and is `p_1` if `D(a)=0`.  Equality types are assigned by
the boundary conventions.

## 6. Exact equilibrium and boundary conditions

Define the cutoff-type margin

\[
 f(a;p_1,p_2):=G(a;a)
 =B(a)(p_1-a)-D(a).
\]

For `0<p_1<1`, the exact conditions are:

\[
 \begin{array}{c|c|l}
 \text{candidate}&\text{condition}&\text{cutoff-type action}\\ \hline
 a=0&f(0)\le0&c=0\text{ rejects}\\
 0<a<p_1&f(a)=0&c=a\text{ may be assigned either action}\\
 a=p_1&f(p_1)\ge0&c=p_1\text{ accepts}.
 \end{array}
\]

The last condition can be sharpened.  Directly,

\[
 f(p_1)=-\alpha e^{-mp_1}e(p_1)h(\lambda_2(p_1))(p_2-p_1)\le0.
\]

Since `h` and the exponential are positive, the accept-all boundary is an
equilibrium iff

\[
 \boxed{\alpha\,e(p_1)(p_2-p_1)=0}.
\]

Thus it occurs for a flat policy, when incumbents cannot survive, or when no
posted rider type chooses rescue (including the relevant degenerate cases).
The reject-all condition may be written explicitly as

\[
 p_1\le \alpha\left\{
 r(0)h(m(\alpha+\gamma)p_1)p_1
 +e(0)h(m(\alpha+\gamma)p_2)p_2
 \right\}.
\]

An interior equilibrium solves

\[
 h(ma)(p_1-a)=\alpha e^{-ma}\left\{
 r(a)h(\lambda_1)(p_1-a)
 +e(a)h(\lambda_2)(p_2-a)
 \right\}.
\]

Important parameter boundaries are as follows.

- `p_1=0`: the only aggregate cutoff is `a=0`; all positive-cost drivers
  reject.  The cost-zero type rejects if waiting is strictly better and may be
  assigned either action at a tie.  Here `f(0)=-D(0)<=0`.  One must not also
  impose the `a=p_1` accept-boundary inequality.
- `p_1=1`: feasibility forces `p_2=1`.  Only the null rider type `v=1` posts,
  so completion is zero.  If the off-path driver subgame is completed in the
  natural way, every `c<1` accepts immediately and the cutoff is `a=1`: even
  the highest rider has `beta v-1<0` after failure, so waiting is worthless.
- `alpha=0` and `p_1>0`: waiting incumbents receive zero, so the unique cutoff
  is `a=p_1` for every announced rescue price.
- `gamma=0`, `a=p_1`, and `p_2>p_1`: repetition has zero coverage but can still
  give a deviating low-cost focal incumbent a continuation payoff.  The
  positive repeat mass dictated by the tie rule must therefore remain in
  `W`; deleting it because `S_1=0` changes the equilibrium.

## 7. Existence and compactness

For fixed `0<p_1<1`, `f` is continuous in `a`.  In the nondegenerate case
`S_2>S_1`, this follows from continuity of `x(a)` and the clipped interval
lengths `r(a),e(a)`.  If `S_2=S_1`, either the policy is flat or continuation
supply is identically zero, and the tie rule fixes the repeat mass directly.

At the upper boundary, `f(p_1)<=0`.  Therefore:

1. if `f(0)<=0`, reject-all is an equilibrium;
2. if `f(0)>0>f(p_1)`, the intermediate value theorem gives an interior root;
3. if `f(0)>0=f(p_1)`, `a=p_1` is an equilibrium.

Together with the direct `p_1=0` and `p_1=1` arguments, an anonymous symmetric
pure-cutoff equilibrium exists for every feasible policy.  For
`0<p_1<1`, its set is the union of the eligible endpoints and the zero set of
`f` in the interior.  Continuity includes all limit roots at an endpoint, so
this set is closed and bounded, hence compact.  This argument does **not**
imply uniqueness: single crossing is in the driver's cost for a fixed rival
cutoff, whereas `f(a)` need not be monotone in the conjectured aggregate
cutoff.

## 8. Completion probability

For an equilibrium cutoff `a` and `p_1<1`, unconditional completion is

\[
 \boxed{
 M(p_1,p_2;a)=(1-p_1)\left[
 1-e^{-ma}+e^{-ma}\{r(a)S_1(a)+e(a)S_2(a)\}
 \right]. }
\]

The three factors are, respectively, posting mass, period-1 completion, and
failure followed by the chosen period-2 completion.  At `p_1=1`, define
`M=0` directly rather than evaluating conditional masses with a zero
denominator.  If several cutoff equilibria exist, a pessimistic symmetric-
cutoff assessment takes the minimum of this expression over the compact
equilibrium set; it is not a minimum over asymmetric or mixed WPBE.

## 9. Flat-payment benchmark

Set `p_1=p_2=p`.  Rescue is only a duplicate label and the tie rule chooses
repeat, so `e(a)=0` and

\[
 f(a;p,p)=(p-a)\left[
 h(ma)-\alpha e^{-ma}\rho(p)
 h\bigl(m\{\alpha(p-a)+\gamma p\}\bigr)
 \right].
\]

For `p>0` the bracket is strictly positive by the single-crossing bound.
Hence no `a<p` can be an equilibrium, while `a=p` satisfies the upper boundary
condition.  The unique numeric cutoff is therefore

\[
 \boxed{a=p}.
\]

At `p=0`, the unique aggregate cutoff is also `a=0`, although the zero-cost
driver's pointwise action is not unique without an extra tie convention.

At `a=p`, a failure establishes that no incumbent has cost below `p`; with
fixed costs, surviving incumbents cannot generate positive-probability
acceptance of the same payment.  Only fresh drivers matter in period 2, so
`S_1=1-e^{-\gamma mp}`.  The flat completion function is

\[
 \boxed{
 Q^F_\gamma(m,p)
 =(1-p)(1-e^{-mp})
 +e^{-mp}[1-p/\beta]^+(1-e^{-\gamma mp}). }
\]

It is independent of `alpha`.  It is continuous on `[0,1]`, including at
`p=beta`, and therefore the optimized flat value is a **maximum**,

\[
 F^*_\gamma(m)=\max_{p\in[0,1]}Q^F_\gamma(m,p).
\]

## 10. Exact discrepancies in the current draft

1. **The stated rider tie rules do not actually make the continuation strategy
   single-valued.**  They say what happens "if all continuation actions yield
   zero," but do not cover an abandon-repeat tie at zero when rescue is
   negative.  This is not merely a null-type issue.  If `S_1=0<S_2`, every
   `v in [p_1/beta,p_2/beta)` has abandonment payoff zero, repeat payoff zero,
   and strictly negative rescue payoff.  The displayed repeat mass counts this
   whole interval as repeating, and the driver wait payoff relies on it.  The
   model must say, for example: "whenever the maximal continuation payoff is
   zero, choose repeat iff `beta v-p_1>=0`, otherwise abandon."

2. **The displayed continuation strategy conflicts with the stated tie rule at
   one exact type.**  When `S_1=0<S_2`, `x=p_2/beta`.  At `v=x` all three
   continuation payoffs are zero, so the stated rule chooses repeat, whereas
   the displayed `v>=x` branch chooses rescue.  This has no aggregate effect
   but prevents the claimed single-valued pure strategy.  More generally, when
   repeat and rescue tie at a positive payoff for `p_2>p_1`, no tie rule is
   stated even though the displayed branch silently selects rescue.

3. **The equilibrium-set display is formally ambiguous at `p_1=0`.**  Then
   `a=0` is simultaneously the lower and upper boundary.  The valid reject-all
   condition is `f(0)<=0`; the upper accept-boundary row says `f(0)>=0`.  These
   must not be imposed together.  The conflict is substantive: with
   `p_1=0`, `alpha>0`, and a rescue used by positive mass,
   `f(0)=-alpha e(0)h(lambda_2)p_2<0`, yet reject-all is a valid equilibrium.
   For example, take `m=1`, `beta=0.8`, `alpha=1`, `gamma=0`, and `p_2=0.4`.
   Then `x=0.5`, `e(0)=0.5`, and
   `f(0)=-0.2h(0.4)<0`.  State `p_1=0` separately or make the cases explicitly
   disjoint.

4. **The feasible endpoint `p_1=1` has no equilibrium correspondence in the
   draft.**  The policy set includes `(1,1)`, the proposition assumes
   `p_1<1`, and the conditional rider masses are `0/0`.  Later defining its
   completion to be zero patches the objective numerically but does not define
   a WPBE or make the displayed minimization over equilibria well-formed at
   that policy.  A clean extension is `E(1,1)={1}` and `M(1,1;1)=0` under the
   boundary driver convention.  Relatedly, the sentence that failure is on
   path for every finite `m` needs the qualifier `p_1<1` (or "conditional on a
   positive-probability post").

5. **The manuscript asserts Bayes consistency but does not state the full
   belief system.**  For `p_1<1`, drivers should have
   `v|post ~ U[p_1,1]`, failure should leave that belief unchanged, and the
   rider/focal-driver Poisson posteriors should be distinguished as above.
   The formulas use the correct beliefs, so this is a WPBE exposition/proof
   gap rather than an algebraic error.

6. **The claim that payoff ties are fully single-valued also omits the
   interior cutoff driver's action and the zero-payment flat boundary.**  These
   are null cost types and do not alter completion, but distinct pure
   strategies remain unless explicitly identified or tied.  The flat
   uniqueness proposition wisely assumes `p>0`; the optimized benchmark also
   includes `p=0`, so the boundary convention should still be recorded.

No discrepancy was found in the draft's core expressions for
`lambda_j`, the rider switch threshold away from ties, the two driver payoffs,
the cutoff margin, existence for `0<p_1<1`, the completion formula, or the
flat completion function.  In particular, the factor `alpha e^{-ma}` and the
selection shares `h(lambda_j)` are required by survival and Palm competition;
they should not be dropped or replaced by rider coverage probabilities.

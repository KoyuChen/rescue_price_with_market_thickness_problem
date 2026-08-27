# Formal setting

## Primitives

- Rider value: `v ~ Uniform[0,1]`.
- Persistent driver order cost: `c ~ Uniform[0,1]`.
- Core first-window incumbent intensity: `m`.
- Time-homogeneous second-window core fresh intensity: `m`.
- Rider delay factor: `beta`.
- Incumbent delay factor: `delta`.
- Incremental pickup-cost slope: `tau`.
- Search-area cap: `s_bar`.
- Incumbent physical-retention probability: `alpha`.
- Conditional platform-recall/eligibility probability: `chi`.

Write

\[
\omega=\alpha\chi\in[0,1].
\]

The archived numerical grid uses `omega=1`; the solver exposes the combined
primitive as `incumbent_retention` so that exit and loss of eligibility affect
both the terminal pool and the focal rejector's waiting payoff consistently.

The platform publicly commits to `mu=(p1,p2,s)` before drivers act. The
baseline and fixed-reach classes impose `s=1`; the flat class additionally
imposes `p2=p1`.

## Spatial search and fresh drivers

Normalize the core catchment to area one and radius `R0`. Search multiplier
`s>=1` expands radius to

\[
R(s)=R_0\sqrt{s}.
\]

Spatial Poisson independent increments imply

\[
N_2^C\sim\operatorname{Pois}(m),\qquad
N_2^O(s)\sim\operatorname{Pois}((s-1)m),\qquad
N_2^C\perp N_2^O(s).
\]

Let area rank be `u=(r/R0)^2`. Core pickup is absorbed into `c`; the extra
outer pickup cost is

\[
d(u)=\tau(\sqrt u-1)_+.
\]

This cost is paid only after assignment. A fresh driver's response payoff is

\[
h(\lambda)[p-c-d(u)],\qquad
h(z)=\frac{1-e^{-z}}{z}.
\]

Since `h(lambda)>0`, response is equivalent to `c+d(u)<=p`. Poisson thinning
therefore gives

\[
e(p,s)=m\int_0^s F(p-d(u))\,du.
\]

For uniform cost, `p in [0,1]`, and `tau>0`, define

\[
R(p,s)=\min\{\sqrt{s},1+p/\tau\}.
\]

Then

\[
e(p,s)=mp+m(p+\tau)(R^2-1)-\frac{2m\tau}{3}(R^3-1),
\]

\[
\frac{\partial e}{\partial s}
=m[p-\tau(\sqrt{s}-1)]_+,
\qquad
s^{\mathrm{sat}}(p)=(1+p/\tau)^2.
\]

There is no notification-time sunk `k` and no fresh-entry fixed point.

## Terminal branches

For proposed incumbent cutoff `a`, terminal action `j` uses

\[
(p_j,s_j)=(p_1,1)\ \text{for repeat},
\qquad
(p_j,s_j)=(p_2,s)\ \text{for rescue}.
\]

The willing-driver intensities and coverage are

\[
I_j^\omega(a)=\omega m[F(p_j)-F(a)]_+,
\]

\[
\lambda_j(a)=I_j^\omega(a)+e(p_j,s_j),
\qquad
C_j(a)=1-e^{-\lambda_j(a)}.
\]

After universal rejection, the rider observes no driver count. She compares

\[
0,\qquad C_1(a)(\beta v-p_1),\qquad C_2(a)(\beta v-p_2).
\]

Let the induced action masses conditional on posting be
`eta_0(a), eta_1(a), eta_2(a)`.

## Cutoff-WPBE

Under a candidate aggregate cutoff, a type-`c` incumbent's
accept-minus-wait payoff is

\[
D(c;a)=h(mF(a))(p_1-c)
-\delta\omega e^{-mF(a)}
\sum_{j=1}^2\eta_j(a)h(\lambda_j(a))(p_j-c)_+.
\]

Together with the rider and fresh-driver strategies above, cutoff `a` is a
WPBE iff beliefs follow Bayes' rule on path and

\[
D(c;a)\ge0\quad\forall c<a,
\qquad
D(c;a)\le0\quad\forall c>a,
\]

with indifference at an interior cutoff. `D(c;a)` is continuous and
piecewise affine in type, with kinks only at `p1` and `p2`. The solver therefore
checks the full type domain exactly through the affine interval endpoints.

The root enumerator includes boundary, sign-changing, and tangential roots and
then certifies the complete root set under grid doubling.

## Outer mechanism design

For `theta=(m,beta,delta)`:

\[
V_k(\theta)=
\max_{\mu\in\mathcal M_k}
\min_{a\in\mathcal E^{\mathrm{WPBE}}(\mu;\theta)}M(\mu,a).
\]

With posting probability `1-p1`, completion at one equilibrium is

\[
M(\mu,a)
=(1-p_1)\left[
1-e^{-mF(a)}
+e^{-mF(a)}\big(\eta_1C_1+\eta_2C_2\big)
\right].
\]

The archived objective is completion, not platform profit or welfare. Pickup
cost is borne by the assigned driver and affects willingness through the
response threshold; it is not subtracted a second time from completion.

## Search-resource extension

Free `s` under a completion objective is a maximal-completion benchmark, not
an economic optimum for notification scope.  Let `q_R(mu,a)` be the ex-ante
probability that expanded rescue is executed.  The expected number of extra
outer contacts is

\[
Q^O(\mu,a)=q_R(\mu,a)m(s-1).
\]

A notification-cost version of the outer objective is

\[
J_\kappa(\mu,a)=B M(\mu,a)-\kappa Q^O(\mu,a),
\]

or one can maximize completion subject to a budget on `Q^O`.  This objective
should be called completion net of notification opportunity cost.  Calling it
platform profit additionally requires separate rider fare and driver-payment
variables.

# Ordered peaks of nested rescue controls

This note separates three statements that should not be conflated:

1. a closed-form theorem on one common Poisson-WPBE branch;
2. a stability corollary that can lift the order to re-optimized value gaps;
3. the current full-model numerics, which motivate but do not prove the global
   ordering.

## 1. Connection to the cutoff-WPBE model

The mechanisms are nested:

\[
\mathcal M_0=\{(p,p,1)\}
\subset
\mathcal M_F=\{(p_1,p_2,1):p_2\ge p_1\}
\subset
\mathcal M_E=\{(p_1,p_2,s):p_2\ge p_1,\ 1\le s\le\bar s\}.
\]

Both terminal mechanisms contain the same time-homogeneous core fresh cohort.
Expanded search adds only the Poisson-thinned outer annulus.  If a first-window
rejector remains available with probability `alpha` and remains eligible with
conditional probability `chi`, let

\[
\omega=\alpha\chi.
\]

Then the terminal incumbent intensity is

\[
I_j^\omega(a)=\omega m[F(p_j)-F(a)]_+,
\]

and the same `omega` multiplies the focal rejector's continuation payoff.  The
archived numerical slice normalizes `omega=1`; the solver now supports any
`omega in [0,1]`.

Fix a symmetric cutoff-WPBE branch on which the rider's terminal action does
not change across the three mechanisms and all effective intensities scale
linearly with thickness.  Let `r` be the common first-window failure hazard and
let

\[
0\le\lambda_0<\lambda_F<\lambda_E
\]

be the terminal effective rates under the three nested mechanism classes.
The rate increments are reduced-form equilibrium objects on this branch; they
already include incumbent retention, core fresh supply, and outer fresh supply.

## 2. The closed-form result

### Theorem 1 (ordered peaks on a common Poisson-WPBE branch)

Suppose

\[
0\le\lambda_0<\lambda_F<\lambda_E,
\qquad r+\lambda_0>0.
\]

Define the adjacent incremental completion gains

\[
\Delta_P^0(m)
=e^{-rm}\left(e^{-\lambda_0m}-e^{-\lambda_Fm}\right),
\]

\[
\Delta_S^0(m)
=e^{-rm}\left(e^{-\lambda_Fm}-e^{-\lambda_Em}\right).
\]

Both gains are strictly single-peaked on `m>0`.  Their unique maximizers are

\[
m_P^*
=\frac{\log[(r+\lambda_F)/(r+\lambda_0)]}
{\lambda_F-\lambda_0},
\]

\[
m_S^*
=\frac{\log[(r+\lambda_E)/(r+\lambda_F)]}
{\lambda_E-\lambda_F},
\]

and they obey the strict order

\[
\boxed{
m_S^*<\frac{1}{r+\lambda_F}<m_P^*}.
\]

Thus the incremental value of expanded search peaks in a strictly thinner
market than the incremental value of fixed-reach rescue pricing.

### Proof

For `0<a<b`, define

\[
g_{a,b}(m)=e^{-am}-e^{-bm}.
\]

Its derivative is

\[
g'_{a,b}(m)
=e^{-am}\left[-a+b e^{-(b-a)m}\right].
\]

The bracketed term is strictly decreasing from `b-a>0` to `-a<0`.
Consequently `g` has exactly one critical point, which is its unique maximum:

\[
m^*(a,b)=\frac{\log(b/a)}{b-a}.
\]

Moreover,

\[
\frac1b<m^*(a,b)<\frac1a.
\]

One way to see these inequalities is to write

\[
\log(b/a)=\int_a^b\frac{dt}{t},
\]

whose integrand lies strictly between `1/b` and `1/a`.  Applying the result to

\[
(a,b)=(r+\lambda_0,r+\lambda_F)
\]

and then to

\[
(a,b)=(r+\lambda_F,r+\lambda_E)
\]

gives

\[
m_P^*>\frac1{r+\lambda_F}>m_S^*.
\qquad\square
\]

### Extension: a common log-concave activation factor

The exponential common trigger is not essential for the ordering.  Let
`A(m)>0` be a common, nonincreasing, log-concave activation factor and suppose
both maxima are interior.  Replace the two gains by

\[
\Delta_P=A(m)e^{-\lambda_0m}
\left(1-e^{-(\lambda_F-\lambda_0)m}\right),
\]

\[
\Delta_S=A(m)e^{-\lambda_Fm}
\left(1-e^{-(\lambda_E-\lambda_F)m}\right).
\]

Each gain is strictly log-concave.  Writing
`d_P=lambda_F-lambda_0` and `d_S=lambda_E-lambda_F`, their log-slope difference
is

\[
(\log\Delta_P)'-(\log\Delta_S)'
=d_P+\frac{d_P}{e^{d_Pm}-1}
-\frac{d_S}{e^{d_Sm}-1}>0.
\]

The last inequality follows from

\[
\frac{d_P}{1-e^{-d_Pm}}>\frac1m>
\frac{d_S}{e^{d_Sm}-1}.
\]

Therefore the search log slope reaches zero first and its peak remains to the
left of the price peak.  What matters is that the activation factor is common;
mechanism-specific rider continuation can reverse the result.

## 3. A stability lift for the fully optimized value gaps

Define the full outer value gaps

\[
\widehat\Delta_P(m)=V_F(m)-V_0(m),
\qquad
\widehat\Delta_S(m)=V_E(m)-V_F(m).
\]

Let

\[
\bar m=\frac1{r+\lambda_F},
\]

and define the benchmark separation margins

\[
\Gamma_P=\Delta_P^0(m_P^*)-\Delta_P^0(\bar m)>0,
\]

\[
\Gamma_S=\Delta_S^0(m_S^*)-\Delta_S^0(\bar m)>0.
\]

### Corollary 1 (uniform argmax separation)

On a compact thickness domain containing `m_S^*`, `bar m`, and `m_P^*`, assume
the full gaps are continuous and

\[
\|\widehat\Delta_P-\Delta_P^0\|_\infty<\Gamma_P/2,
\qquad
\|\widehat\Delta_S-\Delta_S^0\|_\infty<\Gamma_S/2.
\]

If

\[
\mathcal P=\arg\max_m\widehat\Delta_P(m),
\qquad
\mathcal S=\arg\max_m\widehat\Delta_S(m),
\]

then

\[
\boxed{\sup\mathcal S<\bar m<\inf\mathcal P}.
\]

For the price layer, the benchmark is increasing up to `m_P^*`, so its largest
value on `m<=bar m` is its value at `bar m`.  A uniform perturbation smaller
than half `Gamma_P` cannot move a global maximizer to that side.  The search
argument is symmetric because its benchmark is decreasing on `m>=bar m`.

This is the correct full-model theorem target.  It allows multiple optimized
policies and non-singleton argmax sets; it does not pretend that the
re-optimized envelopes are globally differentiable or uniquely peaked.

## 4. Why the common-branch condition is necessary

Let

\[
\Delta_P(m)=e^{-m}-e^{-2m},
\]

whose unique peak is `m_P^*=log 2`.  Suppose expanded search is executed with
the mechanism-specific continuation factor

\[
\eta(m)=(1-e^{-m})^2\in(0,1).
\]

Then

\[
\Delta_S(m)=\eta(m)(e^{-2m}-e^{-3m}).
\]

Writing `x=e^{-m}` gives

\[
\Delta_S=x^2(1-x)^3,
\]

which is uniquely maximized at `x=2/5`.  Hence

\[
m_S^*=\log(5/2)>\log2=m_P^*.
\]

Both gains are smooth and strictly single-peaked, yet the peak order reverses.
Rider-composition changes, WPBE branch switching, and pointwise policy
maximization can therefore invalidate the branchwise theorem.

## 5. Closing the free-search objection

The archived completion objective with free `s` is a maximal-completion
benchmark.  It may choose the search cap or any point beyond physical response
saturation.  Let `q_R(mu,a)` denote the ex-ante probability that expanded
rescue is executed.  Expected extra contacts are

\[
Q^O(\mu,a)=q_R(\mu,a)m(s-1).
\]

An economic objective can be written as completion net of notification
opportunity cost,

\[
J_\kappa(\mu,a)=B M(\mu,a)-\kappa Q^O(\mu,a),
\]

or equivalently as completion subject to a notification budget.  It should not
be called platform profit unless rider fare and driver payments are modeled
separately.

On a common branch, let expanded scope add willing-driver rate `sigma(s)` and
resource rate `n(s)` (with `n(s)=s-1` in the area model).  The net search gain is

\[
G_\kappa(s;m)=A(m)\left[
B e^{-\lambda_Fm}(1-e^{-\sigma(s)m})-\kappa m n(s)
\right].
\]

An interior scope obeys the scalar index condition

\[
\Psi(s;m)
=\frac{B e^{-[\lambda_F+\sigma(s)]m}\sigma'(s)}
{\kappa n'(s)}=1.
\]

Search should expand when `Psi>1` and contract when `Psi<1`.  If
`kappa*n(s)>=B*sigma(s)` for every feasible `s`, then
`1-e^{-x}<=x` implies `G_kappa(s;m)<=0`: extra search is never worthwhile.
For zero `kappa`, the first-order condition disappears and the optimum is
governed by the search cap or physical response saturation, exactly as a
sophisticated reader would expect.

## 6. Relation to neighboring theorem styles

- [Afèche, Liu, and Maglaras (2023)](https://doi.org/10.1287/msom.2023.1221)
  use scarce/moderate/ample thresholds and characterize when nested controls
  have strictly positive value.  Their proposition is a zero-positive-zero
  interval result, not a unique-peak theorem.
- [Zhao, Papier, and Teo (2024)](https://doi.org/10.1287/msom.2021.0354)
  establish a quasi-convex thickness effect and an intermediate optimum; weak
  quasi-convexity alone does not imply uniqueness.
- [Wang, Zhang, and Zhang (2024)](https://doi.org/10.1287/opre.2022.2399)
  characterize matching scope through a scalar index crossing.  The `Psi=1`
  search-cost condition above follows that proof style.
- [Hu, Hu, and Zhu (2022)](https://doi.org/10.1287/msom.2020.0960) build from
  individual threshold behavior to equilibrium regimes and then policy
  comparisons.  The proposed chain follows the same discipline: cutoff-WPBE,
  branchwise ordered peaks, and only then a stability lift to mechanism design.

The new claim is not that thickness effects or search-radius controls exist.
It is the strict ordering of the peak locations of two adjacent, nested rescue
controls, with a transparent condition under which the ordering survives the
full equilibrium-constrained outer design.

# Numerical falsification report

Date: 2026-08-25  
Scope: announced escalation, with `gamma=0` as the main baseline and a smaller
positive-entry stress test. The manuscript itself was not edited.

## Bottom line

1. I found **no numerical counterexample** to the flat benchmark, the claimed
   local derivative, no-entry cutoff uniqueness, the fixed-`p1` optimizer, or
   the `P(a),Q(a),J(a)` global parameterization.
2. I found **no multiple symmetric cutoff equilibrium** in 38,675 structured
   no-entry policies, 55,440 structured positive-entry policies, or 100,000
   randomized no-entry policies checked through an independent reduced
   equation. A 120-policy arbitrary-precision interval-style sample agreed
   with the fast all-root enumerator and left no unresolved same-sign boxes.
   These counts are falsification evidence, not a proof.
3. I found **no discontinuity or nonattainment signature** in the no-entry
   problem. The independent nested optimizer and compact `P,Q,J` optimizer
   agree to binary64 accuracy in moderate test cases. The exact compact
   parameterization in `global_noentry_geometry.md`, rather than this grid,
   is what supports attainment.
4. **Strict single-peakedness is false for `beta<1/2`.** A proof-level
   certificate is given below: for `beta=1/5`, every `alpha>0`, and
   `gamma=0`, the gain is exactly zero for all `0<m<=1` but is strictly
   positive at `m=12`.
5. For the maintained `beta>=1/2` baseline, an adversarial 54-profile scan
   over `alpha in [1e-8,1]` and `m in [1e-5,1e6]` found exactly one sampled
   up-to-down change and no down-to-up reversal in every profile. It also
   found one derivative-certified stationary maximum of `J` at every sampled
   parameter point. This supports, but does not prove, strict
   single-peakedness in that region.

## What was implemented

The code is under `announced_escalation_overhaul/code/`.

- `model.py` independently transcribes the payoff, rider-mass, cutoff, and
  completion formulas. It uses `expm1`, series at zero, and the stable identity

  \[
  C_2-C_1=e^{-\lambda_1}
  \{1-e^{-m(\alpha+\gamma)(p_2-p_1)}\}
  \]

  to avoid the `0/0` cancellation near a flat menu. Binary64 and mpmath paths
  are separate.
- `equilibria.py` has two all-branch solvers. The fast solver partitions at
  the rider kink, combines uniform and endpoint-clustered grids, brackets every
  sign change, and explicitly searches for even-multiplicity candidates. The
  high-precision solver recursively excludes boxes using monotone natural
  interval bounds for all payoff factors. A same-sign box that cannot be
  excluded is retained as `unresolved`; it is never silently dropped.
- `optimize.py` first optimizes `p2` conditional on `p1`, then `p1`. Every
  policy value is the minimum completion over every enumerated cutoff. It
  samples both sides of branch-regime boundaries to look for jumps and
  one-sided nonattainment.
- `noentry.py` implements the independent no-entry reduction

  \[
  D_{p,q}(a)=m e^{ma}f_m(a;p,q)
   =(p-a)h(a)-
   \frac{\max\{(\beta-p)C(p-a),(\beta-q)C(q-a),0\}}
        {\beta(1-p)}.
  \]

- `geometry.py` implements the no-entry rescue envelope and the lower
  quadratic branch in the cutoff coordinate. It solves

  \[
  z+\log(1+z)=\alpha m(\beta-a)
  \]

  instead of exponentiating a large endpoint, so it remains stable through
  `m=1e12`. It has an 80-digit stationary-point and value-difference path.
- `run_falsification.py` reproduces the scans with seed `20260825`.
  `test_engine.py` contains 11 deterministic regression tests.

The root-box code is deliberately described as *interval-style*: calculations
use high precision and a rounding pad, not a formal directed-rounding package.
The reported boxes are candidate numerical certificates, not computer-assisted
proofs.

## Flat benchmark and local derivative

For flat menus in four cases spanning thin/thick markets, `gamma=0` and
`gamma>0`, the all-root solver returned exactly `a=p`; the encoded completion
and the closed-form flat completion agreed exactly in binary64. For
`gamma=0`, the FOC solver and the Lambert-`W` expression for `p_F` differed by
at most `1.63e-16` over `m in {0.001,0.1,2,10,100}`.

The table compares the manuscript's right derivative with the finite
difference at `epsilon=1e-7`.

| `(m,alpha,beta,gamma;p)` | claimed `L` | quotient | relative error |
|---|---:|---:|---:|
| `(2,.8,.7,0;.3)` | 0.259022397696287 | 0.259022263082720 | `-5.20e-7` |
| `(.1,1,.9,0;.4)` | 0.0114679022929602 | 0.0114678773074917 | `-2.18e-6` |
| `(10,.2,.6,0;.2)` | 0.130784091518556 | 0.130784049146016 | `-3.24e-7` |
| `(2,.8,.7,.3;.3)` | 0.299528296565859 | 0.299528116198822 | `-6.02e-7` |

At the first case, an mpmath calculation at `epsilon=1e-8` gives
`0.2590223878377596600`; its unique cutoff lies in a sign-changing box whose
width is below `6e-30`. The first-order error decreases linearly with
`epsilon`, as expected.

## All-root and multiplicity attack

### Structured grids

The main no-entry grid used

\[
m\in\{.03,.1,.3,1,3,10,30\},\quad
\alpha\in\{.1,.3,.6,.9,1\},\quad
\beta\in\{.2,.4,.6,.8,.95\},
\]

with 13 first-payment and 17 rescue-payment nodes below `beta`. There were
38,675 policies and no multiple cutoff set. Prices at or above `beta` are
repeat-only and were checked separately through the flat inequality.

The positive-entry grid used the same thicknesses,
`alpha in {0,.1,.5,1}`, `beta in {.2,.5,.8,.95}`,
`gamma in {.03,.1,.3,1,3}`, and 9-by-11 policy nodes. None of its 55,440
policies had multiple cutoffs.

A separate randomized no-entry attack evaluated the max-of-two-branches
residual on 97 cutoff nodes for 100,000 policies with
`m in [1e-3,10^2.5]`, `alpha in [1e-4,1]`, and the full interior patience and
policy ranges. It found no two-sign-change residual. The identity
`D=m exp(ma) f` had maximum scaled discrepancy `8.89e-16`.

Finally, 120 random policies, including 40 with `gamma>0`, were recertified
with 65-digit box exclusion at cutoff tolerance `1e-18`. The fast and
high-precision cutoff lists all matched within `2e-8`; there were zero
unresolved same-sign boxes.

### Example root certificate

For

\[
(m,\alpha,\beta,\gamma;p_1,p_2)=(2,.8,.7,0;.3,.5),
\]

the endpoint residuals are

\[
f(0)=0.1444013844106697359>0,\qquad
f(.3)=-0.03067195816520658369<0.
\]

The only non-excluded root box is

\[
\begin{aligned}
a\in[&0.247603638015325833415717716842298808506440127,\\
     &0.247603638015325833415717716842299155173830117],
\end{aligned}
\]

with endpoint residuals `+9.13e-35` and `-1.21e-34`. Completion at the
midpoint is

\[
M=0.33124166008827020356393512273206222214.
\]

This is a sign-bracket certificate for one root plus interval-style exclusion
of the remainder of `[0,p1]`; it is not a formal uniqueness proof.

## Independent `P,Q,J` audit

The envelope implementation was attacked independently of the original
payoff code.

- Across 100,000 random points with `m in [1e-5,1e6]`,
  `alpha in [1e-8,1]`, and `beta in [.01,.999]`, there was no violation of
  `a<=P(a)<=Q(a)<=beta`. On the moderate subset, the largest original cutoff
  residual was `1.39e-15` and the largest discrepancy between original
  completion and `J(a)` was `3.67e-15`.
- On 2,250 parameter curves with 501 cutoff nodes each, `P(a)` never
  decreased. The largest discrepancy in `P(0)=p_z` was `3.00e-15`.
- On 4,320 parameter points covering the same broad `m/alpha` ranges and 12
  patience values from `.05` to `.99`, the derivative-filtered `J` search
  found no case with two stationary local maxima. Boundary samples were kept
  separate; this avoids the earlier false multiple-maximum signal caused by
  nearly duplicate `a=0` or `a=beta` nodes.
- Three full nested-policy optimizations matched the scalar geometry value to
  at worst `6.7e-16`:

| `(m,alpha,beta)` | `(a,P,Q)` from geometry | dynamic value |
|---|---|---:|
| `(2,.8,.7)` | `(.3359434665,.3728622646,.5053767075)` | 0.340550397080060 |
| `(10,1,.9)` | `(.1254403081,.1582942089,.3174996007)` | 0.759180045186831 |
| `(.1,.5,.8)` | `(.4575806146,.4927256607,.6284244211)` | 0.0244314771452954 |

The envelope FOC residual

\[
e^{\alpha m(Q-a)}-1-\alpha m(\beta-Q)
\]

was at most `5.33e-15` in these cases.

At `(m,alpha,beta)=(2,.8,.7)`, the fixed-`p` boundary formulas give
`p_z=0.124432569928620` and `Q(0)=0.305699901760710`. Direct conditional
optimization returns `a=0, q=Q(0)` for `p=.02`, `.08`, and just below
`p_z`; just above `p_z`, the optimizer moves continuously to a positive
cutoff. No hidden larger root was found.

## Discontinuity and nonattainment diagnostics

At fixed `p1`, the code brackets changes among flat-upper-boundary,
interior, and reject-all regimes, then evaluates both sides at successively
smaller distances. Representative policies at

- `(m,alpha,beta,gamma;p1)=(2,.8,.7,0;.1)`,
- `(2,.8,.7,.3;.1)`, and
- `(20,1,.6,1;.07)`

showed continuous one-sided convergence at every detected regime boundary.
No boundary value was dominated by a converging one-sided sequence, so there
was no nonattainment signature.

For `gamma=0`, the stronger finding is structural: the numerically verified
`P,Q,J` map places the outer problem on a compact cutoff interval, and its
value matches the nested problem. Thus the companion exact geometry argument
supports attainment. For `gamma>0`, the scans are only negative evidence;
they do not prove continuity, uniqueness, or attainment.

## Thickness and strict single-peakedness

### An exact counterexample for `beta<1/2`

Take `beta=1/5`, any `alpha>0`, and `gamma=0`. Let

\[
\beta_L(m)=-\frac1m\log(1-F_0^*(m)).
\]

Since the flat payment `p=1/2` is feasible,

\[
F_0^*(m)\ge \frac12(1-e^{-m/2}),
\]

and therefore

\[
\beta_L(m)\ge
g(m):=-\frac1m\log\frac{1+e^{-m/2}}2.
\]

The numerator of `g` is a concave function that vanishes at zero, so `g` is
decreasing. Hence for `0<m<=1`,

\[
\beta_L(m)\ge g(1)
=-\log\frac{1+e^{-1/2}}2
=0.2190701963798386>\frac15.
\]

The patience-threshold lower bound in `global_noentry_geometry.md` therefore
gives

\[
D_{\alpha,0}^*(m)=F_0^*(m),\qquad V_{\alpha,0}(m)=0,
\quad 0<m\le1.
\]

At `m=12`, the flat FOC has `p_F(12)=0.197018621924275<1/5` (equivalently,
the FOC residual at `p=1/5` is positive). The strict-menu comparison then
gives `V(12)>0`. Thus `V` has a nondegenerate initial zero plateau but later
becomes positive. It cannot be strictly increasing before a unique peak.

This certificate is exact conditional on the companion no-entry scalar
reduction and patience-threshold theorem; it is not based on the policy grid.
The equation `p_F(m)=1/5` has the numerical nonzero root
`m=11.6833149113153`, which is a useful candidate transition marker but is not
needed for the counterexample.

### Baseline search for `beta>=1/2`

The main search used

\[
\alpha\in\{10^{-8},10^{-7},\ldots,10^{-1},1\},\quad
\beta\in\{.5,.500001,.55,.7,.9,.99\},
\]

and 101 logarithmic thickness nodes from `1e-5` to `1e6`. Each of the 5,454
optimized points was refined through the scalar geometry, and the gain was
subtracted at 50 decimal digits. Every one of the 54 profiles had:

- exactly one sampled positive-to-negative log-slope change;
- no negative-to-positive reversal;
- exactly one derivative-certified stationary `J` maximum at every thickness.

The grid peak ranged from `m=8.7096` to `m=281838`, the latter occurring as
`alpha` approached zero. No robust optimizer switch appeared. For the
reference `(alpha,beta)=(1,.9)`, a further continuous refinement gives

\[
\begin{aligned}
m&\approx9.2548017801,\\
V(m)&\approx0.06568556953038875,\\
(a,p_1,p_2)&\approx
(.131770419046,.167064261906,.330189730736).
\end{aligned}
\]

This is strong negative evidence against a simple counterexample, but a
narrow derivative reversal between nodes or a tangential optimizer switch is
not excluded. Strict single-peakedness for `beta>=1/2` remains open.

## Endpoint asymptotic cross-checks

At the critical patience `beta=1/2`, 80-digit optimization at `m=1e-5`
gives:

| `alpha` | `V` | `V/m^4` | claimed `alpha/2048` |
|---:|---:|---:|---:|
| 1 | `4.88278198250e-24` | `4.88278198250e-4` | `4.8828125e-4` |
| `1e-8` | `4.88276977560e-32` | `4.88276977560e-12` | `4.8828125e-12` |

The convergence is consistent with `V~alpha*m^4/2048`.

For `(alpha,beta)=(1,.9)`, the following slow-moving ratios are consistent
with the thick-market claims
`1-D*~log(log m)/m` and `V~log(m)/m`:

| `m` | `m(1-D*)/log(log m)` | `mV/log m` |
|---:|---:|---:|
| `1e4` | 1.6428 | 0.7125 |
| `1e6` | 1.5144 | 0.7846 |
| `1e8` | 1.4482 | 0.8252 |
| `1e10` | 1.4069 | 0.8518 |
| `1e12` | 1.3781 | 0.8707 |

The ratios approach one slowly and show no contradictory scaling.

## Reproduction

From the workspace root:

```bash
PYTHONPATH=announced_escalation_overhaul/code \
  python -m unittest -v announced_escalation_overhaul/code/test_engine.py

PYTHONPATH=announced_escalation_overhaul/code \
  python announced_escalation_overhaul/code/run_falsification.py --quick

PYTHONPATH=announced_escalation_overhaul/code \
  python announced_escalation_overhaul/code/run_falsification.py --full
```

The full run can also be split deterministically:

```bash
for section in benchmark roots geometry thickness; do
  PYTHONPATH=announced_escalation_overhaul/code \
    python announced_escalation_overhaul/code/run_falsification.py \
      --full --section "$section"
done
```

## Interpretation limits

- Grid and randomized scans cannot prove uniqueness, absence of narrow
  optimizer switches, or single-peakedness.
- A sign-changing root bracket proves existence for the evaluated
  high-precision function; exclusion of all other boxes here is a strong
  numerical certificate, not a formal interval proof.
- The exact zero-plateau counterexample relies on the exact no-entry scalar
  reduction and patience-threshold bound already developed in the companion
  analysis. It does not extend automatically to `gamma>0`.
- Positive-entry results should therefore be read only as exploratory
  falsification evidence.

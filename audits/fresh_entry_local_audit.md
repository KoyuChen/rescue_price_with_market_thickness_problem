# Fresh-entry local positivity: independent proof and localization audit

## Verdict

Fix

\[
 m>0,\qquad 0<p<\beta<1,\qquad
 0\le\alpha\le1,\qquad \gamma\ge0,
 \qquad \alpha+\gamma>0.
\]

Let

\[
 x=mp,\quad R=e^{-x},\quad E=e^{-\gamma x},\quad
 \sigma=\phi(x),\quad \ell=\phi(\gamma x),\quad
 \rho=\frac{1-p/\beta}{1-p}.
\]

The sign expression in the prompt is

\[
 T=E(\alpha+\gamma)\sigma
 -R\alpha\ell\{1-\rho+\rho E(1+\gamma)\}.       \tag{1}
\]

The result is **true as stated**:

\[
 \boxed{\bar v<1\quad\Longrightarrow\quad T>0}
\]

for every maintained parameter vector.  No restriction such as
`gamma<=1` is needed.  The proof does naturally split at `gamma=1`:

- for `0<=gamma<=1`, positivity holds even without the active-rescue
  condition;
- for `gamma>1`, the active condition is essential in the only potentially
  dangerous exponential region.

The localization bound and cutoff coefficient also check exactly:

\[
 0\le p-a_\varepsilon
 \le\frac{\alpha\rho}{1-\alpha\rho}\varepsilon,
 \qquad
 \boxed{
 \kappa=
 \frac{R\alpha\ell\eta^0}
 {\sigma-R\alpha\rho\ell}},                     \tag{2}
\]

where

\[
 \bar v=\frac1\beta\left[p+
 \frac{1-E}{mE(\alpha+\gamma)}\right],
 \qquad
 \eta^0=\frac{1-\bar v}{1-p}>0.                \tag{3}
\]

## 1. A sign-equivalent form of T

First take `gamma>0` and define

\[
 u=e^x-1,\qquad t=1-E,\qquad A=\alpha+\gamma,
 \qquad
 B=1-\rho+\rho E(1+\gamma).                    \tag{4}
\]

Since

\[
 \sigma=\frac{R u}{x},\qquad
 \ell=\frac{t}{\gamma x},
\]

equation (1) becomes

\[
 T=\frac{R}{\gamma x}
 \underbrace{\{E\gamma A u-\alpha tB\}}_{=:Q}.
 \tag{5}
\]

Thus it suffices to prove `Q>0`.  Put

\[
 \Delta:=1-E(1+\gamma),\qquad B=1-\rho\Delta.   \tag{6}
\]

The proof has three cases.

## 2. Region E(1+gamma) >= 1

**Claim.** If `Delta<=0`, then `Q>0` for every `gamma>0`, without using
active rescue.

Here `B` is a convex combination of `1` and `E(1+gamma)`, so

\[
 B\le E(1+\gamma).                              \tag{7}
\]

Moreover,

\[
 \gamma u>\gamma x>1-e^{-\gamma x}=t,          \tag{8}
\]

and, because `alpha<=1`,

\[
 A=\alpha+\gamma\ge\alpha(1+\gamma).           \tag{9}
\]

Consequently,

\[
 \begin{aligned}
 Q
 &\ge E\{\gamma A u-\alpha t(1+\gamma)\}\\
 &>E\{A t-\alpha t(1+\gamma)\}\ge0.
 \end{aligned}                                  \tag{10}
\]

The first strict inequality in (8) uses `e^x-1>x`; the second uses
`1-e^{-y}<y`.

## 3. Region E(1+gamma) < 1 with 0 < gamma <= 1

**Claim.** In this region `Q>0` without using active rescue.

Now `B<=1`.  Convexity of the exponential gives, for `0<gamma<=1`,

\[
 e^{\gamma x}\le(1-\gamma)e^0+\gamma e^x
 =1+\gamma(e^x-1).
\]

After multiplying by `E=e^{-gamma x}`,

\[
 t=E(e^{\gamma x}-1)\le E\gamma u.              \tag{11}
\]

It follows that

\[
 \begin{aligned}
 Q
 &\ge E\gamma(\alpha+\gamma)u-\alpha t\\
 &=\alpha(E\gamma u-t)+E\gamma^2u>0.           \tag{12}
 \end{aligned}
\]

Thus all `0<gamma<=1` cases are covered by Sections 2--3.

## 4. The only difficult region: gamma > 1 and E(1+gamma) < 1

This is where active rescue is needed.

### 4.1 What the active condition implies

The active condition is

\[
 \frac1\beta\left[p+\frac{t}{mEA}\right]<1.
 \tag{13}
\]

Let

\[
 s:=\frac{\beta-p}{\beta}=\rho(1-p).
\]

Using `m=x/p` and `p/beta=1-s`, (13) is equivalent to

\[
 \frac{t}{xEA}<\frac{s}{1-s},
\]

and hence

\[
 s>\frac{t}{t+xEA}.
\]

Because `rho=s/(1-p)>s`, active rescue gives the strict lower bound

\[
 \boxed{
 \rho>r_0:=\frac{t}{t+xEA}.}                    \tag{14}
\]

In the present region `Delta>0`, so `B=1-rho Delta` decreases in `rho`.
Using (14),

\[
 \begin{aligned}
 B
 &<1-r_0\Delta\\
 &=\frac{E\{xA+t(1+\gamma)\}}{t+xEA}.          \tag{15}
 \end{aligned}
\]

Substitution in (5) shows that `Q>0` follows from

\[
 I(\alpha):=
 \gamma A u(t+xEA)
 -\alpha t\{xA+t(1+\gamma)\}>0.                \tag{16}
\]

Indeed,

\[
 Q\ge\frac{E}{t+xEA}I(\alpha),                  \tag{17}
\]

with strict inequality when `alpha>0` (and equality possible at
`alpha=0`).  Positivity of `I` is therefore sufficient in every case.

### 4.2 I(alpha) is concave when gamma > 1

As a polynomial in `alpha`, the coefficient on `alpha^2` in (16) is

\[
 x\{\gamma E u-t\}.                             \tag{18}
\]

For `gamma>1`, strict convexity of `z mapsto e^{zx}-1`, which vanishes at
zero, gives

\[
 e^{\gamma x}-1>\gamma(e^x-1)=\gamma u.
\]

Multiplying by `E` yields `t>gamma E u`, so (18) is strictly negative.
Therefore `I` is strictly concave on `alpha in [0,1]`, and its minimum is at
an endpoint.

At `alpha=0`, `A=gamma` and

\[
 I(0)=\gamma^2u(t+xE\gamma)>0.                  \tag{19}
\]

It remains to check `alpha=1`.

### 4.3 The alpha=1 endpoint

At `alpha=1`, put

\[
 H:=t+xE(1+\gamma)>t,
 \qquad d:=\gamma u-t>0.
\]

Equation (16) becomes

\[
 \begin{aligned}
 \frac{I(1)}{1+\gamma}
 &=\gamma uH-t(t+x)\\
 &=(t+d)H-t(t+x)\\
 &=dH-tx\Delta.                                 \tag{20}
 \end{aligned}
\]

We next prove `d>x Delta`.  Since `u> x+x^2/2` and `t<gamma x`,

\[
 d=\gamma u-t>\frac{\gamma x^2}{2}.            \tag{21}
\]

Let `y=gamma x`.  In the present region `Delta>0`, so
`y>log(1+gamma)`.  The elementary inequality

\[
 1-(1+\gamma)e^{-y}<\frac y2                    \tag{22}
\]

holds for every `gamma>1` and `y>=log(1+gamma)`.  To see this, define

\[
 f(y)=\frac y2-1+(1+\gamma)e^{-y}.
\]

On that half-line its unique minimizer is
`y_*=log(2(1+gamma))`, and

\[
 f(y_*)=\frac{\log(2(1+\gamma))-1}{2}>0
\]

because `2(1+gamma)>4>e`.  This proves (22).  Combining (21)--(22),

\[
 d>\frac{xy}{2}>x\Delta.                        \tag{23}
\]

Since `H>t`, (20) and (23) give

\[
 dH>x\Delta H>x\Delta t,
\]

so `I(1)>0`.  Concavity and (19) now imply

\[
 I(\alpha)>0\quad\text{for every }0\le\alpha\le1.
\]

Equations (17) and (5) prove `T>0` in the last remaining region.

## 5. The gamma=0 boundary

If `gamma=0`, then `E=ell=1`.  Since `alpha+gamma>0`, `alpha>0`, and

\[
 T=\alpha(\sigma-R).
\]

For `x>0`,

\[
 \sigma-R=\frac{1-(1+x)e^{-x}}x>0,
\]

because `e^x>1+x`.  Thus `T>0` also at the no-entry boundary.

Sections 2--5 exhaust all parameters and complete the proof.

## 6. Why active rescue cannot be deleted for gamma > 1

The active condition is not a cosmetic assumption in the large-entry
region.  For an exact counterexample outside it, take

\[
 x=1,\quad p=\frac12,\quad m=2,\quad
 \beta=\frac{51}{100},\quad
 \alpha=1,\quad\gamma=10,
 \quad\rho=\frac2{51}.
\]

Then

\[
 T=11e^{-10}(1-e^{-1})
 -e^{-1}\frac{1-e^{-10}}{10}
 \left\{\frac{49}{51}+\frac{22}{51}e^{-10}\right\}<0. \tag{24}
\]

For a simple rigorous certificate, use
`e^10>20000` and `e<3`.  The first term in (24) is less than
`11/20000`, while the second is greater than

\[
 \frac13\frac{19999}{200000}\frac{49}{51},
\]

which is larger than `11/20000`.  This parameter vector is very far from
active:

\[
 \frac{1-e^{-10}}{2e^{-10}(11)}
 =\frac{e^{10}-1}{22}>900,
\]

so `bar v>1`.  The maintained local theorem is unaffected, but an
unconditional claim `T>0` for all `gamma` would be false.

## 7. Independent localization derivation

Consider the nearby menu

\[
 p_1=p,\qquad p_2=p+\varepsilon,\qquad
 \delta:=p-a\in[0,p].
\]

Conditional on failure, the two acceptable-supply means are

\[
 \lambda_1=m(\alpha\delta+\gamma p),
 \qquad
 \lambda_2=\lambda_1+m(\alpha+\gamma)\varepsilon. \tag{25}
\]

Let `eta_epsilon(a)` be the posting-conditional rescue mass.  The repeat mass
is `rho-eta_epsilon`.  At a positive interior cutoff, cutoff-driver
indifference is

\[
 \begin{aligned}
 \phi(ma)\delta
 =\alpha e^{-ma}\{&[\rho-\eta_\varepsilon(a)]
       \phi(\lambda_1)\delta\\
 &+\eta_\varepsilon(a)\phi(\lambda_2)
       (\delta+\varepsilon)\}.
 \end{aligned}                                  \tag{26}
\]

Rearranging,

\[
 \begin{aligned}
 &\left[\phi(ma)-\alpha e^{-ma}
 \{(\rho-\eta_\varepsilon)\phi(\lambda_1)
 +\eta_\varepsilon\phi(\lambda_2)\}\right]\delta\\
 &\hspace{35mm}
 =\alpha e^{-ma}\eta_\varepsilon
 \phi(\lambda_2)\varepsilon.                  \tag{27}
\end{aligned}
\]

Use `phi(lambda_j)<=1`, `eta_epsilon<=rho`, and
`phi(ma)>=e^{-ma}`.  The bracket in (27) is at least

\[
 e^{-ma}(1-\alpha\rho)>0.
\]

Consequently every interior equilibrium satisfies

\[
 0\le\delta\le
 \frac{\alpha\rho}{1-\alpha\rho}\varepsilon.  \tag{28}
\]

The same bound holds for a reject-all candidate: its lower-boundary
accept-minus-wait inequality has the weak direction corresponding to (27),
and the same upper bounds give

\[
 p\le\frac{\alpha\rho}{1-\alpha\rho}\varepsilon.
\]

For fixed `p>0`, this is impossible for all sufficiently small epsilon.  The
upper boundary `a=p` trivially satisfies (28).  Thus **every** equilibrium is
localized; this is not merely a statement about one selected branch.

## 8. Limiting rider mass and kappa

For a bounded rescaled displacement `y=delta/epsilon`, the rider switch type
can be written

\[
 v^M_\varepsilon
 =\frac p\beta+
 \frac{\varepsilon C_2}{\beta(C_2-C_1)},
 \qquad C_j=1-e^{-\lambda_j}.                   \tag{29}
\]

From (25), uniformly for bounded `y`,

\[
 \frac{C_2-C_1}{\varepsilon}
 \longrightarrow mE(\alpha+\gamma),
 \qquad C_2\longrightarrow1-E.
\]

Therefore

\[
 v^M_\varepsilon\longrightarrow
 \bar v=\frac1\beta\left[p+
 \frac{1-E}{mE(\alpha+\gamma)}\right].         \tag{30}
\]

The formula also covers `gamma=0`: then `C_2` itself is order epsilon and
the second term in the limit is zero.  If `bar v<1`, the limiting rescue mass
is

\[
 \eta^0=\frac{1-\bar v}{1-p}>0.                \tag{31}
\]

Divide (26) by `epsilon`, put `delta=epsilon y`, and let epsilon decrease to
zero.  Since

\[
 a\to p,\quad \lambda_j\to\gamma x,\quad
 \eta_\varepsilon\to\eta^0,
\]

the limiting rescaled equation is

\[
 [\sigma-R\alpha\rho\ell]y
 -R\alpha\eta^0\ell=0.                         \tag{32}
\]

The slope is strictly positive:

\[
 \sigma-R\alpha\rho\ell>\sigma-R>0,           \tag{33}
\]

where the first inequality uses `alpha rho ell<1` and the second uses
`e^x>1+x`.  The unique root of (32) is exactly (2).

The localization bound restricts all roots to a fixed compact `y` interval.
When `bar v<1`, the rider threshold stays uniformly away from its upper kink,
and the rescaled cutoff margin converges in `C^1` on that interval to the
strictly increasing affine function in (32).  Hence for small epsilon there
is at most one root; existence supplies it.  If `alpha>0`, its displacement
is interior and positive.  If `alpha=0`, drivers cannot benefit from waiting,
the unique cutoff remains `a=p`, and (2) correctly gives `kappa=0`.

If `bar v>1`, rescue is inactive for all localized candidates once epsilon is
small.  Repeat alone satisfies the strict flat inequality, so the unique
cutoff is exactly `a=p`; again `eta^0=kappa=0`.  The knife edge
`bar v=1` is correctly excluded from the stated local theorem because a
second-order rider-mass expansion is then required.

## 9. Completion derivative and the role of T

Write

\[
 S_\varepsilon
 =\rho C_1+\eta_\varepsilon(C_2-C_1).
\]

Along `a_epsilon=p-kappa epsilon+o(epsilon)`,

\[
 S'_0=mE\{\rho\alpha\kappa+
 \eta^0(\alpha+\gamma)\}.                       \tag{34}
\]

Differentiating

\[
 M_\varepsilon=(1-p)
 \{1-e^{-ma_\varepsilon}+e^{-ma_\varepsilon}S_\varepsilon\}
\]

gives

\[
 L=m(1-p)R
 \left[E(\alpha+\gamma)\eta^0-\kappa B_m\right], \tag{35}
\]

where

\[
 B_m=1-\rho+\rho E(1-\alpha).
\]

Substituting (2) and collecting terms yields the exact factorization

\[
 \boxed{
 L=m(1-p)R\eta^0
 \frac{T}{\sigma-R\alpha\rho\ell}.}            \tag{36}
\]

Indeed,

\[
 E(\alpha+\gamma)\rho+B_m
 =1-\rho+\rho E(1+\gamma),
\]

which is precisely the bracket in (1).  All factors outside `T` in (36) are
strictly positive under active rescue.  Sections 1--5 therefore prove the
claimed strict local completion gain.

## 10. Audit conclusions

1. The displayed `kappa` formula is correct, including the entry term
   `ell=phi(gamma mp)` and the limiting rescue mass `eta^0`.
2. The uniform localization bound is correct for every symmetric cutoff
   equilibrium, not only an equilibrium selected near the flat branch.
3. The local equilibrium is unique for sufficiently small positive
   escalation when `bar v!=1`; at `bar v<1` this follows from `C^1` convergence
   of the rescaled margin, and at `bar v>1` from repeat-only strictness.
4. The coefficient `T` is strictly positive throughout the active region.
   For `gamma<=1` it is actually positive without activity; for `gamma>1`
   activity is used exactly through the lower bound (14).
5. The knife edge `bar v=1` genuinely needs separate second-order analysis
   and should remain excluded.

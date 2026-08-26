# Approach and counterexample registry

## Approach families

| Family | Target | Key mechanism | Result or exact remaining gap | Falsification | Status |
|---|---|---|---|---|---|
| Blind extensive-form reconstruction | general WPBE | Palm rivals, Poisson marking, sequential payoffs, tie rules | complete arbitrary-menu cutoff correspondence | boundary and zero-coverage audit | PROVED / AUDITED |
| General-entry local blow-up | marginal rescue with incumbent discount | uniform localization in $y=(p-a)/\varepsilon$ and affine limiting margin | $\kappa_\delta$ and $T_\delta>0$ proved whenever $\bar v<1$ | high-precision derivative checks and discounted inactive counterexample | PROVED WITH SHARP ACTIVITY SCOPE |
| No-entry downward crossing | cutoff uniqueness | active-rescue scalar ratio has negative log derivative at every zero | every no-entry menu has one numeric cutoff | 38,675 structured and 100,000 random policies | PROVED / RED-TEAMED |
| Discounted completion identity | global comparison | cutoff indifference eliminates continuation coverage but not physical delay | $M=(1-p)m\phi(ma)[a+(p-a)/\delta]$; old formula only at $\delta=1$ | primitive/reduced-form identity cross-check | PROVED / RED-TEAMED |
| Fixed-$p_1$ rescue envelope | conditional policy design | strict concavity of $A(a,q)$ and smallest implementable cutoff | reject-all, tangent, repeat-only regimes exactly solved | nested optimizer versus geometry | PROVED / RED-TEAMED |
| Lower quadratic inversion | outer menu design | feasible root $P_\delta(a)$ lies below unchanged envelope maximizer $Q(a)$ | compact scalar $J_\delta(a)$ and policy attainment | discounted geometry and residual cross-checks | PROVED / RED-TEAMED |
| Two patience comparative statics | rider $\beta$ and driver $\delta$ | menu reuse in $\beta$; pointwise $J_\delta$ derivative in $\delta$ | gain set $(\beta_c,1)$; $D^*$ weakly falls and $\beta_c$ weakly rises in $\delta$ | threshold and boundary scans | PROVED / RED-TEAMED |
| Fixed-coordinate topology | continuity and attainment | $a\in[0,\beta]$ for every $m$; Berge theorem | values continuous; scalar argmax UHC | optimizer-boundary diagnostics | PROVED / RED-TEAMED |
| Uniform thin asymptotics | optimized $m\downarrow0$ value | uniform discriminant and compact rescaled argmax expansions | $\beta>1/2$: $m$ for $\delta<1$, $m^2$ at $\delta=1$; $\beta=1/2$: exact $m^3$ coefficient versus $\alpha m^4/2048$ with a fourth-order certificate; $\beta<1/2$: exact plateau | discounted critical-rate checks | PROVED AFTER STRUCTURAL REWRITE |
| Policy-uniform thick bounds | optimized $m\to\infty$ value | exact loss split and full-domain lower bound | dynamic loss $\log\log m/m$; gain $\log m/m$, uniformly over $\delta\in(0,1]$ for fixed positive $(\alpha,\beta)$ | ratios through $m=10^{12}$ | PROVED / SHARP UNIFORMITY RECORDED |
| Thickness shape attack | strict single-peakedness | exact plateau plus derivative/optimizer-switch search | false for $\beta<1/2$; open for $\beta\ge1/2$ | 54 profiles on $[10^{-5},10^6]$ | DISPROVED / OPEN BY REGION |
| Public deterministic supply | impatience versus competition | binomial share $s_n(a)$ and finite-population localization | $\delta<1$: gain for every $n$; $\delta=1$: gain iff $n\ge2$ | exact derivative decomposition | PROVED / AUDITED |
| Adversarial literature map | novelty boundary | nearest-neighbor threat matrix | defensible contribution is the exact intersection, not failure-contingent pay itself | primary-source metadata verification | COMPLETED |
| First-response and profit extensions | robustness | response-time race or resource-cost objective | new equilibrium and objective required | none claimed | OPEN / OUT OF BASELINE |

## Exact counterexamples and killed claims

### C1. Strict single-peakedness for impatient riders

Take $\beta=1/5$, any $\alpha>0$, and $\gamma=0$.  The patience lower bound
implies

\[
V_{\alpha,\delta,0}(m)=0\qquad(0<m\le1),
\]

while $p_F(12)<1/5$ and the strict same-$p$ theorem gives $V(12)>0$.
Therefore $V$ cannot be strictly increasing from zero thickness to a unique
peak.  This is an analytic certificate, not a grid pattern.

### C2. Activity cannot be deleted from the fresh-entry sign theorem

At

\[
x=1,\quad p=1/2,\quad m=2,\quad \beta=51/100,\quad
\alpha=1,\quad\gamma=10,\quad\delta=1/2,
\]

the limiting rider switch satisfies $\bar v>1$ and

\[
T_\delta=11e^{-10}(1-e^{-1})-
\frac12e^{-1}\frac{1-e^{-10}}{10}
\left(\frac{49}{51}+\frac{22}{51}e^{-10}\right)<0.
\]

Thus $T_\delta>0$ for arbitrary $\gamma$ is true in the active region, not
unconditionally.

### C3. Thick-market convergence is not primitive-uniform

Along $\alpha_m=m^{-2}$ with fixed $\beta>0$, the continuation envelope
satisfies $T_m\le1/m$, and the same loss minimization gives

\[
1-D_{\alpha_m,\delta,0}^*(m)=\Theta(\log m/m),
\]

not $\log\log m/m$.  The thick theorem must fix positive $\alpha$ and
$\beta$ before taking $m\to\infty$.  No analogous lower bound on $\delta$
is needed: the sharp rates hold uniformly over $\delta\in(0,1]$.

### C4. Boundary and tie corrections

1. “If all continuation actions yield zero” failed to select a
   positive-measure abandon/repeat tie when repeat coverage is zero.  The
   rule is now based on the maximal continuation payoff.
2. The original cutoff display overlapped lower and upper tests at $p_1=0$;
   the zero cutoff now carries its lower-boundary reject action explicitly.
3. The policy domain contained $(1,1)$ without an off-path equilibrium
   convention; the paper now sets its cutoff set to $\{1\}$ and completion
   to zero.
4. A positive known-$n$ derivative without $\alpha>0$ would be false; the
   proposition now displays the survival assumption and records the
   $\alpha=0$ zero derivative.

### C5. The undiscounted thin-market orders cannot be reused

With $\alpha=1$, $\delta=1/2$, and $\beta=3/4$, the discounted limiting
objective satisfies

\[
\liminf_{m\downarrow0}\frac{V_{1,1/2,0}(m)}m
\ge \frac{(3-\sqrt6)^2}{24}>0.
\]

Thus the old $O(m^2)$ patient-market rate is false once incumbents strictly
discount.  At $\beta=1/2$ the exact replacement is

\[
V_{\alpha,\delta,0}(m)
\sim\frac{\alpha(1-\delta)}
{512\{1-\alpha(1-\delta)/2\}}m^3,
\]

not the undiscounted $\alpha m^4/2048$ rate.

### C6. One-incumbent neutrality is a boundary result

The public-$n$ derivative is

\[
(1-p)n\kappa_n\left\{\frac{1-\delta}{\delta}s_n(p)
-p s_n'(p)\right\}.
\]

For $n=1$, $s_1=1$ and $s_1'=0$, so the derivative is strictly positive
whenever $\delta<1$ and is zero only at $\delta=1$.  Assignment competition
is therefore an amplification channel, not the sole mechanism.

## Routes deliberately not promoted to theorems

- No uniqueness or single-peakedness of the outer scalar $J(a)$ is used.
- The 54-profile thickness search is evidence only for $\beta\ge1/2$.
- The full original-menu optimizer correspondence has not been proved upper
  hemicontinuous; only scalar and flat argmax correspondences have.
- General fresh-entry equilibrium and local gain are proved, but global
  fresh-entry policy attainment and optimizer geometry remain open.
- No result is generalized to asymmetric or mixed WPBE, first-response races,
  profit, welfare, or platform-funded bonus budgets.

# Proof claim ledger

Statuses use only **PROVED**, **DISPROVED**, **NUMERICALLY OBSERVED**, and
**OPEN**. A result is marked PROVED only after a complete derivation, an
independent audit, boundary review, and computational falsification where
applicable. All equilibrium claims below concern anonymous symmetric pure
driver-cutoff WPBE unless a different scope is stated.

| ID | Claim | Exact scope | Status | Proof and audit certificate |
|---|---|---|---|---|
| P1 | Poisson coverage, Palm assignment share, failure posterior, and terminal intensities | all primitives; fixed cutoff | PROVED | Paper Lemma 1 and Appendix A; blind WPBE reconstruction; zero-intensity limits checked |
| P2 | Rider posts iff $v\ge p_1$ and has the stated abandon/repeat/rescue thresholds | all legal menus | PROVED | Paper Section 4 and Appendix A; maximal-zero and positive repeat--rescue ties repaired |
| P3 | Driver accept-minus-discounted-wait margin is strictly single crossing in cost | $p_1>0$, $0<\delta\le1$ | PROVED | Paper (4)--(7); strict coefficient bound at $a=0$ and $a>0$ |
| P4 | $\mathcal E_m^{\alpha,\delta,\gamma}(p_1,p_2)$ is nonempty and compact | all legal menus, $0<\delta\le1$ | PROVED | Paper Proposition 1 and Appendix A; $p_1=0$ and $(1,1)$ treated separately |
| P5 | Branch completion is continuous and the conservative minimum is well defined | all legal menus | PROVED | Paper (9)--(11); compact-equilibrium argument |
| P6 | A flat menu has unique numeric cutoff $a=p$ | $m>0$, $p>0$, all $\alpha,\gamma$, $0<\delta\le1$ | PROVED | Paper Proposition 2; incumbent discount does not change terminal eligibility |
| P7 | Flat completion formula and flat-policy attainment | all primitives | PROVED | Paper (12)--(13); direct terminal-entry derivation |
| L1 | Every nearby cutoff localizes and the active marginal-rescue menu has a unique cutoff | $0<p<\beta$, $\bar v<1$, all $\gamma\ge0$, $\alpha+\gamma>0$, $0<\delta\le1$ | PROVED | Paper Theorem 1, (L3)--(L4), Appendix A; independent discounted-WPBE audit |
| L2 | A small announced rescue strictly raises completion when marginal rescue is active | same scope as L1 | PROVED | $T_\delta=T_1+(1-\delta)R\alpha\ell\{1-\rho+\rho E(1+\gamma)\}>0$ under activity |
| L3 | $T_\delta>0$ without the activity condition for all entry rates | unrestricted $\gamma$ | DISPROVED | Counterexample $x=1,p=1/2,\beta=51/100,m=2,\alpha=1,\gamma=10,\delta=1/2$; activity fails |
| G1 | No-entry positive-cutoff completion identity | $\gamma=0$, positive cutoff, $0<\delta\le1$ | PROVED | $M=(1-p)m\phi(ma)[a+(p-a)/\delta]$ in Paper (20); old identity is only the $\delta=1$ boundary |
| G2 | Every no-entry menu has a unique numeric cutoff | $\gamma=0$, all menu and parameter boundaries | PROVED | Paper Theorem 2; global downward-crossing lemma; `global_geometry_redteam.md` |
| G3 | Every strict active menu beats the same flat first payment | $\gamma=0$, $\alpha>0$, $0<p<q<\beta$ | PROVED | Paper (22), including reject-all and positive-cutoff regimes |
| G4 | Exact fixed-$p_1$ rescue optimizer: reject-all, tangent, and repeat-only regimes | $\gamma=0$, $\alpha>0$ | PROVED | Paper Theorem 3 and Appendix B; implementability and all boundaries red-teamed |
| G5 | Full menu value is attained and has the scalar $P,Q,J$ representation | $\gamma=0$, $\alpha>0$ | PROVED | Paper (33)--(35), Theorem 4; lower quadratic branch and endpoint injectivity audited |
| G6 | Optimized announced policy strictly dominates optimized flat | $\gamma=0$, $\alpha>0$, $\beta\ge1/2$, every finite $m>0$ | PROVED | Paper Theorem 4; $p_F(m)<1/2$; equality case $\beta=1/2$ included |
| G7 | Strict-gain patience region is exactly $(\beta_c(m,\alpha,\delta),1)$ with bounds and scalar test | $\gamma=0$, $m>0$, $\alpha>0$, fixed $0<\delta\le1$ | PROVED | Paper Theorem 5 and Appendix B; fixed-menu monotonicity plus value continuity |
| G8 | Completion is weakly decreasing in driver patience $\delta$, and $\beta_c$ is weakly increasing in $\delta$ | no-entry, fixed $(m,\alpha,\beta)$ | PROVED | Paper (38a), (42a); pointwise derivative of the exact scalar objective |
| T1 | $D^*(m)$, $F^*(m)$, and $V(m)$ are continuous | fixed positive $(\alpha,\beta,\delta)$, $\gamma=0$ | PROVED | Fixed compact cutoff coordinate and Berge maximum theorem |
| T2 | Driver discount changes the optimized thin-market order | fixed positive no-entry primitives | PROVED | $\beta>1/2$: $O(m)$ for $\delta<1$ versus $O(m^2)$ at $\delta=1$; $\beta=1/2$: exact $O(m^3)$ coefficient versus $\alpha m^4/2048$, with the fourth-order compact-argmax certificate in (54a)--(54b) |
| T3 | $1-D^*\sim\log\log m/m$ and $V\sim\log m/m$ | fixed positive $(\alpha,\beta)$, uniformly over $\delta\in(0,1]$, $m\to\infty$, $\gamma=0$ | PROVED | Exact loss decomposition; $P_m^\delta\ge a$ for the lower bound, $P_m^\delta\le P_m^1$ for the feasible upper bound, and $T_m$ is independent of $\delta$ |
| T4 | The thick-market rates are uniform as rider patience or incumbent survival approach zero | varying $\alpha$ or $\beta$ with $m$ | DISPROVED | Along $\alpha_m=m^{-2}$, $1-D^*=\Theta(\log m/m)$; by contrast T3 proves uniformity over the full interval $\delta\in(0,1]$ |
| T5 | $V(m)$ has at least one finite positive global maximizer | fixed positive $(\alpha,\beta,\delta)$, $\gamma=0$ | PROVED | Continuity, endpoint vanishing, and eventual positivity; Paper Corollary 1 |
| T6 | $V(m)$ is strictly single-peaked | $\beta<1/2$, every fixed $0<\delta\le1$ | DISPROVED | Exact initial zero interval in Paper (49); at $\beta=1/5$, $V=0$ for $0<m\le1$ but $V(12)>0$ |
| T7 | $V(m)$ is strictly single-peaked or has a unique maximizing thickness | $\beta\ge1/2$, fixed $\delta$ | OPEN | Numerical evidence does not control derivative one-crossing or optimizer switches |
| B1 | Public deterministic-$n$ local effect decomposes into impatience and assignment competition | fixed $n$, $0<\alpha\le1$, $0<p<\beta$ | PROVED | Positive for every $n\ge1$ if $\delta<1$; at $\delta=1$, positive iff $n\ge2$ and zero at $n=1$; Paper (62) |
| O1 | The full original-menu optimizer correspondence is upper hemicontinuous | no-entry | OPEN | Berge proves this only for scalar cutoff and flat argmax sets; outcome-equivalent menu representatives need a direct closed-graph proof |
| O2 | Global policy attainment and optimizer characterization with fresh entry | $\gamma>0$ | OPEN | General equilibrium and local theorem are proved; no global scalar reduction is claimed |
| O3 | Robustness to asymmetric or mixed WPBE and first-response races | extensions | OPEN | Outside the maintained equilibrium and assignment protocols |

## Numerical audit record

- The incumbent-discount extension was scanned over 150,800 policies with
  $\delta$ as low as $10^{-6}$ and $m\in[10^{-4},10^4]$; no multiplicity,
  cutoff-ordering, or same-$p$ dominance failure was found.
- An 80-case multiprecision discounted cross-check resolved apparent roots
  within one binary64 ulp of $p$ and found no mismatch.
- Ninety discounted patience curves each had exactly one zero-to-positive
  transition and no violation of the nesting in $\delta$.
- Global root isolation covered 38,675 no-entry menus and 55,440
  positive-entry menus at the nested boundary $\delta=1$; no contradiction
  to the proved cutoff results was found.
- A 120-case multiprecision cross-check matched the double-precision root
  enumerator.
- Geometry falsification covered 100,000 random scalar-policy points, 2,250
  monotonicity curves for $P$, and 4,320 searches over $J$; no failed
  inequality or hidden policy branch was found.
- A 54-profile thickness scan over $\beta\ge1/2$ found one numerical peak and
  no down--up reversal in every profile; this is evidence for, not a proof of,
  the remaining thickness conjecture.
- Numerical survival is recorded only as an audit. It is never the reason a
  claim is marked PROVED.

## Scope rule

The paper's conservative minimum is only over anonymous symmetric pure-cutoff
WPBE. “Unique equilibrium” in the paper always means unique numeric cutoff
inside that class. No statement above silently changes the rider-to-driver
transfer or the platform's completion objective.

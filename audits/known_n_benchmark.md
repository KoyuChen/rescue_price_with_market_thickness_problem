# Public-supply benchmark: what latent supply does and does not drive

This benchmark keeps the rider and driver primitives but replaces the latent
Poisson pool by a publicly known deterministic incumbent count $n\ge1$.
There is no fresh entry.  The announced menu is fixed before actions, and the
realized count is observed by the rider and all drivers.  The purpose is not
to give the platform a state-contingent price; it is to isolate the strategic
effect of rival-count uncertainty.

For a conjectured cutoff $a$, a focal acceptor faces
$X\sim\operatorname{Bin}(n-1,a)$ accepting rivals, so her assignment share is

\[
 s_n(a):=\mathbb E\!\left[\frac1{1+X}\right]
 =\frac{1-(1-a)^n}{na},
 \qquad s_n(0)=1.
\]

If she waits, all $n-1$ rivals reject with probability $(1-a)^{n-1}$.
Conditional on universal rejection, every rival cost is independently
uniform on $(a,1)$.  If terminal payment $p_j$ is selected, a rival is a
surviving eligible competitor with probability

\[
 \theta_j(a)=\frac{\alpha(p_j-a)}{1-a},
\]

and the focal driver's terminal assignment share is
$s_n(\theta_j(a))$.  The rider's terminal coverage is

\[
 C_{j,n}(a)=1-[1-\theta_j(a)]^n
 =n\theta_j(a)s_n(\theta_j(a)).
\]

These formulas give the same distinction as in the Poisson model: assignment
conditional on accepting now is $s_n(a)$, whereas reaching the wait payoff
requires the different event $(1-a)^{n-1}$.

## Completion identity

Let $\eta_j(a)$ denote the posting-conditional probability that the rider
selects terminal payment $p_j$ after failure.  At a positive interior cutoff,
driver indifference is

\[
 s_n(a)(p_1-a)
 =(1-a)^{n-1}\alpha
 \sum_j\eta_j(a)s_n(\theta_j(a))(p_j-a).
 \tag{N1}
\]

Conditional on posting, completion is

\[
 1-(1-a)^n+(1-a)^n\sum_j\eta_j(a)C_{j,n}(a).
\]

Using $C_{j,n}=n\alpha(p_j-a)s_n(\theta_j)/(1-a)$ and (N1), this simplifies
exactly to

\[
 \frac{p_1}{a}[1-(1-a)^n]=n p_1s_n(a).
\]

Thus unconditional completion at any positive interior cutoff is

\[
 \boxed{M_n(p_1,p_2;a)=(1-p_1)n p_1s_n(a).}
 \tag{N2}
\]

The identity is the finite-population counterpart of
$(1-p_1)mp_1\phi(ma)$.

## Local escalation and the source of the gain

Fix a flat payment $p\in(0,\beta)$ and consider $(p,p+\varepsilon)$.  The
nearby cutoff has the form
$a_\varepsilon=p-\kappa_n\varepsilon+o(\varepsilon)$, where

\[
 \kappa_n=
 \frac{(1-p)^{n-1}\alpha\rho}
 {s_n(p)-(1-p)^{n-1}\alpha\rho}>0,
 \qquad
 \rho=\frac{1-p/\beta}{1-p}.
 \tag{N3}
\]

The denominator is positive because
$s_n(p)\ge(1-p)^{n-1}$ and $\alpha\rho<1$.  Differentiating (N2) gives

\[
 \left.\frac{dM_n}{d\varepsilon}\right|_{0+}
 =-(1-p)n p\,s_n'(p)\kappa_n.
 \tag{N4}
\]

For $n\ge2$,

\[
 s_n(a)=\frac1n\sum_{r=0}^{n-1}(1-a)^r
\]

is strictly decreasing, so (N4) is strictly positive.  For $n=1$,
$s_1\equiv1$ and the derivative is exactly zero; indeed (N2) is independent
of the cutoff.

Hence the first-order announced-rescue gain does **not** require latent
realized supply.  It already appears with a publicly known pool whenever at
least two incumbents compete simultaneously.  Latent Poisson supply changes
the posterior and policy problem, and makes the rivalry wedge
$\phi(ma)-e^{-ma}$ smooth for every $m>0$, but the primitive source of the
local coverage gain is assignment competition.  This benchmark therefore
supports a narrower contribution claim: latent supply is part of the joint
information-and-design environment, not the sole mechanism behind strict
escalation.

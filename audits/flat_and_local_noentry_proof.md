# Flat benchmark and local no-entry escalation

This note supplies a self-contained proof for the optimized flat benchmark
and for the one-sided local escalation comparison in the no-entry baseline.
Throughout, $m>0$, $\gamma=0$, $\alpha\in(0,1]$, and $\beta\in(0,1)$.

## 1. Flat benchmark

Under $(p,p)$, an incumbent who rejects in period 1 never accepts the same
payment after failure.  The unique numeric symmetric cutoff is therefore
$a=p$ (with the zero-cost action tie understood at $p=0$), and completion is

\[
 F_m(p)=(1-p)(1-e^{-mp}).
\]

For $p\in[0,1]$,

\[
 F_m'(p)=-(1-e^{-mp})+m(1-p)e^{-mp},
\]

and

\[
 F_m''(p)=-2me^{-mp}-m^2(1-p)e^{-mp}<0.
\]

Because $F_m'(0)=m>0$ and $F_m'(1)=-(1-e^{-m})<0$, there is a unique
optimizer $p_F(m)\in(0,1)$.  Its first-order condition is

\[
 e^{mp_F}=1+m(1-p_F),
\]

equivalently

\[
 p_F(m)=\frac{1+m-W_0(e^{1+m})}{m}.
\]

Finally,

\[
 e^{m/2}F_m'(1/2)=1+\frac m2-e^{m/2}<0,
\]

so strict concavity implies

\[
 \boxed{p_F(m)<\tfrac12\quad\text{for every finite }m>0.}
\]

## 2. Localization of the strict-menu cutoff

Fix $p\in(0,\beta)$ and consider $(p,p+\varepsilon)$ with
$0<\varepsilon<\beta-p$.  The strict-menu one-crossing theorem gives one
symmetric cutoff $a_\varepsilon\in[0,p)$.  Its active-rescue equation is

\[
 h_m(a_\varepsilon)(p-a_\varepsilon)
 =r_\varepsilon
 \left[1-e^{-m\alpha(p+\varepsilon-a_\varepsilon)}\right],
 \tag{L1}
\]

where

\[
 h_m(a)=\frac{e^{ma}-1}{a},\quad h_m(0)=m,
 \qquad
 r_\varepsilon=\frac{1-(p+\varepsilon)/\beta}{1-p}.
\]

We first prove $a_\varepsilon\to p$.  Along any convergent subsequence,
(L1) has the limiting equation

\[
 h_m(a)(p-a)
 =\rho\left[1-e^{-m\alpha(p-a)}\right],
 \qquad
 \rho=\frac{1-p/\beta}{1-p}.
\]

For every $a<p$, immediate assignment strictly dominates waiting for a
repeat at the same payment.  Equivalently, the left side of this display is
strictly larger than the right side.  Thus its only solution in $[0,p]$ is
$a=p$, proving localization.

Put $\delta_\varepsilon=p-a_\varepsilon$.  Localization and the strict
assignment-versus-waiting inequality allow a neighborhood of $p$ and a
constant $c>0$ such that
\[
 h_m(a_\varepsilon)-r_\varepsilon m\alpha\ge c.
\]
Using $1-e^{-x}\le x$ in (L1) then gives
\[
 c\,\delta_\varepsilon
 \le r_\varepsilon m\alpha\varepsilon,
\]
so $\delta_\varepsilon=O(\varepsilon)$ uniformly.  Dividing (L1) by
$\varepsilon$ and taking limits then gives

\[
 h_m(p)\kappa=\rho m\alpha(1+\kappa),
 \qquad
 \kappa:=\lim_{\varepsilon\downarrow0}
 \frac{\delta_\varepsilon}{\varepsilon}.
\]

The denominator below is strictly positive by the same
assignment-versus-waiting inequality, so the limit is unique and hence holds
for the full sequence:

\[
 \boxed{
 \kappa=
 \frac{e^{-mp}\alpha\rho}
 {\phi(mp)-e^{-mp}\alpha\rho}>0.}
 \tag{L2}
\]

The rescue threshold converges to $p/\beta<1$, so rescue is indeed activated
by a positive mass for all sufficiently small $\varepsilon$.  Thus no rider
threshold kink is crossed in this one-sided neighborhood.

## 3. Exact local completion gain

At the unique positive cutoff, the no-entry indifference identity gives

\[
 M_m^{\alpha,0}(p,p+\varepsilon;a_\varepsilon)
 =(1-p)mp\phi(ma_\varepsilon).
\]

Since $a_\varepsilon=p-\kappa\varepsilon+o(\varepsilon)$, differentiating
from the right and using

\[
 -x\phi'(x)=\phi(x)-e^{-x}
\]

yields

\[
 \boxed{
 \left.\frac{dM}{d\varepsilon}\right|_{0+}
 =
 \frac{
 m(1-p)e^{-mp}\alpha\rho
 [\phi(mp)-e^{-mp}]
 }{
 \phi(mp)-e^{-mp}\alpha\rho
 }>0.}
 \tag{L3}
\]

The strict sign uses $p>0$, $\alpha>0$, $\rho>0$, and
$\phi(mp)>e^{-mp}$.  It has a direct mechanism interpretation: the numerator
contains the surviving marginal-rescue mass, while
$\phi(mp)-e^{-mp}$ is the wedge between a driver's assignment chance after
accepting now and the event that all rivals wait.

## 4. Optimized-flat dominance

If $\beta\ge1/2$, Section 1 gives $p_F(m)<1/2\le\beta$.  Applying (L3) at
$p=p_F(m)$ shows that some sufficiently small strict escalation
$(p_F,p_F+\varepsilon)$ has completion strictly above $F_m(p_F)$.  The
strict-menu cutoff is unique, so this comparison is already conservative
over the anonymous symmetric pure-cutoff class.  Consequently,

\[
 \boxed{
 D_{\alpha,0}^*(m)>F_0^*(m)
 \quad\text{for every }m>0,\ \alpha>0,\ \beta\ge\tfrac12.}
\]

Thus the earlier sufficient condition $\beta>1/2$ extends to the equality
boundary.  This statement does not claim that $1/2$ is the sharp patience
threshold; the global cutoff parameterization determines the full region.

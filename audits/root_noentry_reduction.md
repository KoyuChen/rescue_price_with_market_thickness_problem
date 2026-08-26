# Root derivation: exact no-entry reduction

This note is an independent derivation. Statements through Proposition 4 are
proved algebraically below; the fixed-$p_1$ global step is isolated as a
remaining lemma rather than assumed.

Fix $\gamma=0$, $m>0$, $\alpha\in(0,1]$, and $\beta\in(0,1)$, and write
\[
C_j(a)=1-e^{-m\alpha(p_j-a)},\qquad
\rho=\frac{1-p_1/\beta}{1-p_1}
\]
when $p_1<\beta$.

## 1. Economically relevant price region

If $p_1\ge\beta$, no rider has positive continuation surplus at either
payment, so the unique symmetric cutoff is $a=p_1$ and the menu is equivalent
to the flat first-period payment.

If $p_1<\beta\le p_2$, rescue is not used by a positive mass of riders.
Repeat at $p_1$ alone cannot support an interior cutoff because, for
$0<a<p_1$,
\[
\phi(ma)
>
e^{-ma}
\ge
e^{-ma}\alpha\rho\phi(m\alpha(p_1-a)).
\]
At $a=0<p_1$, the first comparison is an equality, but the overall
comparison remains strict because
$\rho=(1-p_1/\beta)/(1-p_1)<1$.  When $p_1=0$, there is no candidate
$a<p_1$.
Thus the unique cutoff is again $a=p_1$ and the menu is outcome-equivalent to
the flat policy $(p_1,p_1)$.

Hence every nontrivial no-entry escalation can be sought in
\[
0\le p_1<p_2<\beta.
\]

## 2. Active-rescue simplification

Let $0\le a<p_1$ and suppose rescue is used by a positive mass of riders.
With
\[
v^M(a)
=
\frac{C_2(a)p_2-C_1(a)p_1}
{\beta[C_2(a)-C_1(a)]},
\]
the conditional period-2 coverage chosen by a posting rider is
\[
\begin{aligned}
S(a)
&:=\eta^R(a)C_1(a)+\eta(a)C_2(a)\\
&=
\frac{
C_1(a)(v^M(a)-p_1/\beta)
+C_2(a)(1-v^M(a))
}{1-p_1}\\
&=
\frac{1-p_2/\beta}{1-p_1}C_2(a).
\end{aligned}
\]
The repeat coverage cancels after substituting the indifference type.

Conversely, if rescue is inactive at $a<p_1$, cutoff indifference is
impossible by the strict assignment-versus-waiting inequality above.
For $p_1>0$, the upper-boundary strategy at $a=p_1$ is not an equilibrium:
strict escalation with $p_2<\beta$ makes rescue active and gives
$f(p_1)<0$.  When $p_1=0$, the same numeric cutoff instead denotes the
lower-boundary reject-all strategy; that case is retained below. Therefore
every equilibrium under $0\le p_1<p_2<\beta$ uses active rescue; it is either
the lower-boundary cutoff $a=0$ or an interior positive root.

## 3. Scalar global equilibrium equation

For a positive cutoff, the focal cutoff driver's indifference condition is
\[
\phi(ma)(p_1-a)
=
\frac{e^{-ma}}{m}S(a).
\]
Define, continuously at $a=0$,
\[
G(a;p_1,p_2)
:=
\frac{(e^{ma}-1)(p_1-a)}{a}
-
\frac{1-p_2/\beta}{1-p_1}
\left[1-e^{-m\alpha(p_2-a)}\right],
\]
where the first term at zero is $mp_1$. Then
\[
\mathcal E_m^{\alpha,0}(p_1,p_2)
=
\{0:G(0)\le0\}
\cup
\{a\in(0,p_1):G(a)=0\}.
\]
Moreover,
\[
G(p_1)
=
-
\frac{1-p_2/\beta}{1-p_1}
\left[1-e^{-m\alpha(p_2-p_1)}\right]
<0,
\]
so this set is nonempty and compact.

The set identity requires one additional no-spurious-root check.  Put
\[
L(a)=\frac{(e^{ma}-1)(p_1-a)}a,
\qquad
k_j=\frac{1-p_j/\beta}{1-p_1},
\]
with $L(0)=mp_1$.  Rescue is inactive exactly when
$k_2C_2(a)\le k_1C_1(a)$.  The strict assignment-versus-repeat comparison
gives $L(a)>k_1C_1(a)$ for every $a<p_1$ (including $a=0$ by the separate
argument above).  Hence inactivity implies
\[
G(a)=L(a)-k_2C_2(a)>0.
\]
Every zero of $G$, and every lower-boundary condition $G(0)\le0$, therefore
lies in the active-rescue regime and is a genuine equilibrium condition.

## 4. Exact completion identity and worst root

At a positive equilibrium, cutoff indifference gives
\[
e^{-ma}S(a)=m\phi(ma)(p_1-a).
\]
Substituting this into conditional completion,
\[
1-e^{-ma}+e^{-ma}S(a),
\]
and using $1-e^{-ma}=ma\phi(ma)$ yields
\[
\boxed{
M_m^{\alpha,0}(p_1,p_2;a)
=(1-p_1)m p_1\phi(ma)
}
\qquad(a>0).
\]
Because $\phi$ is strictly decreasing on $(0,\infty)$, completion is strictly
decreasing in the positive equilibrium cutoff.

At a reject-all equilibrium,
\[
M_m^{\alpha,0}(p_1,p_2;0)
=
\left(1-\frac{p_2}{\beta}\right)
\left(1-e^{-m\alpha p_2}\right).
\]
The condition $G(0)\le0$ implies
\[
M_m^{\alpha,0}(p_1,p_2;0)
\ge m p_1(1-p_1),
\]
whereas every positive equilibrium has value
\[
(1-p_1)m p_1\phi(ma)<m p_1(1-p_1).
\]
Consequently:

- if positive equilibrium roots exist, the pessimistic outcome is generated
  by the largest positive root;
- if no positive root exists, $a=0$ is the only equilibrium and the displayed
  completion expression after active-rescue cancellation is the
  conservative value.  Repeat may still be used by a positive mass when
  $p_1>0$; it cancels only in the aggregate formula.

This is an exact reduction of equilibrium selection to the largest positive
zero of $G$.

## 5. Fixed-cutoff rescue-price envelope

For fixed $a<p_1$, the right side of the positive-root equation is proportional
to
\[
q(p_2;a)
:=(\beta-p_2)
\left[1-e^{-m\alpha(p_2-a)}\right].
\]
On $p_2\in(p_1,\beta)$,
\[
\frac{\partial^2q}{\partial p_2^2}<0.
\]
Its unique unconstrained maximizer solves
\[
e^{m\alpha(p_2-a)}
=1+m\alpha(\beta-p_2).
\]
Writing $k=m\alpha$, it is
\[
p_2^\dagger(a)
=
\beta-
\frac{
W_0\!\left(e^{1+k(\beta-a)}\right)-1
}{k}.
\]
Let $y(a)=\beta-p_2^\dagger(a)$. At the envelope,
\[
\max_{p_2}
\frac{1-p_2/\beta}{1-p_1}
\left[1-e^{-k(p_2-a)}\right]
=
\frac{k\,y(a)^2}
{\beta(1-p_1)[1+k y(a)]}.
\]

Equating this envelope to the left side of $G=0$ yields
\[
(1-p_1)(p_1-a)=B_m(a),
\]
where
\[
B_m(a)
=
\frac{a}{e^{ma}-1}
\frac{k\,y(a)^2}{\beta[1+k y(a)]}.
\]
Thus candidate conditional optima obey
\[
p_1^\pm(a)
=
\frac{
1+a\pm\sqrt{(1-a)^2-4B_m(a)}
}{2}.
\]
Numerical solutions use the lower branch, but this is not yet a theorem.

## 6. Exact remaining global lemma

To turn the envelope into a fixed-$p_1$ theorem, it remains to prove:

> If $a_*(p_1)$ is the smallest cutoff for which the root equation is feasible
> over $p_2\in[p_1,\beta)$, then the tangent menu
> $p_2=p_2^\dagger(a_*)$ has no equilibrium root larger than $a_*$.

Equivalently, the tangent menu must be shown to make $a_*$ the largest, not
merely one, positive root of $G$. Broad numerical tests support this
one-crossing property, but they are not a proof.

Once this lemma is established, fixed-$p_1$ optimization reduces exactly to
minimizing the largest implementable cutoff, and the outer menu problem becomes
a one-dimensional maximization over $a$ using the lower quadratic branch.

## 7. Immediate local corollary

For $(p,p+\varepsilon)$, write
\[
a_\varepsilon=p-\kappa\varepsilon+o(\varepsilon).
\]
Expanding $G=0$ gives
\[
\kappa
=
\frac{e^{-mp}\alpha\rho}
{\phi(mp)-e^{-mp}\alpha\rho}.
\]
Differentiating the exact equilibrium-completion identity and using
\[
-x\phi'(x)=\phi(x)-e^{-x}
\]
gives
\[
\left.\frac{dM}{d\varepsilon}\right|_{0+}
=
\frac{
m(1-p)e^{-mp}\alpha\rho
[\phi(mp)-e^{-mp}]
}{
\phi(mp)-e^{-mp}\alpha\rho
}>0.
\]
This provides a shorter no-entry proof of the local theorem, conditional on
the localization result.

Because the unique flat optimizer satisfies $p_F(m)<1/2$ strictly, the same
argument appears to cover $\beta=1/2$ as well as $\beta>1/2$. The equality
boundary must be independently audited before strengthening the corollary.

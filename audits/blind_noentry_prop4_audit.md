# Independent audit of the no-entry reduction through Proposition 4

Scope: `gamma=0`, `m>0`, `alpha>0`, through the active-rescue reduction,
scalar `G` equation, equilibrium set, completion identity, and largest-root
selection in `root_noentry_reduction.md`.  This audit starts from the primitive
driver payoffs in `blind_wpbe_reconstruction.md`.

## Verdict

The main algebra and the largest-root conclusion are correct.  One logical
bridge needed for the claimed exact `G`-root characterization is omitted, one
displayed strict inequality is false at `a=0`, and the treatment of `p_1=0`
again conflates lower- and upper-boundary cutoff actions.  All three are
repairable without changing the substantive reduction.  The phrase
"rescue-only completion" at `a=0` is also economically inaccurate: repeat
completions generally occur even though their weighted contribution cancels
from the simplified formula.

## 1. Direct checksum of the active-rescue algebra

Put

\[
 C_j(a)=1-e^{-m\alpha(p_j-a)},\qquad
 k_j:=\frac{1-p_j/\beta}{1-p_1}.
\]

When rescue has positive rider mass, the repeat/rescue switch is

\[
 v^M=\frac{C_2p_2-C_1p_1}{\beta(C_2-C_1)}<1.
\]

The posting-conditional continuation coverage is

\[
 \begin{aligned}
 S
 &=\frac{C_1(v^M-p_1/\beta)+C_2(1-v^M)}{1-p_1}\\
 &=\frac{C_2-(C_2-C_1)v^M-C_1p_1/\beta}{1-p_1}\\
 &=\frac{C_2-C_2p_2/\beta}{1-p_1}
 =k_2C_2.
 \end{aligned}
\]

So the cancellation displayed in the root note is exact.  It is an
**aggregate algebraic cancellation**; it does not mean repeat is unused or
that repeat produces no completions.

The condition for strictly active rescue can be written in a form useful for
the root audit:

\[
 v^M<1
 \quad\Longleftrightarrow\quad
 C_2(\beta-p_2)>C_1(\beta-p_1)
 \quad\Longleftrightarrow\quad
 k_2C_2>k_1C_1.
\]

At equality the switch is `v^M=1`, so rescue has zero mass.

## 2. Direct checksum of the cutoff equation

For a cutoff driver of cost `c=a`, no entry implies
`lambda_j=m alpha(p_j-a)`.  Therefore

\[
 \alpha\phi(\lambda_j)(p_j-a)
 =\frac{1-e^{-\lambda_j}}m=\frac{C_j}{m}.
\]

Her indifference condition is exactly

\[
 \phi(ma)(p_1-a)=\frac{e^{-ma}}m S(a).
\]

For `a>0`, multiplying by `m e^{ma}` and using
`m e^{ma}\phi(ma)=(e^{ma}-1)/a` gives

\[
 \frac{(e^{ma}-1)(p_1-a)}a=S(a).
\]

Under active rescue, `S=k_2C_2`, so the displayed equation `G=0` is correct,
and its continuous first term at zero is `mp_1`.

## 3. Missing bridge: why the simplified G has no inactive-rescue roots

The note correctly observes that an *actual* cutoff indifference cannot occur
when rescue is inactive, but that sentence alone does not prove that the
newly defined, active-formula function `G` has no spurious zero at such an
`a`.  This is needed before one can identify the equilibrium set with all
zeros of `G`.

The missing argument is short.  Define

\[
 L(a):=\frac{(e^{ma}-1)(p_1-a)}a,
 \]

with `L(0)=mp_1`.  If rescue is inactive, actual continuation coverage is
`k_1C_1`, and the condition in Section 1 gives `k_2C_2<=k_1C_1`.  For every
`a<p_1`, immediate assignment strictly dominates waiting for repeat alone:

\[
 \phi(ma)>
 \alpha e^{-ma}\rho\phi(m\alpha(p_1-a)).
\]

After multiplying by `m e^{ma}(p_1-a)`, this is

\[
 L(a)>k_1C_1\ge k_2C_2.
\]

Consequently `G(a)=L(a)-k_2C_2>0` whenever rescue is inactive.  In particular:

- any positive zero of `G` necessarily has active rescue and is a genuine
  cutoff indifference;
- `G(0)<=0` necessarily has active rescue and is equivalent to the lower
  boundary margin being nonpositive.

Adding this lemma makes the claimed equilibrium-set identity exact.  Without
it, the displayed set equality is not proved, even though it is true.

## 4. The strict inequality at a=0

The root note writes

\[
 \phi(ma)>e^{-ma}\ge
 e^{-ma}\alpha\rho\phi(m\alpha(p_1-a))
\]

for every `a<p_1`.  The first strict inequality is false at `a=0`, where both
sides equal one.  The desired overall strict inequality is still true when
`p_1>0`: because `beta<1`,

\[
 \rho=\frac{1-p_1/\beta}{1-p_1}<1,
\]

so the second comparison is strict at `a=0`.  A correct proof splits the
cases `a>0` and `a=0`, or writes weak inequalities and separately notes that
at least one is strict.  When `p_1=0`, there is no `a<p_1` to consider.

## 5. Boundary p_1=0

The price region in the note includes `p_1=0`.  It then says that at
`a=p_1`, strict escalation gives `f(p_1)<0`, "so `a=p_1` is not an
equilibrium."  This is valid only for the **upper-boundary strategy** that has
the cutoff type accept, and should be restricted to `p_1>0`.  At `p_1=0`, the
same numeric cutoff is also the **lower-boundary reject-all strategy**.  Since
`f(0)<0` under active rescue, reject-all is precisely the equilibrium.

Thus either restrict the nontrivial positive-root analysis to
`0<p_1<p_2<beta` and treat `p_1=0` separately, or explicitly carry the
cutoff-type action along with the scalar cutoff.  The later `G`-set formula
does include the valid lower-boundary equilibrium, but the preceding sentence
is otherwise contradictory at `p_1=0`.

## 6. Completion identity

At a positive equilibrium,

\[
 e^{-ma}S=m\phi(ma)(p_1-a).
\]

Hence conditional completion is

\[
 1-e^{-ma}+e^{-ma}S
 =ma\phi(ma)+m\phi(ma)(p_1-a)
 =mp_1\phi(ma),
\]

and unconditional completion is exactly

\[
 M=(1-p_1)mp_1\phi(ma).
\]

There is no missing factor of `alpha`, `m`, or `1-p_1`.  Since `phi(ma)` is
strictly decreasing in positive `a`, completion is strictly decreasing across
positive equilibrium roots.

At the reject-all equilibrium, active-rescue cancellation gives

\[
 M(0)=(1-p_2/\beta)(1-e^{-m\alpha p_2}).
\]

This formula is correct.  It should not be called "rescue-only completion" in
an operational sense when `p_1>0`: a positive interval of rider types repeats,
and repeat can complete because incumbents with costs in `(0,p_1]` exist.  The
repeat term has merely canceled from the aggregate expression through rider
indifference.

## 7. Largest-root selection

At zero,

\[
 G(0)\le0
 \quad\Longleftrightarrow\quad
 mp_1\le\frac{1-p_2/\beta}{1-p_1}
 (1-e^{-m\alpha p_2}),
\]

which after multiplying by `1-p_1` is exactly

\[
 M(0)\ge mp_1(1-p_1).
\]

For every positive equilibrium,

\[
 M(a)=(1-p_1)mp_1\phi(ma)<mp_1(1-p_1).
\]

Therefore, if zero and positive equilibria coexist, zero can never be the
pessimistic selection.  Among positive roots, strict decrease of `phi(ma)`
makes the largest root uniquely worst in completion value.  A largest positive
root exists: `G(p_1)<0` rules out roots near `p_1`, and continuity includes any
root limit at zero in the lower-boundary set.  If no positive root exists,
continuity plus `G(p_1)<0` forces `G(0)<=0`, so reject-all is the only
equilibrium.  The largest-root conclusion is therefore correct.

## Required repairs through Proposition 4

1. Replace the false strict chain at `a=0` with the split strictness argument.
2. Insert the `L>k_1C_1>=k_2C_2` lemma before claiming that *all* zeros of the
   active-formula `G` are exactly equilibria.
3. Separate `p_1=0` lower-boundary rejection from the `a=p_1` accept-boundary
   statement.
4. Replace "rescue-only completion" with "the completion expression after
   active-rescue cancellation" (unless `p_1=0`).

With those repairs, no algebraic or equilibrium-selection error remains in
the reduction through Proposition 4.

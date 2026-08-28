# Committed-reach numerical slice

This is the numerical input to the five-page group-meeting note. It uses the
main search-resource specification

\[
Q^{\mathrm{com}}=(1-p_1)e^{-ma}m(s-1),\qquad
J=M-\kappa Q^{\mathrm{com}}.
\]

The calibration is

\[
(\beta,\delta,\omega,\tau,\kappa,\bar s,B)
=(.8,.8,.8,.25,.0125,4,1),
\]

with uniform rider values and driver costs. The local per-window Poisson flow
is varied over

\[
m\in\{.5,.75,1,1.5,2,3,4,6,8,12,16\}.
\]

For every architecture and every (m), the solver fixes (p_1), optimizes the
permitted continuation controls, and then optimizes (p_1). Every objective
evaluation solves the unique incumbent cutoff-WPBE. Three independent
differential-evolution challengers search the joint policy domain; finalists
are checked again by dense sign-change enumeration and grid doubling.

## Main displayed results

| Quantity | Largest value on the tested (m)-grid | Location |
|---|---:|---:|
| Fresh-core value (V_A-V_I) | 0.135030 | (m=3) |
| Outer-search option value (V_E-V_A) | 0.107917 | (m=1) |

The optimized expanded-search multiplier is at the cap (s=4) for
(m\le1.5), declines to (s=1.3027) at (m=8), and equals (s=1) at the
tested (m=12,16) tail. The optimized rescue increment (p_2-p_1) remains
positive at those thick-market points.

These are displayed-grid numerical maxima, not claims of unique global peaks
in (m). The maintained theory guarantees endpoint collapse and existence of
an interior maximizer when a gap is positive, but not peak uniqueness or a
universal ordering.

## Audit status

- 33 architecture rows across 11 environments;
- all final cutoff sets stable under grid doubling;
- maximum certified cutoff count: one;
- minimum (E-A) value gap: zero;
- maximum (E-A) value gap: 0.107917;
- all 25 unit tests pass.

The wider (3\times3) ((\beta,\delta)) comparative-static grid is intentionally
deferred; this slice is designed to communicate the mechanism intuition
cleanly rather than stand in for a full market-conditions audit.

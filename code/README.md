# Numerical falsification engine

> **Incumbent-discount correction.** The current paper gives incumbents a
> separate period-2 discount factor $\delta$. Use `discount_model.py`,
> `run_discount_falsification.py`, and `test_discount_model.py` for the
> corrected model; see `DISCOUNT_README.md`. The original files remain as an
> exact $\delta=1$ regression benchmark.

This directory contains an independent implementation of the announced-
escalation model.  It does not import or modify the manuscript.

- `model.py`: stable binary64 and mpmath payoff/completion primitives.
- `equilibria.py`: fast all-branch bracketing plus high-precision,
  interval-style global root exclusion.  Same-sign boxes are retained as
  unresolved tangency candidates rather than discarded.
- `optimize.py`: deterministic nested optimization of `p2` conditional on
  `p1`, followed by `p1`, always using pessimistic completion over every
  enumerated cutoff.
- `noentry.py`: independent max-of-two-branches reduction for `gamma=0`.
- `geometry.py`: overflow-safe `P(a), Q(a), J(a)` parameterization and
  high-precision stationary-point certificates.
- `run_falsification.py`: reproducible scans summarized in the report.
- `test_engine.py`: regression suite.
- `exact_one_driver_regions.py`: solves the exact-one-driver WPBE envelope and
  reproduces the $(\beta,\delta)$ type-region figure in the group-meeting note.
- `thickness_regions.py`: re-solves the latent-thickness cutoff WPBE at
  $m=1,5,10,20$ and reproduces its rider and driver type-region widths.

From the repository root:

```bash
PYTHONPATH=code python -m unittest discover -s code -p 'test_*.py' -v

PYTHONPATH=code python code/run_falsification.py --quick

PYTHONPATH=code python code/run_falsification.py --full
```

The random generator seed is fixed at `20260825`. The audited NumPy, SciPy,
and mpmath versions are pinned in `requirements.txt`.
Numerical root boxes are candidate certificates, not directed-rounding formal
proofs.

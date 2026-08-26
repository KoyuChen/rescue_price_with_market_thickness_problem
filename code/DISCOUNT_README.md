# Incumbent-discount falsification engine

This extension studies the corrected timing in which an incumbent driver's
period-2 net payoff is `delta * (p-c)`, while a fresh entrant receives the
undiscounted terminal payoff `p-c`.  It does not modify the baseline engine.

Run the regression tests from the repository root:

```bash
PYTHONPATH=code python code/test_discount_model.py
```

Run a short smoke scan:

```bash
PYTHONPATH=code python code/run_discount_falsification.py --quick
```

Reproduce the full deterministic searches reported in
`../analysis/incumbent_discount_numerical_report.md`:

```bash
for section in formulas roots exact thickness; do
  PYTHONPATH=code python code/run_discount_falsification.py \
    --full --section "$section"
done
```

The runner prints JSON and uses seed `20260825`.  Binary64 scans enumerate
every visible cutoff root and label roots closer than one float ulp to the
upper boundary as `near-p-limit`.  Reported root candidates are rechecked by
the arbitrary-precision interval-style isolator.  Its enclosures are a
falsification safeguard, not a formal directed-rounding proof.

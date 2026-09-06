# m=3 rare-posterior repairs for menus 157--159

The active outer search completed these menus with failed numerical gates:

| Ordinal | Menu | Original unknown histories | Original training max regret |
|---:|---:|---:|---:|
| 157 | (0.20,0.25) | 4 | 0.001633404 |
| 158 | (0.20,0.30) | 3 | approximately 0 |
| 159 | (0.20,0.35) | 2 | approximately 0 |

Ordinals 158 and 159 are blocked by unobserved conditional histories.  Menu
157 also has a genuine training/support failure.  Its earlier zero-retention
cold start did not resolve the histories and is preserved as a failed attempt.

`run_m3_rare_posterior_repairs.py` independently recomputes bounded conditional
posteriors after every policy update.  Every case starts from the same common
full-support cold homotopy as the outer search; no failed profile is used as an
initial condition.  Prices, 2048x24 support, training and audit budgets, seeds,
quadrature and numerical tolerances are unchanged.  Inputs and source are
hashed, every iteration is checkpointed and an exclusive lock prevents a
duplicate supervisor.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -u \
  run_m3_rare_posterior_repairs.py \
  --source-run runs/m3_outer_search_20260906 \
  --output runs/m3_rare_posterior_repairs_20260906 --workers 3
```

The independent run began on 2026-09-06.  A running process or a low sampled
regret is not acceptance.  Each profile must finish training and pass both
million-draw audits with no unresolved histories under the original thresholds.
If any repair passes, it will receive fresh-seed frozen-profile audits before
being explicitly linked to outer-search aggregation.  Original failed cache
entries are never overwritten.

This repair does not optimize prices or produce V(3).  Menus 162 and 163 have
known-history cycling failures and are deliberately outside this posterior-only
repair batch.

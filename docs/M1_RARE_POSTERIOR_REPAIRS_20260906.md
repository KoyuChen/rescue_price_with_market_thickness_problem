# m=1 new unresolved menus and independent cold-start repairs

This work concerns three completed failures from the still-active outer search:

| Ordinal | Menu | Original unknown histories | Original audit issue |
|---:|---:|---:|---|
| 193 | (0.25,0.30) | 2 | 249 unresolved checks in each audit |
| 194 | (0.25,0.35) | 2 | 251 unresolved checks in each audit |
| 195 | (0.25,0.40) | 1 | 92 unresolved checks in each audit |

The more complete posterior evaluator was applied read-only to the frozen 194
and 195 profiles with the original 50,000 training counts. It removed the
unknown-history flag without changing either policy. Independent million-count
diagnostics then found zero unresolved checks, but the frozen strategies still
failed:

| Menu | Full-plan upper | Retention upper | Supported-action upper |
|---:|---:|---:|---:|
| (0.25,0.35) | 0.0000015040969 | 0.0040000000 | 0.0040000000 |
| (0.25,0.40) | 0.0000004543641 | 0.0017648442 | 0.0040000000 |

Thus these are not accepted by merely reclassifying or observing the histories.
The retained actions need to respond to the corrected beliefs. Menu 193 was not
given an acceptance diagnosis from the old frozen profile.

`run_m1_rare_posterior_repairs.py` performs independent common full-support
cold starts for ordinals 193--195. It uses the original menu-specific settings,
prices, 2048x24 support, training and audit seeds and unchanged tolerances. It
uses no failed profile as an initial condition. Inputs and source are hashed;
each iteration is checkpointed; an exclusive lock rejects duplicate runs; all
original result and profile files are copied into the independent output.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -u \
  run_m1_rare_posterior_repairs.py \
  --source-run runs/m1_outer_search_20260906 \
  --output runs/m1_rare_posterior_repairs_20260906 --workers 3
```

The three cold starts began on 2026-09-06. Initial posterior-aware evaluations
had no unknown histories. No repaired menu has completed training or audit yet;
the existence of a process or checkpoint is not an acceptance result. Original
outer-search caches remain unchanged. If a repair passes, aggregation must link
its separate evidence explicitly rather than silently relabeling the old cache.

Two runner tests and the prior frozen-audit tests pass. The complete suite passed
**117 tests** after adding this runner. This work does not optimize prices,
compare completion rates, or certify continuous-type WPBE. A completed repair
result will receive its own archive and status update.

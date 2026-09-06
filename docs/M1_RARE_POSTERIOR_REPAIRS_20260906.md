# m=1 new unresolved menus and independent cold-start repairs

## Completed repair and held-out audit

All three common-full-support cold starts completed and passed the unchanged
finite-support numerical gates.  The profiles were then frozen and audited
again with two new, independent one-million-draw count samples per menu.  The
fresh seeds were disjoint from training and from the two original audit seeds.

| Ordinal | Menu | Training max regret | Fresh audit max regret uppers | Fresh unresolved checks |
|---:|---:|---:|---:|---:|
| 193 | (0.25,0.30) | 0.0000048231 | 0.0002850255 / 0.0003368441 | 0 / 0 |
| 194 | (0.25,0.35) | 0.0000001335 | 0.0000015385 / 0.0000015385 | 0 / 0 |
| 195 | (0.25,0.40) | 0.0000001332 | 0.0000004996 / 0.0000004996 | 0 / 0 |

Every upper bound is below the original regret tolerance of `0.00075`; all
support checks also pass.  `audit_m1_rare_posterior_repairs.py` verifies the
profile, support and source hashes and checks that audit evaluation does not
change the frozen profile.  Complete original failures, cold-start checkpoints,
repaired profiles, original audits and fresh audits are preserved in
`results/m1_rare_posterior_repairs_20260906`.

These results repair three individual coarse-grid candidates.  They do not
replace their failed records in the still-active outer-search cache, optimize
prices, compare completion rates, establish continuous-type convergence or
certify WPBE.  Any outer-search aggregation must link this evidence explicitly.

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

The repair runner is resumable, but this run is now finished.  To reproduce the
held-out audits after reproducing the repairs:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -u \
  audit_m1_rare_posterior_repairs.py \
  --root runs/m1_rare_posterior_repairs_20260906
```

The complete suite passed **119 tests** after adding the fresh-audit provenance
tests.  This work does not optimize prices, compare completion rates, or certify
continuous-type WPBE.

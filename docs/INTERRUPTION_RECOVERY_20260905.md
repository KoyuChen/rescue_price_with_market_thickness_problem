# Interrupted thick-market computation and checkpoint recovery

Observation time: 2026-09-05 19:40 UTC (2026-09-06 03:40 Hong Kong).

The original supervisor PID 278488 and workers 278529, 278532, 278533,
278534 disappeared. A scan of accessible process command lines found no
replacement `run_thick_markets.py` workers. No completed menu result or
policy checkpoint exists in `runs/thick_high_precision_20260905`.
The available records do not establish why the processes terminated;
this is **not** evidence of an equilibrium-audit failure.

The last recorded iterations for m=6,12,24,48 are 201,136,116,71,
respectively. Every job was still solving its first validation menu.
All original source hashes and the random-OD support checksum match the
run request. The original source commit is
`1c4b62eacada84ff69d8ad74824eef447c70f04b`.
Copies of all four logs are retained in
`results/interruption_20260905/`; the original files are not overwritten.

## Implementation repair (not an economic-model change)

`checkpoint_solver.py` implements the same cold start, homotopy schedule,
polishing, updates, random seeds, audit budgets and acceptance thresholds
as `research_solver/high_precision.py`. It atomically saves the policy,
next iteration, stage history and completed audit replicates after each
update/stage/audit. Source, settings, model, type support and quadrature
are bound to the checkpoint with a SHA-256 fingerprint. A mismatched
checkpoint is rejected. Policy and cursor are stored in the same NPZ;
both the file and parent directory are fsynced before proceeding.

`run_checkpointed_markets.py` adds an exclusive supervisor lock, reuse of
completed menus and audits, and resumable per-menu calculations. Unresolved
candidates remain in the records and refinement competition. Failed
validation gates still block that thickness. It retains the original
global and local price grids, selection samples and independent final
paired evaluation. The 4096-cost, 96-route, route-seed and 0.00125-price
confirmation requirements remain pending, not implicitly satisfied.

The original in-memory policies were lost. Consequently the first run of
the new version is explicitly a **cold restart**, not a continuation from
iteration 201/136/116/71. Subsequent executions of this identical command
resume saved policies and reject duplicate active supervisors:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_checkpointed_markets.py \
  --source-run runs/thick_high_precision_20260905 \
  --output runs/thick_checkpointed_20260905 --workers 4
```

## Verification and remaining limitations

Regression tests compare the new solver with the unmodified original
after simulated interruptions at an iteration, a stage boundary, and an
audit boundary. Policy arrays are exactly equal, and complete cleaned
result dictionaries agree. Changed source fingerprints are rejected.
Runner tests preserve failed candidates, reuse completed menus and reject
tampered menu identities. These small-support tests verify recovery
semantics, **not** high-precision equilibrium convergence.

The runner regression also exposed a duplicate `m` keyword in the original
failed-gate logging path (`dict(m=m, **summary)`). The independent runner
uses an explicit override so a failed gate can return its diagnostic
summary normally. The original running-version files remain unchanged.

The m=3 old 2048-by-24 rescue remains unresolved: both audits have 294
unresolved cost/history entries, all at q=.535 and route index 0. Their
conditional event sample means are zero. Full-plan regret upper bounds
are about .00047545 and .00047666, but the universal retention bound is
.08655352 and the retention support-gap bound .14425586. A zero sample
frequency is not a proof that the event is impossible. No posterior,
candidate, or acceptance threshold has been altered to hide this issue.

The m=1 fixed-menu report remains a fixed-menu result. Neither optimized
V(1) nor the requested six-thickness price/peak comparison is complete.

The complete suite passed: 72 tests, 2026-09-05. The independent four-worker
recovery run was then started at `runs/thick_checkpointed_20260905`.
This is a runtime recovery, not a new equilibrium or optimal-price result.

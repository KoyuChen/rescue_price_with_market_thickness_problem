# Frozen-profile expanded audit: m=3, menu 164

This is a numerical audit follow-up, not a price-search result, a change to the
equilibrium selection rule, or a continuous-type WPBE certificate.

## Why this menu

The original common-cold-start search produced `(p1,p2)=(0.20,0.60)` on the
2048-cost by 24-route support. Its final training maximum regret was
`8.5615873727e-7`, with no unresolved training histories. The two original
million-count audits had no unresolved histories and full-plan regret upper
bounds `0.0006909224400` and `0.0007920195848`. The second exceeded the unchanged
`0.00075` tolerance. Conditional retention upper bounds were below `4.61e-7`.

This is distinct from m=3 menu 163 `(0.20,0.55)`: that profile had actual
training retention regret `0.0012275670` and independent retention upper bounds
about `0.001233`, with zero unresolved histories. More reporting samples do
not fix its unprofitable retained strategy. Menu 163 remains unresolved.

## Prespecified follow-up

`audit_frozen_search_menu.py` takes an immutable completed search profile. It
does not solve, warm-start, change prices, replace original caches, or choose
new strategies after observing audit outcomes.

- Exactly two independent IID count samples, each of size 5,000,000.
- Seeds: `202609064236813`, `202609064236814`.
- Per-replicate error allocation: `1.8608114534864606e-9`.
- The new audit family alone has budget `0.001`, allocated across the six
  thicknesses, all nonnegative menu ordinals using inverse-square spending,
  and two replicates. No combined confidence claim is made for the original
  adaptive search or other historical audit families.
- Original profile, support, request and result are copied with SHA-256
  verification. The plan is saved before drawing samples. In-memory strategy
  arrays are also compared exactly after each audit.
- No automatic increase in sample size or replacement of an unsuccessful seed.

The separate request, snapshots, full audit records and summary are in
`results/m3_menu164_expanded_audit_20260906/`. The original failed result stays
in `runs/m3_outer_search_20260906/m3/menu_00164/` unchanged. Future search
aggregation must explicitly link follow-up evidence; it must not silently
reinterpret the old failed cache as a pass.

## Reproduction

From the published checkout, reconstruct only the required source layout in
a new temporary directory. No complete historical search is needed:

```bash
ARCHIVE=results/m3_menu164_expanded_audit_20260906
SOURCE=$(mktemp -d)
OUTPUT=$(mktemp -d)
mkdir -p "$SOURCE/m3/menu_00164"
cp "$ARCHIVE/original_request.json" "$SOURCE/request.json"
cp "$ARCHIVE/support.npz" "$SOURCE/support.npz"
cp "$ARCHIVE/original_result.json" "$SOURCE/m3/menu_00164/result.json"
cp "$ARCHIVE/profile.npz" "$SOURCE/m3/menu_00164/profile.npz"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python audit_frozen_search_menu.py \
  --m 3 --ordinal 164 \
  --source-run "$SOURCE" --output "$OUTPUT"
```

Use the recorded source revision: input/source hash mismatches intentionally
stop replay. The two original sample seeds are replayed, not replaced by
fresh seeds until a desired outcome appears.

## Software checks

The three new tests check the fixed plan and confidence spending, reject
source/output overlap, and detect changed input hashes. The complete test
suite passed **115 tests** on 2026-09-06. This tests the implementation and its
guards; it does not establish equilibrium uniqueness or an optimal V(m).

## Outcome

Both prespecified replicates completed and passed on 2026-09-06.

| Replicate | Full-plan regret upper | Retention regret upper | Unresolved checks |
|---:|---:|---:|---:|
| 1 | 0.0004821018299276475 | 0.00000045424917562669724 | 0 |
| 2 | 0.0004891100832591605 | 0.0000004541320410787143 | 0 |

Both supported-action checks also pass their unchanged 0.0015 tolerance.
The same frozen finite-support strategy now has sufficient independent
count-sampling audit evidence. This resolves this menu's audit uncertainty;
it does not repair the genuinely nonconverged menu 163, complete the outer
search, or establish that this menu is close to an optimum.

The original search cache remains `validation_blocked`. The follow-up summary
explicitly identifies the original menu and unchanged profile instead of
overwriting that cache. In addition, m=1 menu 193 `(0.25,0.30)` has been archived
in `results/m1_menu193_unresolved_20260906/`: two unknown histories and 249
unresolved audit checks remain. No repair or acceptance is claimed for it.

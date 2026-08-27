"""Run the three-regime equilibrium-constrained mechanism comparison.

Every reported row re-optimizes the permitted policy outside the complete
cutoff-WPBE correspondence.  The main run varies ``(m,beta,delta)`` and holds
the spatial pickup technology, incumbent retention, and outer-contact cost
fixed.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from spatial_design import (
    Environment,
    SearchConfig,
    SpatialMechanismSolver,
    mechanism_record,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "results" / "csv" / "regime_comparison.csv"
DEFAULT_METADATA = ROOT / "results" / "regime_metadata.json"

M_GRID = (0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0)
BETA_GRID = (0.6, 0.8, 0.9)
DELTA_GRID = (0.4, 0.8, 0.95)


def _config(quick: bool, s_bar: float) -> SearchConfig:
    if quick:
        return SearchConfig(
            s_bar=s_bar,
            cutoff_grid=41,
            final_cutoff_grid=201,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            certify_top_k=4,
            certify_finalists=2,
            certification_max_grid=801,
            adversarial_seeds=0,
        )
    return SearchConfig(
        s_bar=s_bar,
        cutoff_grid=61,
        final_cutoff_grid=401,
        p1_nodes=9,
        p1_refine_levels=2,
        inner_refine_levels=2,
        certify_top_k=7,
        certify_finalists=3,
        certification_max_grid=1601,
        adversarial_seeds=1,
        adversarial_maxiter=16,
        adversarial_popsize=8,
    )


def _solve_one(task: tuple[float, float, float, float, float, float, float, bool]):
    m, beta, delta, pickup_rate, retention, kappa, s_bar, quick = task
    environment = Environment(
        m=m,
        beta=beta,
        delta=delta,
        pickup_rate=pickup_rate,
        incumbent_retention=retention,
        completion_value=1.0,
        outer_contact_cost=kappa,
    )
    solver = SpatialMechanismSolver(environment, _config(quick, s_bar))
    results = solver.optimize_all()
    rows = []
    for result in results:
        row = mechanism_record(result)
        row["solver_total_evaluations"] = solver.evaluation_count
        row["quick"] = quick
        rows.append(row)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kappa", type=float, default=0.01)
    parser.add_argument("--pickup-rate", type=float, default=0.25)
    parser.add_argument("--retention", type=float, default=0.8)
    parser.add_argument("--s-bar", type=float, default=4.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--main-slice-only", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.kappa < 0:
        raise ValueError("kappa must be nonnegative")
    if not 0 <= args.retention <= 1:
        raise ValueError("retention must lie in [0,1]")

    beta_grid = (0.8,) if args.main_slice_only else BETA_GRID
    delta_grid = (0.8,) if args.main_slice_only else DELTA_GRID
    tasks = [
        (
            m,
            beta,
            delta,
            args.pickup_rate,
            args.retention,
            args.kappa,
            args.s_bar,
            args.quick,
        )
        for beta in beta_grid
        for delta in delta_grid
        for m in M_GRID
    ]

    if args.workers == 1:
        nested_rows = [_solve_one(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            nested_rows = list(pool.map(_solve_one, tasks))
    rows = [row for group in nested_rows for row in group]
    data = pd.DataFrame(rows).sort_values(
        ["beta", "delta", "m", "mechanism"]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.output, index=False)
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(data),
        "environment_count": len(tasks),
        "mechanisms": sorted(data["mechanism"].unique().tolist()),
        "m_grid": list(M_GRID),
        "beta_grid": list(beta_grid),
        "delta_grid": list(delta_grid),
        "pickup_rate": args.pickup_rate,
        "incumbent_retention": args.retention,
        "outer_contact_cost": args.kappa,
        "completion_value": 1.0,
        "s_bar": args.s_bar,
        "quick": args.quick,
        "search_config": asdict(_config(args.quick, args.s_bar)),
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"wrote {len(data)} rows to {args.output}")


if __name__ == "__main__":
    main()

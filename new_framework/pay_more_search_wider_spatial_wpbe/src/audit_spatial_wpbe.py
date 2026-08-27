"""Independent numerical audits for the maintained spatial cutoff-WPBE model."""

from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

from spatial_design import (
    Environment,
    SearchConfig,
    SpatialMechanismSolver,
    mechanism_record,
)
from spatial_wpbe import (
    Params,
    Policy,
    extra_pickup_cost,
    fresh_accept_intensity,
    solve_policy_certified,
)


HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "outputs" / "spatial_pickup_wpbe_v4"
CSV_DIR = OUT / "csv"
AUDIT_DIR = OUT / "audit"


def dense_config() -> SearchConfig:
    return SearchConfig(
        s_bar=4.0,
        cutoff_grid=81,
        final_cutoff_grid=801,
        p1_nodes=13,
        p1_refine_levels=3,
        inner_refine_levels=3,
        certify_top_k=14,
        certify_finalists=4,
        certification_max_grid=3201,
    )


def dense_environment(m: float) -> list[dict]:
    environment = Environment(m, 0.8, 0.8, pickup_rate=0.25)
    solver = SpatialMechanismSolver(environment, dense_config())
    records = []
    for result in solver.optimize_all():
        record = mechanism_record(result)
        record["solver_total_evaluations"] = solver.evaluation_count
        records.append(record)
    return records


def run_dense_reoptimization(workers: int) -> pd.DataFrame:
    targets = (0.5, 1.0, 4.0, 16.0)
    records: list[dict] = []
    with ProcessPoolExecutor(max_workers=min(workers, len(targets))) as executor:
        futures = {executor.submit(dense_environment, m): m for m in targets}
        for future in as_completed(futures):
            m = futures[future]
            records.extend(future.result())
            print(f"dense reoptimization complete: m={m:g}", flush=True)
    dense = pd.DataFrame(records).sort_values(["m", "mechanism"])
    dense.to_csv(CSV_DIR / "dense_reoptimization.csv", index=False)
    return dense


def compare_dense(dense: pd.DataFrame) -> pd.DataFrame:
    formal = pd.read_csv(CSV_DIR / "optimized_grid.csv")
    formal = formal[
        np.isclose(formal.beta, 0.8)
        & np.isclose(formal.delta, 0.8)
        & formal.m.isin(dense.m.unique())
    ]
    columns = ["m", "mechanism", "completion", "p1", "p2", "s", "cutoff"]
    comparison = formal[columns].merge(
        dense[columns], on=["m", "mechanism"], suffixes=("_formal", "_dense")
    )
    for variable in ("completion", "p1", "p2", "s", "cutoff"):
        comparison[f"{variable}_difference"] = (
            comparison[f"{variable}_dense"] - comparison[f"{variable}_formal"]
        )
    comparison.to_csv(CSV_DIR / "dense_reoptimization_comparison.csv", index=False)
    return comparison


def root_stress_task(task: tuple[float, float, float, float, float, float]) -> dict:
    m, beta, delta, p1, p2, search = task
    params = Params(m, beta, delta, pickup_rate=0.25)
    certificate = solve_policy_certified(
        Policy(p1, p2, search),
        params,
        initial_grid=151,
        max_grid=601,
    )
    return {
        "m": m,
        "beta": beta,
        "delta": delta,
        "p1": p1,
        "p2": p2,
        "s": search,
        "stable": certificate.stable,
        "grids": ",".join(str(grid) for grid in certificate.grids),
        "equilibrium_count": certificate.solution.equilibrium_count,
        "completion_spread": certificate.solution.completion_spread,
        "cutoffs": ",".join(
            f"{equilibrium.cutoff:.10g}"
            for equilibrium in certificate.solution.equilibria
        ),
    }


def run_root_stress(workers: int, draws: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(20260827)
    tasks = []
    for _ in range(draws):
        m = float(2 ** rng.uniform(-1.0, 4.0))
        beta = float(rng.uniform(0.55, 0.95))
        delta = float(rng.uniform(0.35, 0.98))
        p1 = float(rng.uniform(0.01, min(beta, 0.75)))
        p2 = float(rng.uniform(p1, beta))
        search = float(rng.uniform(1.0, 4.0))
        tasks.append((m, beta, delta, p1, p2, search))
    records: list[dict] = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for record in executor.map(root_stress_task, tasks, chunksize=4):
            records.append(record)
    stress = pd.DataFrame(records)
    stress.to_csv(CSV_DIR / "random_policy_root_stress.csv", index=False)
    return stress


def monte_carlo_thinning(replications: int = 300_000) -> dict:
    rng = np.random.default_rng(521903)
    params = Params(m=2.0, beta=0.8, delta=0.8, pickup_rate=0.25)
    payment, search = 0.35, 4.0
    candidates = rng.poisson(params.m * search, size=replications)
    total = int(candidates.sum())
    order_index = np.repeat(np.arange(replications), candidates)
    area_rank = rng.uniform(0.0, search, size=total)
    base_cost = rng.uniform(0.0, 1.0, size=total)
    accepted = base_cost + extra_pickup_cost(area_rank, params.pickup_rate) <= payment
    accepted_counts = np.bincount(
        order_index[accepted], minlength=replications
    )

    exact_intensity = fresh_accept_intensity(payment, search, params)
    exact_coverage = 1.0 - np.exp(-exact_intensity)
    simulated_intensity = float(accepted_counts.mean())
    simulated_coverage = float(np.mean(accepted_counts > 0))
    intensity_se = float(np.sqrt(exact_intensity / replications))
    coverage_se = float(
        np.sqrt(exact_coverage * (1.0 - exact_coverage) / replications)
    )
    return {
        "replications": replications,
        "potential_candidates": total,
        "exact_intensity": exact_intensity,
        "simulated_intensity": simulated_intensity,
        "intensity_error": simulated_intensity - exact_intensity,
        "intensity_standard_error": intensity_se,
        "exact_coverage": exact_coverage,
        "simulated_coverage": simulated_coverage,
        "coverage_error": simulated_coverage - exact_coverage,
        "coverage_standard_error": coverage_se,
    }


def main() -> None:
    workers = max(1, min(6, os.cpu_count() or 1))
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    dense = run_dense_reoptimization(workers)
    comparison = compare_dense(dense)
    stress = run_root_stress(workers)
    monte_carlo = monte_carlo_thinning()

    summary = {
        "dense_max_abs_completion_difference": float(
            comparison.completion_difference.abs().max()
        ),
        "dense_max_completion_improvement": float(
            comparison.completion_difference.max()
        ),
        "dense_min_completion_improvement": float(
            comparison.completion_difference.min()
        ),
        "random_policies": int(len(stress)),
        "random_root_sets_stable": int(stress.stable.sum()),
        "random_multiple_wpbe": int((stress.equilibrium_count > 1).sum()),
        "random_max_completion_spread": float(stress.completion_spread.max()),
        "monte_carlo": monte_carlo,
    }
    with (AUDIT_DIR / "audit_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    if not stress.stable.all():
        raise RuntimeError("at least one random policy has an unstable root set")
    if abs(monte_carlo["intensity_error"]) > 4 * monte_carlo["intensity_standard_error"]:
        raise RuntimeError("fresh-intensity Monte Carlo error exceeds four standard errors")
    if abs(monte_carlo["coverage_error"]) > 4 * monte_carlo["coverage_standard_error"]:
        raise RuntimeError("fresh-coverage Monte Carlo error exceeds four standard errors")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()

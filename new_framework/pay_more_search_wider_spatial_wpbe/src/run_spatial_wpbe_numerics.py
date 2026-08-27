"""Run equilibrium-constrained numerics for the spatial pickup-cost model."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from spatial_design import (
    Environment,
    SearchConfig,
    SpatialMechanismSolver,
    mechanism_record,
)


HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "outputs" / "spatial_pickup_wpbe_v4"
CSV_DIR = OUT / "csv"
FIG_DIR = OUT / "figures"

M_GRID = (0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0)
MAIN_BETA = 0.8
MAIN_DELTA = 0.8
CONDITION_BETAS = (0.6, 0.9)
CONDITION_DELTAS = (0.4, 0.8, 0.95)
PICKUP_RATE = 0.25
S_BAR = 4.0

COLORS = {
    "baseline": "#6B7280",
    "fixed_rescue": "#D55E00",
    "expanded_search": "#0072B2",
    "incumbent": "#CC79A7",
    "core_fresh": "#009E73",
    "outer_fresh": "#56B4E9",
}
LABELS = {
    "baseline": r"Flat baseline $(p,p,1)$",
    "fixed_rescue": r"Fixed-reach rescue $(p_1,p_2,1)$",
    "expanded_search": r"Expanded search $(p_1,p_2,s)$",
}


def _config(quick: bool = False) -> SearchConfig:
    if quick:
        return SearchConfig(
            s_bar=S_BAR,
            cutoff_grid=41,
            final_cutoff_grid=301,
            p1_nodes=7,
            p1_refine_levels=1,
            inner_refine_levels=1,
            certify_top_k=5,
            certify_finalists=2,
            certification_max_grid=1201,
        )
    return SearchConfig(
        s_bar=S_BAR,
        cutoff_grid=51,
        final_cutoff_grid=401,
        p1_nodes=9,
        p1_refine_levels=3,
        inner_refine_levels=3,
        certify_top_k=10,
        certify_finalists=3,
        certification_max_grid=1601,
    )


def environment_grid() -> list[tuple[float, float, float]]:
    grid = {(m, MAIN_BETA, MAIN_DELTA) for m in M_GRID}
    grid.update(
        (m, beta, delta)
        for m in M_GRID
        for beta in CONDITION_BETAS
        for delta in CONDITION_DELTAS
    )
    return sorted(grid)


def solve_environment(task: tuple[float, float, float, bool]) -> list[dict]:
    m, beta, delta, quick = task
    environment = Environment(m, beta, delta, PICKUP_RATE)
    solver = SpatialMechanismSolver(environment, _config(quick))
    records = []
    for result in solver.optimize_all():
        record = mechanism_record(result)
        equilibrium = result.solution.selected
        p1 = result.solution.policy.p1
        record.update(
            {
                "holdout_share": (
                    max(p1 - equilibrium.cutoff, 0.0) / p1 if p1 > 0 else 0.0
                ),
                "rescue_bonus": result.solution.policy.p2 - p1,
                "rescue_incumbent_intensity": equilibrium.rescue.incumbent_intensity,
                "rescue_core_fresh_intensity": m * result.solution.policy.p2,
                "rescue_outer_fresh_intensity": max(
                    equilibrium.rescue.fresh_accept_intensity
                    - m * result.solution.policy.p2,
                    0.0,
                ),
                "rescue_total_intensity": equilibrium.rescue.total_intensity,
                "solver_total_evaluations": solver.evaluation_count,
                "quick": quick,
            }
        )
        records.append(record)
    return records


def run_grid(quick: bool, workers: int, resume: bool) -> pd.DataFrame:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    path = CSV_DIR / ("optimized_grid_quick.csv" if quick else "optimized_grid.csv")
    tasks = environment_grid()
    existing = pd.DataFrame()
    completed: set[tuple[float, float, float]] = set()
    if resume and path.exists():
        existing = pd.read_csv(path)
        counts = existing.groupby(["m", "beta", "delta"]).mechanism.nunique()
        completed = {tuple(map(float, index)) for index, count in counts.items() if count == 3}
    tasks = [task for task in tasks if task not in completed]

    new_records: list[dict] = []
    started = time.time()
    if tasks:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(solve_environment, (*task, quick)): task for task in tasks
            }
            for done, future in enumerate(as_completed(futures), start=1):
                task = futures[future]
                records = future.result()
                new_records.extend(records)
                elapsed = time.time() - started
                print(
                    f"{done:3d}/{len(tasks)} environments | "
                    f"m={task[0]:g}, beta={task[1]:.2f}, delta={task[2]:.2f} | "
                    f"{elapsed:.1f}s",
                    flush=True,
                )
                checkpoint = pd.concat(
                    [existing, pd.DataFrame(new_records)], ignore_index=True
                )
                checkpoint.to_csv(path, index=False)

    data = pd.concat([existing, pd.DataFrame(new_records)], ignore_index=True)
    data = data.drop_duplicates(
        ["m", "beta", "delta", "mechanism"], keep="last"
    ).sort_values(["beta", "delta", "m", "mechanism"])
    data.to_csv(path, index=False)
    return data


def _style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 8.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 140,
            "savefig.dpi": 300,
            "lines.linewidth": 2.1,
            "lines.markersize": 4.5,
        }
    )


def _main(data: pd.DataFrame) -> pd.DataFrame:
    return data[
        np.isclose(data.beta, MAIN_BETA) & np.isclose(data.delta, MAIN_DELTA)
    ].copy()


def _line(ax, frame: pd.DataFrame, mechanism: str, variable: str, label=None):
    values = frame[frame.mechanism == mechanism].sort_values("m")
    ax.plot(
        values.m,
        values[variable],
        marker="o",
        color=COLORS[mechanism],
        label=label or LABELS[mechanism],
    )


def _format_m_axis(ax) -> None:
    ax.set_xscale("log", base=2)
    ticks = [0.5, 1, 2, 4, 8, 16]
    ax.set_xticks(ticks, [str(tick).rstrip("0").rstrip(".") for tick in ticks])
    ax.set_xlabel(r"Market thickness $m$")
    ax.grid(axis="y", alpha=0.22, linewidth=0.7)


def save_figure(fig, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight")
    plt.close(fig)


def figure_value(data: pd.DataFrame) -> None:
    frame = _main(data)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.8), sharey=True)
    _line(axes[0], frame, "baseline", "completion")
    _line(axes[0], frame, "fixed_rescue", "completion")
    axes[0].set_title("A. Value of a committed rescue price")
    axes[0].set_ylabel("Optimized completion rate")
    _line(axes[1], frame, "fixed_rescue", "completion")
    _line(axes[1], frame, "expanded_search", "completion")
    axes[1].set_title("B. Incremental value of expanded search")
    for ax in axes:
        _format_m_axis(ax)
        ax.set_ylim(0, min(1.0, frame.completion.max() + 0.08))
        ax.legend(frameon=False, loc="lower right")
    fig.suptitle(
        r"Every point re-optimizes its mechanism over the induced cutoff-WPBE "
        r"($\beta=\delta=0.8$)",
        y=1.02,
        fontsize=11,
    )
    fig.tight_layout()
    save_figure(fig, "figure1_optimized_value")


def figure_policy(data: pd.DataFrame) -> None:
    frame = _main(data)
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.0), sharex=True)
    for mechanism in ("baseline", "fixed_rescue", "expanded_search"):
        _line(axes[0, 0], frame, mechanism, "p1")
    axes[0, 0].set_title(r"A. First-window payment $p_1^*$")
    axes[0, 0].set_ylabel("Payment")

    for mechanism in ("fixed_rescue", "expanded_search"):
        _line(axes[0, 1], frame, mechanism, "rescue_bonus")
    axes[0, 1].axhline(0, color="#9CA3AF", linewidth=1)
    axes[0, 1].set_title(r"B. Rescue premium $p_2^*-p_1^*$")
    axes[0, 1].set_ylabel("Payment premium")

    _line(axes[1, 0], frame, "expanded_search", "s")
    axes[1, 0].axhline(1, color="#9CA3AF", linewidth=1)
    axes[1, 0].set_title(r"C. Search-area multiplier $s^*$")
    axes[1, 0].set_ylabel("Area / core area")

    for mechanism in ("baseline", "fixed_rescue", "expanded_search"):
        values = frame[frame.mechanism == mechanism].sort_values("m")
        axes[1, 1].plot(
            values.m,
            100 * values.holdout_share,
            marker="o",
            color=COLORS[mechanism],
            label=LABELS[mechanism],
        )
    axes[1, 1].set_title("D. Strategic incumbent holdout")
    axes[1, 1].set_ylabel(r"Share of $c\leq p_1^*$ waiting (%)")

    for ax in axes.flat:
        _format_m_axis(ax)
    axes[0, 0].legend(frameon=False, ncol=1)
    axes[0, 1].legend(frameon=False)
    axes[1, 0].legend(frameon=False)
    fig.suptitle("How the optimized WPBE mechanism changes with market thickness", y=1.01)
    fig.tight_layout()
    save_figure(fig, "figure2_optimal_policy")


def figure_supply(data: pd.DataFrame) -> None:
    frame = _main(data)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3), sharey=True)
    for ax, mechanism, title in (
        (axes[0], "fixed_rescue", "A. Fixed-reach rescue"),
        (axes[1], "expanded_search", "B. Expanded-search rescue"),
    ):
        values = frame[frame.mechanism == mechanism].sort_values("m")
        components = [
            values.rescue_incumbent_intensity.to_numpy(),
            values.rescue_core_fresh_intensity.to_numpy(),
        ]
        colors = [COLORS["incumbent"], COLORS["core_fresh"]]
        labels = ["Screened incumbents", "Core fresh arrivals"]
        if mechanism == "expanded_search":
            components.append(values.rescue_outer_fresh_intensity.to_numpy())
            colors.append(COLORS["outer_fresh"])
            labels.append("Outer fresh arrivals")
        ax.stackplot(values.m, *components, colors=colors, alpha=0.84, labels=labels)
        ax.plot(values.m, values.rescue_total_intensity, color="#111827", linewidth=1.5)
        for intensity, coverage in ((-np.log(0.5), "50%"), (-np.log(0.2), "80%"), (-np.log(0.05), "95%")):
            ax.axhline(intensity, color="#9CA3AF", linewidth=0.7, linestyle="--")
            ax.text(
                16.2,
                intensity,
                coverage,
                va="center",
                ha="left",
                color="#6B7280",
                fontsize=7.5,
                clip_on=False,
            )
        ax.set_title(title)
        _format_m_axis(ax)
        legend = ax.legend(frameon=True, loc="upper left")
        legend.get_frame().set_facecolor("white")
        legend.get_frame().set_alpha(0.88)
        legend.get_frame().set_edgecolor("none")
    axes[0].set_ylabel(r"Willing-driver intensity in rescue, $\lambda_2^*$")
    fig.suptitle(
        "Fixed reach already has fresh arrivals; expansion adds only the outer annulus",
        y=1.02,
    )
    fig.tight_layout()
    save_figure(fig, "figure3_rescue_supply")


def _supply_panel(ax, frame: pd.DataFrame, mechanism: str) -> None:
    values = frame[frame.mechanism == mechanism].sort_values("m")
    components = [
        values.rescue_incumbent_intensity.to_numpy(),
        values.rescue_core_fresh_intensity.to_numpy(),
    ]
    colors = [COLORS["incumbent"], COLORS["core_fresh"]]
    labels = ["Screened incumbents", "Core fresh arrivals"]
    if mechanism == "expanded_search":
        components.append(values.rescue_outer_fresh_intensity.to_numpy())
        colors.append(COLORS["outer_fresh"])
        labels.append("Outer fresh arrivals")
    ax.stackplot(values.m, *components, colors=colors, alpha=0.84, labels=labels)
    ax.plot(values.m, values.rescue_total_intensity, color="#111827", linewidth=1.5)
    for intensity, coverage in ((-np.log(0.5), "50%"), (-np.log(0.2), "80%"), (-np.log(0.05), "95%")):
        ax.axhline(intensity, color="#9CA3AF", linewidth=0.7, linestyle="--")
        ax.text(
            16.2,
            intensity,
            coverage,
            va="center",
            ha="left",
            color="#6B7280",
            fontsize=7.2,
            clip_on=False,
        )
    _format_m_axis(ax)
    legend = ax.legend(frameon=True, loc="upper left")
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_alpha(0.88)
    legend.get_frame().set_edgecolor("none")


def figure_fixed_story(data: pd.DataFrame) -> None:
    frame = _main(data)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.75))
    _line(axes[0], frame, "baseline", "completion")
    _line(axes[0], frame, "fixed_rescue", "completion")
    axes[0].set_title("A. Optimized completion")
    axes[0].set_ylabel("Completion rate")
    axes[0].legend(frameon=False, loc="lower right")
    _format_m_axis(axes[0])

    _supply_panel(axes[1], frame, "fixed_rescue")
    axes[1].set_title("B. Rescue supply at the optimized WPBE")
    axes[1].set_ylabel(r"Willing-driver intensity $\lambda_2^*$")
    fig.suptitle(
        r"Fixed-reach rescue: reprice the same catchment, which already has fresh arrivals",
        y=1.02,
    )
    fig.tight_layout()
    save_figure(fig, "figure_fixed_rescue_story")


def figure_expanded_story(data: pd.DataFrame) -> None:
    frame = _main(data)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.75))
    _line(axes[0], frame, "fixed_rescue", "completion")
    _line(axes[0], frame, "expanded_search", "completion")
    axes[0].set_title("A. Incremental completion value")
    axes[0].set_ylabel("Completion rate")
    axes[0].legend(frameon=False, loc="lower right")
    _format_m_axis(axes[0])

    _supply_panel(axes[1], frame, "expanded_search")
    axes[1].set_title("B. Expansion adds only the outer annulus")
    axes[1].set_ylabel(r"Willing-driver intensity $\lambda_2^*$")
    fig.suptitle(
        r"Expanded-search rescue: widen area and pay progressively costlier pickup drivers",
        y=1.02,
    )
    fig.tight_layout()
    save_figure(fig, "figure_expanded_search_story")


def figure_conditions(data: pd.DataFrame) -> None:
    fig, axes = plt.subplots(
        2, 2, figsize=(10.8, 7.0), sharex=True, sharey="row"
    )
    linestyles = {0.4: ":", 0.8: "-", 0.95: "-."}
    for column, beta in enumerate(CONDITION_BETAS):
        gains_fixed = []
        gains_expanded = []
        for delta in CONDITION_DELTAS:
            subset = data[
                np.isclose(data.beta, beta) & np.isclose(data.delta, delta)
            ]
            pivot = subset.pivot(index="m", columns="mechanism", values="completion")
            pivot = pivot.reindex(M_GRID)
            fixed_gain = 100 * (pivot.fixed_rescue - pivot.baseline)
            expanded_gain = 100 * (pivot.expanded_search - pivot.fixed_rescue)
            gains_fixed.append(fixed_gain.to_numpy())
            gains_expanded.append(expanded_gain.to_numpy())
            axes[0, column].plot(
                M_GRID,
                fixed_gain,
                marker="o",
                color=COLORS["fixed_rescue"],
                linestyle=linestyles[delta],
                label=rf"$\delta={delta:g}$",
            )
            axes[1, column].plot(
                M_GRID,
                expanded_gain,
                marker="o",
                color=COLORS["expanded_search"],
                linestyle=linestyles[delta],
                label=rf"$\delta={delta:g}$",
            )
        fixed_array = np.asarray(gains_fixed)
        expanded_array = np.asarray(gains_expanded)
        axes[0, column].fill_between(
            M_GRID,
            fixed_array.min(axis=0),
            fixed_array.max(axis=0),
            color=COLORS["fixed_rescue"],
            alpha=0.10,
        )
        axes[1, column].fill_between(
            M_GRID,
            expanded_array.min(axis=0),
            expanded_array.max(axis=0),
            color=COLORS["expanded_search"],
            alpha=0.10,
        )
        axes[0, column].set_title(rf"Rider delay factor $\beta={beta:g}$")
        for row in (0, 1):
            axes[row, column].axhline(0, color="#9CA3AF", linewidth=0.8)
            _format_m_axis(axes[row, column])
    axes[0, 0].set_ylabel("Fixed rescue value\n(percentage points)")
    axes[1, 0].set_ylabel("Expanded search value\n(percentage points)")
    axes[0, 1].legend(frameon=False, title="Driver patience")
    axes[1, 1].legend(frameon=False, title="Driver patience")
    fig.suptitle(
        "Under which market conditions does each additional mechanism tool work best?",
        y=1.01,
    )
    fig.tight_layout()
    save_figure(fig, "figure4_market_conditions")


def write_metadata(data: pd.DataFrame, quick: bool) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    metadata = {
        "model": "spatial PPP, assignment-contingent driver-paid pickup cost",
        "mechanisms": ["(p,p,1)", "(p1,p2,1)", "(p1,p2,s)"],
        "equilibrium": "all cutoff-WPBE enumerated; conservative selection",
        "outer_objective": "maximize completion over each mechanism domain",
        "pickup_rate": PICKUP_RATE,
        "s_bar": S_BAR,
        "m_grid": list(M_GRID),
        "main_beta_delta": [MAIN_BETA, MAIN_DELTA],
        "condition_betas": list(CONDITION_BETAS),
        "condition_deltas": list(CONDITION_DELTAS),
        "search_config": asdict(_config(quick)),
        "environment_count": int(data[["m", "beta", "delta"]].drop_duplicates().shape[0]),
        "all_certifications_stable": bool(data.certification_stable.all()),
        "quick": quick,
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument(
        "--workers", type=int, default=max(1, min(6, os.cpu_count() or 1))
    )
    args = parser.parse_args()

    data = run_grid(args.quick, args.workers, not args.no_resume)
    expected = len(environment_grid()) * 3
    if len(data) != expected:
        raise RuntimeError(f"expected {expected} optimized rows, found {len(data)}")
    if not data.certification_stable.all():
        unstable = data.loc[
            ~data.certification_stable,
            ["m", "beta", "delta", "mechanism", "certification_grids"],
        ]
        raise RuntimeError(f"unstable cutoff correspondence:\n{unstable}")

    _style()
    figure_value(data)
    figure_policy(data)
    figure_supply(data)
    figure_fixed_story(data)
    figure_expanded_story(data)
    figure_conditions(data)
    write_metadata(data, args.quick)
    print(f"saved results to {OUT}", flush=True)


if __name__ == "__main__":
    sys.exit(main())

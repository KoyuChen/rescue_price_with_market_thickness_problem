"""Figures for the five-page group-meeting note.

The inputs must use the committed-reach objective.  Each displayed point is an
architecture-specific outer optimum evaluated at its induced cutoff-WPBE.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "csv" / "regime_comparison_committed.csv"
FIGURES = ROOT / "figures"

PURPLE = "#7E57A6"
GREEN = "#008A65"
BLUE = "#1769AA"
GRAY = "#68717D"
LIGHT_GRAY = "#D7DCE2"

LABELS = {
    "incumbent_only": "I: retained incumbents",
    "fixed_arrivals": "A: + fresh core arrivals",
    "expanded_search": "E: + outer rescue reach",
}
COLORS = {
    "incumbent_only": PURPLE,
    "fixed_arrivals": GREEN,
    "expanded_search": BLUE,
}


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10.8,
            "axes.titlesize": 11.6,
            "axes.labelsize": 10.8,
            "legend.fontsize": 9.2,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 160,
            "savefig.dpi": 320,
            "lines.linewidth": 2.25,
            "lines.markersize": 4.8,
        }
    )


def _load() -> pd.DataFrame:
    data = pd.read_csv(DATA)
    if not data["search_cost_basis"].eq("committed_reach").all():
        raise ValueError("group-meeting figures require committed-reach results")
    if data[["beta", "delta"]].drop_duplicates().shape[0] != 1:
        raise ValueError("five-page figures expect one transparent calibration slice")
    return data.sort_values(["mechanism", "m"]).copy()


def _m_axis(ax: plt.Axes) -> None:
    ax.set_xscale("log", base=2)
    ax.set_xlim(0.46, 16.8)
    ax.set_xticks([0.5, 1, 2, 4, 8, 16], ["0.5", "1", "2", "4", "8", "16"])
    ax.set_xlabel(r"Local per-window driver flow $m$")
    ax.grid(axis="y", color=LIGHT_GRAY, linewidth=0.7, alpha=0.75)


def plot_reoptimized_values(data: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.65, 3.35))

    for mechanism in ("incumbent_only", "fixed_arrivals", "expanded_search"):
        group = data[data["mechanism"].eq(mechanism)].sort_values("m")
        axes[0].plot(
            group["m"],
            group["design_value"],
            color=COLORS[mechanism],
            marker="o",
            label=LABELS[mechanism],
        )
    axes[0].set_title("A. Each architecture reoptimizes its menu")
    axes[0].set_ylabel(r"Optimized objective value ($B=1$)")
    axes[0].set_ylim(0.0, 1.0)
    axes[0].legend(frameon=False, loc="lower right", handlelength=2.2)

    pivot = data.pivot(index="m", columns="mechanism", values="design_value")
    arrival_gap = pivot["fixed_arrivals"] - pivot["incumbent_only"]
    search_gap = pivot["expanded_search"] - pivot["fixed_arrivals"]
    axes[1].plot(
        arrival_gap.index,
        arrival_gap,
        color=GREEN,
        marker="o",
    )
    axes[1].plot(
        search_gap.index,
        search_gap,
        color=BLUE,
        marker="o",
    )
    axes[1].axhline(0.0, color=GRAY, linewidth=0.9)
    axes[1].set_title("B. The two gains peak at different thicknesses")
    axes[1].set_ylabel("Incremental objective value")
    axes[1].set_ylim(0.0, 0.155)
    axes[1].annotate(
        r"fresh arrivals: $V_A-V_I$",
        (16.0, float(arrival_gap.loc[16.0])),
        xytext=(-116, 5), textcoords="offset points", color=GREEN, fontsize=9.0,
    )
    axes[1].annotate(
        r"outer reach: $V_E-V_A$",
        (6.0, float(search_gap.loc[6.0])),
        xytext=(-12, 10), textcoords="offset points", color=BLUE, fontsize=9.0,
    )

    for series, color, offset in (
        (arrival_gap, GREEN, (8, 7)),
        (search_gap, BLUE, (8, -19)),
    ):
        peak_m = float(series.idxmax())
        peak_value = float(series.max())
        axes[1].scatter(
            [peak_m], [peak_value], s=64, facecolor="white", edgecolor=color,
            linewidth=1.8, zorder=4,
        )
        axes[1].annotate(
            rf"largest tested: $m={peak_m:g}$",
            (peak_m, peak_value),
            xytext=offset,
            textcoords="offset points",
            color=color,
            fontsize=8.7,
        )

    for ax in axes:
        _m_axis(ax)
    fig.suptitle(
        "Fresh replenishment matters later; geographic reach matters first",
        y=1.015,
        fontsize=12.4,
    )
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"figure_reoptimized_values.{suffix}",
            bbox_inches="tight",
        )
    plt.close(fig)


def plot_optimal_controls(data: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.65, 3.35))

    for mechanism in ("incumbent_only", "fixed_arrivals", "expanded_search"):
        group = data[data["mechanism"].eq(mechanism)].sort_values("m")
        axes[0].plot(
            group["m"],
            group["p2"] - group["p1"],
            color=COLORS[mechanism],
            marker="o",
            label={
                "incumbent_only": "I",
                "fixed_arrivals": "A",
                "expanded_search": "E",
            }[mechanism],
        )
    axes[0].axhline(0.0, color=GRAY, linewidth=0.9)
    axes[0].set_title(r"A. Rescue bonus $p_2^*-p_1^*$")
    axes[0].set_ylabel("Optimized price increment")
    axes[0].set_ylim(0.0, 0.23)
    axes[0].legend(
        frameon=False, loc="upper center", ncol=3, handlelength=2.0,
        columnspacing=1.2,
    )

    expanded = data[data["mechanism"].eq("expanded_search")].sort_values("m")
    axes[1].plot(expanded["m"], expanded["s"], color=BLUE, marker="o")
    axes[1].axhline(1.0, color=GREEN, linestyle=":", linewidth=1.4)
    axes[1].axhline(4.0, color=GRAY, linestyle=":", linewidth=1.2)
    axes[1].text(0.49, 1.08, r"fixed footprint: $s=1$", color=GREEN, fontsize=8.8)
    axes[1].text(0.49, 3.82, r"search cap: $\bar s=4$", color=GRAY, fontsize=8.8)
    axes[1].set_title(r"B. Rescue-area multiplier $s^*$")
    axes[1].set_ylabel("Optimized search area")
    axes[1].set_ylim(0.85, 4.18)
    no_search = expanded[np.isclose(expanded["s"], 1.0, atol=1e-8)]
    if not no_search.empty:
        first = no_search.iloc[0]
        axes[1].annotate(
            "no expansion on the\ntested thick-market tail",
            (first["m"], first["s"]),
            xytext=(-82, 42),
            textcoords="offset points",
            arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 1.0},
            color=GREEN,
            fontsize=8.7,
        )

    for ax in axes:
        _m_axis(ax)
    fig.suptitle(
        "Search scope contracts before the rescue price increment disappears",
        y=1.015,
        fontsize=12.4,
    )
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"figure_optimal_controls.{suffix}",
            bbox_inches="tight",
        )
    plt.close(fig)


def main() -> None:
    _style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    data = _load()
    plot_reoptimized_values(data)
    plot_optimal_controls(data)


if __name__ == "__main__":
    main()

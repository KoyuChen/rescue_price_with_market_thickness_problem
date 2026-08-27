"""Create the group-meeting figures for the three-regime comparison."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
COSTLY_DATA = ROOT / "results" / "csv" / "regime_comparison.csv"
FREE_DATA = ROOT / "results" / "csv" / "regime_comparison_free_search.csv"
FIGURES = ROOT / "figures"

GRAY = "#6B7280"
PURPLE = "#8C6BB1"
GREEN = "#009E73"
BLUE = "#0072B2"
LIGHT_BLUE = "#56B4E9"
ORANGE = "#D55E00"
GRID = "#D1D5DB"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.size": 11.2,
            "axes.titlesize": 12.0,
            "axes.labelsize": 11.2,
            "legend.fontsize": 10.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "lines.linewidth": 2.25,
            "lines.markersize": 4.8,
        }
    )


def _main_slice(data: pd.DataFrame) -> pd.DataFrame:
    return data[
        np.isclose(data["beta"], 0.8) & np.isclose(data["delta"], 0.8)
    ].copy()


def _finish_m_axis(ax: plt.Axes) -> None:
    ax.set_xscale("log", base=2)
    ax.set_xlim(0.45, 16.7)
    ax.set_xticks([0.5, 1, 2, 4, 8, 16], ["0.5", "1", "2", "4", "8", "16"])
    ax.set_xlabel(r"Core market thickness $m$ (log$_2$ scale)")
    ax.grid(axis="y", color=GRID, alpha=0.55, linewidth=0.7)


def plot_arrival_value(data: pd.DataFrame) -> None:
    main = _main_slice(data)
    incumbent = main[main["mechanism"].eq("incumbent_only")].sort_values("m")
    arrivals = main[main["mechanism"].eq("fixed_arrivals")].sort_values("m")
    merged = incumbent[["m", "completion"]].merge(
        arrivals[["m", "completion"]], on="m", suffixes=("_i", "_a")
    )
    merged["gain"] = 100 * (merged["completion_a"] - merged["completion_i"])

    fig, axes = plt.subplots(1, 2, figsize=(8.7, 3.55))
    axes[0].plot(
        merged["m"], merged["completion_i"], color=PURPLE, marker="o",
        label="Retained incumbents only",
    )
    axes[0].plot(
        merged["m"], merged["completion_a"], color=GREEN, marker="o",
        label="Add fresh core arrivals",
    )
    axes[0].set_title("A. Best cross-checked completion")
    axes[0].set_ylabel("Completion probability")
    axes[0].set_ylim(0.08, 0.93)
    axes[0].legend(frameon=False, loc="lower right")

    axes[1].plot(merged["m"], merged["gain"], color=GREEN, marker="o")
    axes[1].fill_between(
        merged["m"], 0, merged["gain"], color=GREEN, alpha=0.15
    )
    peak = merged.loc[merged["gain"].idxmax()]
    axes[1].scatter([peak["m"]], [peak["gain"]], color=GREEN, s=52, zorder=4)
    axes[1].annotate(
        f"peak {peak['gain']:.1f} pp",
        (peak["m"], peak["gain"]),
        xytext=(8, 8), textcoords="offset points", color=GREEN,
    )
    axes[1].set_title("B. Value of time-homogeneous arrivals")
    axes[1].set_ylabel("Completion gain (percentage points)")
    axes[1].set_ylim(bottom=0)

    for ax in axes:
        _finish_m_axis(ax)
    fig.suptitle(
        r"Same cross-checked $(p_1,p_2)$ design; only period-2 supply changes",
        y=1.02,
        fontsize=12.5,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "figure_arrival_value.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / "figure_arrival_value.png", bbox_inches="tight")
    plt.close(fig)


def plot_search_geometry() -> None:
    fig, ax = plt.subplots(figsize=(4.15, 3.25))
    ax.set_aspect("equal")
    ax.axis("off")
    outer = Circle((0, 0), 1.55, facecolor=LIGHT_BLUE, edgecolor=BLUE, alpha=0.48, lw=2)
    core = Circle((0, 0), 1.0, facecolor="#BFE8D7", edgecolor=GREEN, alpha=0.96, lw=2)
    ax.add_patch(outer)
    ax.add_patch(core)
    ax.annotate(
        "", xy=(-0.71, -0.71), xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 1.8},
    )
    ax.annotate(
        "", xy=(1.34, 0.78), xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.8},
    )
    ax.text(-0.54, -0.43, r"$R_0$", color=GREEN, ha="center", rotation=45)
    ax.text(0.92, 0.62, r"$R_0\sqrt{s}$", color=BLUE, ha="center", rotation=30)
    ax.text(0, 0.18, "Core fresh cohort", ha="center", color="#075E46", weight="bold")
    ax.text(0, -0.05, r"area $=1$, mean $m$", ha="center", color="#075E46")
    ax.text(0, 1.30, "Outer annulus", ha="center", color="#075985", weight="bold")
    ax.text(0, 1.08, r"area $=s-1$, mean $(s-1)m$", ha="center", color="#075985")
    ax.text(-1.85, -1.62, r"$s=1$: fixed footprint", color=GREEN, ha="left")
    ax.text(0.25, -1.62, r"$s>1$: expanded rescue only", color=BLUE, ha="left")
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.75, 1.75)
    fig.tight_layout(pad=0.1)
    fig.savefig(FIGURES / "figure_search_geometry.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_search_decision(costly: pd.DataFrame, free: pd.DataFrame) -> None:
    costly_main = _main_slice(costly)
    free_main = _main_slice(free)
    expanded = costly_main[costly_main["mechanism"].eq("expanded_search")].sort_values("m")
    fixed = costly_main[costly_main["mechanism"].eq("fixed_arrivals")].sort_values("m")
    free_expanded = free_main[free_main["mechanism"].eq("expanded_search")].sort_values("m")
    merged = expanded[["m", "s", "design_value"]].merge(
        fixed[["m", "design_value"]], on="m", suffixes=("_e", "_a")
    )
    merged["gain"] = 100 * (merged["design_value_e"] - merged["design_value_a"])

    fig, axes = plt.subplots(1, 2, figsize=(8.7, 3.55))
    axes[0].plot(
        free_expanded["m"], free_expanded["s"], color=GRAY, marker="o",
        linestyle="--", label=r"Free outer contacts: $\kappa=0$",
    )
    axes[0].plot(
        merged["m"], merged["s"], color=BLUE, marker="o",
        label=r"Costly outer contacts: $\kappa=0.0125$",
    )
    axes[0].axhline(1, color=GREEN, linestyle=":", linewidth=1.2)
    axes[0].axhline(4, color=GRAY, linestyle=":", linewidth=1.0)
    axes[0].text(0.48, 1.07, "no expansion", color=GREEN, fontsize=9.5)
    axes[0].text(0.48, 3.83, "search cap", color=GRAY, fontsize=9.5)
    axes[0].set_title("A. Selected search-area multiplier")
    axes[0].set_ylabel(r"Selected $s$")
    axes[0].set_ylim(0.85, 4.18)
    axes[0].legend(frameon=False, loc="center right")

    axes[1].plot(merged["m"], merged["gain"], color=BLUE, marker="o")
    axes[1].fill_between(
        merged["m"], 0, merged["gain"], color=LIGHT_BLUE, alpha=0.22
    )
    axes[1].axhline(0, color=GRAY, linewidth=0.9)
    zero = merged[np.isclose(merged["s"], 1.0, atol=1e-3)]
    if not zero.empty:
        first = zero.iloc[0]
        axes[1].annotate(
            r"choose $s^*=1$",
            (first["m"], first["gain"]),
            xytext=(-45, 18), textcoords="offset points", color=GREEN,
            arrowprops={"arrowstyle": "->", "color": GREEN, "lw": 1.0},
        )
    axes[1].set_title("B. Net value of expanding beyond the core")
    axes[1].set_ylabel(r"$100\,[V_E^\kappa-V_A]$ (points)")
    axes[1].set_ylim(bottom=-0.25)

    for ax in axes:
        _finish_m_axis(ax)
    fig.suptitle(
        "Incremental outer-contact cost turns reach into an economic choice",
        y=1.02,
        fontsize=12.5,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "figure_search_decision.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / "figure_search_decision.png", bbox_inches="tight")
    plt.close(fig)


def plot_market_conditions(data: pd.DataFrame) -> None:
    rows = []
    for (beta, delta), group in data.groupby(["beta", "delta"]):
        pivot_c = group.pivot(index="m", columns="mechanism", values="completion")
        pivot_j = group.pivot(index="m", columns="mechanism", values="design_value")
        expanded = group[group["mechanism"].eq("expanded_search")].set_index("m")
        arrival_peak = 100 * (pivot_c["fixed_arrivals"] - pivot_c["incumbent_only"]).max()
        no_search = expanded[np.isclose(expanded["s"], 1.0, atol=1e-3)]
        threshold = float(no_search.index.min()) if not no_search.empty else np.inf
        search_peak = 100 * (pivot_j["expanded_search"] - pivot_j["fixed_arrivals"]).max()
        rows.append((beta, delta, arrival_peak, threshold, search_peak))
    summary = pd.DataFrame(
        rows, columns=["beta", "delta", "arrival_peak", "threshold", "search_peak"]
    )
    betas = sorted(summary["beta"].unique())
    deltas = sorted(summary["delta"].unique())
    arrival = summary.pivot(index="delta", columns="beta", values="arrival_peak").loc[deltas, betas]
    threshold = summary.pivot(index="delta", columns="beta", values="threshold").loc[deltas, betas]

    fig, axes = plt.subplots(1, 2, figsize=(8.7, 3.55))
    im0 = axes[0].imshow(arrival.to_numpy(), cmap="YlGn", aspect="auto", vmin=0)
    axes[0].set_title("A. Peak value of core arrivals (pp)")
    im1 = axes[1].imshow(
        np.where(np.isfinite(threshold), np.log2(threshold), np.log2(24)),
        cmap="Blues_r", aspect="auto", vmin=np.log2(0.5), vmax=np.log2(24),
    )
    axes[1].set_title(r"B. First tested $m_0$ with $s^*=1$")

    for ax in axes:
        ax.set_xticks(range(len(betas)), [f"{x:.1f}" for x in betas])
        ax.set_yticks(range(len(deltas)), [f"{x:.2g}" for x in deltas])
        ax.set_xlabel(r"Rider patience $\beta$")
        ax.set_ylabel(r"Incumbent patience $\delta$")
        ax.tick_params(length=0)
    for i in range(len(deltas)):
        for j in range(len(betas)):
            arrival_value = float(arrival.iloc[i, j])
            axes[0].text(
                j, i, f"{arrival_value:.1f}", ha="center", va="center",
                color="white" if im0.norm(arrival_value) > 0.55 else "#111827",
                weight="semibold",
            )
            value = threshold.iloc[i, j]
            plotted_value = np.log2(value) if np.isfinite(value) else np.log2(24)
            axes[1].text(
                j, i, f"{value:g}" if np.isfinite(value) else ">16",
                ha="center", va="center",
                color="white" if im1.norm(plotted_value) < 0.40 else "#111827",
                weight="semibold",
            )
    for im, ax in ((im0, axes[0]), (im1, axes[1])):
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.suptitle(
        r"Cross-search $(p_1,p_2,s)$ and re-solve its cutoff-WPBE in every cell",
        y=1.02,
        fontsize=12.5,
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "figure_market_conditions.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / "figure_market_conditions.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    costly = pd.read_csv(COSTLY_DATA)
    free = pd.read_csv(FREE_DATA)
    plot_arrival_value(costly)
    plot_search_geometry()
    plot_search_decision(costly, free)
    plot_market_conditions(costly)


if __name__ == "__main__":
    main()

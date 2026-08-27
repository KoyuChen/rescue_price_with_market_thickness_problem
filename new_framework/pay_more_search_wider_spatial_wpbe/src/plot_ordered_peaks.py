"""Create the group-meeting ordered-peaks figure.

Panel A uses the archived equilibrium-constrained mechanism optima. Panel B
plots the closed-form common-Poisson-branch benchmark used in the theorem.
"""

from __future__ import annotations

from pathlib import Path
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "csv" / "optimized_grid.csv"
FIGURES = ROOT / "figures"

ORANGE = "#D55E00"
BLUE = "#0072B2"
GRAY = "#6B7280"


def closed_form_peak(a: float, b: float) -> float:
    if not 0 < a < b:
        raise ValueError("closed-form peak requires 0 < a < b")
    return math.log(b / a) / (b - a)


def main() -> None:
    data = pd.read_csv(DATA)
    main_slice = data[
        np.isclose(data["beta"], 0.8) & np.isclose(data["delta"], 0.8)
    ]
    pivot = main_slice.pivot(index="m", columns="mechanism", values="completion")
    pivot = pivot.sort_index()
    fixed_gain = 100 * (pivot["fixed_rescue"] - pivot["baseline"])
    search_gain = 100 * (pivot["expanded_search"] - pivot["fixed_rescue"])

    # Illustrative common-branch rates. The theorem holds for every ordered
    # tuple; these values are chosen only to make the separation visible.
    r, lam0, lamf, lame = 0.15, 0.10, 0.35, 1.20
    m = np.geomspace(0.25, 16.0, 600)
    delta_p = np.exp(-r * m) * (np.exp(-lam0 * m) - np.exp(-lamf * m))
    delta_s = np.exp(-r * m) * (np.exp(-lamf * m) - np.exp(-lame * m))
    m_p = closed_form_peak(r + lam0, r + lamf)
    m_s = closed_form_peak(r + lamf, r + lame)
    separator = 1.0 / (r + lamf)

    plt.rcParams.update(
        {
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.3,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "lines.linewidth": 2.2,
            "lines.markersize": 4.6,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.65))

    ax = axes[0]
    ax.plot(pivot.index, fixed_gain, color=ORANGE, marker="o", label=r"Pay layer $V_F-V_0$")
    ax.plot(pivot.index, search_gain, color=BLUE, marker="o", label=r"Search layer $V_E-V_F$")
    mp_num = float(fixed_gain.idxmax())
    ms_num = float(search_gain.idxmax())
    ax.scatter([mp_num], [fixed_gain.loc[mp_num]], color=ORANGE, s=55, zorder=5)
    ax.scatter([ms_num], [search_gain.loc[ms_num]], color=BLUE, s=55, zorder=5)
    ax.annotate(r"search peak $m\approx1$", (ms_num, search_gain.loc[ms_num]),
                xytext=(8, -18), textcoords="offset points", color=BLUE)
    ax.annotate(r"pay peak $m\approx6$", (mp_num, fixed_gain.loc[mp_num]),
                xytext=(-47, 12), textcoords="offset points", color=ORANGE)
    ax.set_title("A. Full optimized cutoff-WPBE numerics")
    ax.set_ylabel("Incremental completion (percentage points)")
    ax.legend(frameon=False, loc="upper right")

    ax = axes[1]
    ax.plot(m, 100 * delta_p, color=ORANGE, label=r"$\Delta_P^0(m)$")
    ax.plot(m, 100 * delta_s, color=BLUE, label=r"$\Delta_S^0(m)$")
    ax.axvline(m_s, color=BLUE, linestyle="--", linewidth=1.1)
    ax.axvline(m_p, color=ORANGE, linestyle="--", linewidth=1.1)
    ax.axvline(separator, color=GRAY, linestyle=":", linewidth=1.2)
    ax.scatter([m_s], [100 * np.interp(m_s, m, delta_s)], color=BLUE, s=50, zorder=5)
    ax.scatter([m_p], [100 * np.interp(m_p, m, delta_p)], color=ORANGE, s=50, zorder=5)
    ax.text(m_s, ax.get_ylim()[1] * 0.95, r"$m_S^*$", color=BLUE, ha="center", va="top")
    ax.text(m_p, ax.get_ylim()[1] * 0.95, r"$m_P^*$", color=ORANGE, ha="center", va="top")
    ax.text(separator, ax.get_ylim()[1] * 0.70,
            r"separator $1/(r+\lambda_F)$", color=GRAY, ha="center", va="top",
            rotation=90, fontsize=8)
    ax.set_title("B. Common Poisson-WPBE branch: closed form")
    ax.set_ylabel("Benchmark incremental completion (points)")
    ax.legend(frameon=False, loc="upper right")

    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_xlim(0.45, 16.5)
        ax.set_xticks([0.5, 1, 2, 4, 8, 16], ["0.5", "1", "2", "4", "8", "16"])
        ax.set_xlabel(r"Market thickness $m$")
        ax.axhline(0, color="#9CA3AF", linewidth=0.8)
        ax.grid(axis="y", alpha=0.20, linewidth=0.7)

    fig.suptitle(
        "The search increment peaks first; the price increment peaks later",
        y=1.015,
        fontsize=11.2,
    )
    fig.tight_layout()
    FIGURES.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"figure5_ordered_peaks.{suffix}", bbox_inches="tight")
    plt.close(fig)

    assert m_s < separator < m_p
    print(f"m_S={m_s:.6f}, separator={separator:.6f}, m_P={m_p:.6f}")


if __name__ == "__main__":
    main()

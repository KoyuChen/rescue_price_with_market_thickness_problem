"""Generate formal-paper-only theoretical figures and tables.

These outputs use assumed parameters and are deliberately labeled numerical
illustrations. They do not read empirical data and must not be presented as a
calibration.
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
FORMAL_DIR = SCRIPT_DIR.parent
REPO_ROOT = FORMAL_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT / "code"))

from discount_model import (  # noqa: E402
    DiscountParams,
    corrected_local_coefficient,
    optimize_flat_noentry,
    optimize_geometry,
)


ALPHA = 1.0
BETA = 0.8
DELTA = 0.8


def solve_noentry(m: float):
    par = DiscountParams(m=m, alpha=ALPHA, beta=BETA, gamma=0.0, delta=DELTA)
    return optimize_geometry(par, grid_size=181, xatol=8e-13)


def write_table(rows: list[tuple[float, object]], path: Path) -> None:
    lines = [
        r"\begin{tabular}{rrrrrrr}",
        r"\toprule",
        r"$m$ & $p_1^*$ & $p_2^*$ & $a^*$ & $M_R^*$ & $M_F^*$ & $100V(m)$ \\",
        r"\midrule",
    ]
    for m, result in rows:
        point = result.point
        lines.append(
            f"{m:g} & {point.p:.4f} & {point.q:.4f} & {point.a:.4f} & "
            f"{result.dynamic_value:.4f} & {result.flat_value:.4f} & "
            f"{100 * result.gain:.4f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    figure_dir = FORMAL_DIR / "figures"
    table_dir = FORMAL_DIR / "tables"
    figure_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    m_grid = np.geomspace(0.05, 100.0, 121)
    results = [solve_noentry(float(m)) for m in m_grid]
    p1 = np.array([x.point.p for x in results])
    p2 = np.array([x.point.q for x in results])
    dynamic = np.array([x.dynamic_value for x in results])
    flat = np.array([x.flat_value for x in results])
    gain_pp = 100 * (dynamic - flat)

    peak = minimize_scalar(
        lambda log_m: -solve_noentry(float(np.exp(log_m))).gain,
        bounds=(float(np.log(0.05)), float(np.log(100.0))),
        method="bounded",
        options={"xatol": 2e-8, "maxiter": 100},
    )
    peak_m = float(np.exp(peak.x))
    peak_gain = 100 * solve_noentry(peak_m).gain

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.titlesize": 9,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
        }
    )
    blue = "#1f5a94"
    orange = "#c35a22"
    gray = "#5b6573"

    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.25), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(m_grid, p1, color=blue, linewidth=1.8, label=r"$p_1^*(m)$")
    ax.plot(m_grid, p2, color=orange, linewidth=1.8, linestyle="--", label=r"$p_2^*(m)$")
    ax.set_xscale("log")
    ax.set_ylabel("Payment")
    ax.set_title("(a) Optimal announced menu")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2, linewidth=0.5)

    ax = axes[0, 1]
    ax.plot(m_grid, flat, color=gray, linewidth=1.7, linestyle=":", label=r"$M_F^*(m)$")
    ax.plot(m_grid, dynamic, color=blue, linewidth=1.8, label=r"$M_R^*(m)$")
    ax.set_xscale("log")
    ax.set_ylabel("Completion probability")
    ax.set_title("(b) Optimized completion")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2, linewidth=0.5)

    ax = axes[1, 0]
    ax.plot(m_grid, gain_pp, color=orange, linewidth=2.0)
    ax.scatter([peak_m], [peak_gain], marker="o", s=26, color="black", zorder=3)
    ax.annotate(
        f"numerical peak\n$m={peak_m:.2f}$, {peak_gain:.2f} pp",
        xy=(peak_m, peak_gain),
        xytext=(0.44, 0.66),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "lw": 0.7},
        fontsize=8,
    )
    ax.set_xscale("log")
    ax.set_xlabel(r"Expected incumbent thickness $m$")
    ax.set_ylabel(r"$100V(m)$ (percentage points)")
    ax.set_title("(c) Completion value of rescue pricing")
    ax.grid(alpha=0.2, linewidth=0.5)

    ax = axes[1, 1]
    for gamma, style, color in (
        (0.0, "-", blue),
        (0.25, "--", orange),
        (1.0, ":", gray),
    ):
        coefficients = []
        for m in m_grid:
            p_flat, _ = optimize_flat_noentry(float(m))
            par = DiscountParams(
                m=float(m), alpha=0.8, beta=BETA, gamma=gamma, delta=DELTA
            )
            coefficients.append(100 * corrected_local_coefficient(p_flat, par))
        ax.plot(
            m_grid,
            coefficients,
            linestyle=style,
            color=color,
            linewidth=1.7,
            label=rf"$\gamma={gamma:g}$",
        )
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xscale("log")
    ax.set_xlabel(r"Expected incumbent thickness $m$")
    ax.set_ylabel("Local gain per unit rescue (pp)")
    ax.set_title(r"(d) Survival and entry extension ($\alpha=.8$)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2, linewidth=0.5)

    fig.savefig(figure_dir / "theory_profiles.pdf", bbox_inches="tight")
    fig.savefig(figure_dir / "theory_profiles.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    selected = [(m, solve_noentry(m)) for m in (1.0, 5.0, 10.0, 20.0)]
    write_table(selected, table_dir / "theory_selected_m.tex")
    print(
        f"THEORETICAL ILLUSTRATION ONLY: peak m={peak_m:.8f}, "
        f"gain={peak_gain:.8f} pp"
    )


if __name__ == "__main__":
    main()

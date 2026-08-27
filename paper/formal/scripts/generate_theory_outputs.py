"""Generate formal-paper-only theoretical figures and tables.

These outputs use assumed parameters and are theoretical numerical
illustrations of the model's mechanisms and conjectured shapes.
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import brentq, minimize_scalar  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
FORMAL_DIR = SCRIPT_DIR.parent
REPO_ROOT = FORMAL_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT / "code"))

from discount_model import (  # noqa: E402
    DiscountParams,
    corrected_local_coefficient,
    optimize_flat_noentry,
    optimize_geometry,
    share,
)


ALPHA = 1.0
BETA = 0.8
DELTA = 0.8


def solve_noentry(m: float, alpha: float = ALPHA, beta: float = BETA, delta: float = DELTA):
    par = DiscountParams(m=m, alpha=alpha, beta=beta, gamma=0.0, delta=delta)
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


def concave_completion(p2: float) -> float:
    """Worst-cutoff completion for the paper's F(c)=sqrt(c) example."""
    m, alpha, beta, delta, p1 = 0.5, 0.75, 0.3, 1.0, 0.06
    f = np.sqrt

    def residual(a: float) -> float:
        lam1 = m * alpha * (f(p1) - f(a))
        lam2 = m * alpha * (f(p2) - f(a))
        c1, c2 = -np.expm1(-lam1), -np.expm1(-lam2)
        if abs(c2 - c1) < 1e-12:
            return share(m * f(a)) * (p1 - a)
        switch = (c2 * p2 - c1 * p1) / (beta * (c2 - c1))
        repeat = np.clip((switch - p1 / beta) / (1 - p1), 0, 1)
        rescue = np.clip((1 - switch) / (1 - p1), 0, 1)
        return share(m * f(a)) * (p1 - a) - delta * alpha * np.exp(-m * f(a)) * (
            repeat * share(lam1) * (p1 - a)
            + rescue * share(lam2) * (p2 - a)
        )

    grid = np.linspace(0, p1, 500)
    roots = []
    vals = [residual(float(a)) for a in grid]
    for left, right, fl, fr in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fl == 0:
            roots.append(float(left))
        elif fl * fr < 0:
            roots.append(float(brentq(residual, left, right)))
    if not roots:
        roots = [p1]

    completions = []
    for a in roots:
        lam1 = m * alpha * (f(p1) - f(a))
        lam2 = m * alpha * (f(p2) - f(a))
        c1, c2 = -np.expm1(-lam1), -np.expm1(-lam2)
        if abs(c2 - c1) < 1e-12:
            repeat, rescue = 1.0, 0.0
        else:
            switch = (c2 * p2 - c1 * p1) / (beta * (c2 - c1))
            repeat = np.clip((switch - p1 / beta) / (1 - p1), 0, 1)
            rescue = np.clip((1 - switch) / (1 - p1), 0, 1)
        failure = np.exp(-m * f(a))
        completions.append((1 - p1) * (1 - failure + failure * (repeat * c1 + rescue * c2)))
    return float(min(completions))


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

    # Comparative statics requested for the revision.  Each curve re-solves
    # the equilibrium and both payment choices; these are not fixed-policy
    # counterfactuals.
    sensitivity_m = np.geomspace(0.1, 60.0, 61)
    fig, axes = plt.subplots(1, 3, figsize=(7.15, 2.55), constrained_layout=True)
    for beta, style in ((0.45, ":"), (0.6, "--"), (0.8, "-")):
        gains = [100 * solve_noentry(float(m), beta=beta).gain for m in sensitivity_m]
        axes[0].plot(sensitivity_m, gains, style, linewidth=1.6, label=rf"$\beta={beta:g}$")
    for delta, style in ((0.4, ":"), (0.7, "--"), (1.0, "-")):
        gains = [100 * solve_noentry(float(m), delta=delta).gain for m in sensitivity_m]
        axes[1].plot(sensitivity_m, gains, style, linewidth=1.6, label=rf"$\delta={delta:g}$")
    for alpha, style in ((0.25, ":"), (0.6, "--"), (1.0, "-")):
        gains = [100 * solve_noentry(float(m), alpha=alpha).gain for m in sensitivity_m]
        axes[2].plot(sensitivity_m, gains, style, linewidth=1.6, label=rf"$\alpha={alpha:g}$")
    for ax, title in zip(axes, ("(a) Rider patience", "(b) Driver patience", "(c) Incumbent survival")):
        ax.set_xscale("log")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlabel(r"Thickness $m$")
        ax.set_title(title)
        ax.legend(frameon=False)
        ax.grid(alpha=0.2, linewidth=0.5)
    axes[0].set_ylabel(r"Optimized rescue gain $100V(m)$ (pp)")
    fig.savefig(figure_dir / "theory_sensitivity.pdf", bbox_inches="tight")
    fig.savefig(figure_dir / "theory_sensitivity.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.7), constrained_layout=True)
    p2_grid = np.linspace(0.0601, 0.22, 120)
    flat_concave = (1 - 0.06) * (1 - np.exp(-0.5 * np.sqrt(0.06)))
    concave_gain = 100 * (np.array([concave_completion(float(q)) for q in p2_grid]) - flat_concave)
    axes[0].plot(p2_grid, concave_gain, color=orange, linewidth=1.8)
    axes[0].axhline(0, color="black", linewidth=0.6)
    axes[0].axvline(0.17, color=gray, linestyle=":", linewidth=1)
    axes[0].set_xlabel(r"Rescue payment $p_2$ (fixed $p_1=.06$)")
    axes[0].set_ylabel("Completion change (pp)")
    axes[0].set_title(r"(a) Concave supply: local gain, large-rescue reversal")
    axes[0].grid(alpha=0.2, linewidth=0.5)

    gamma_grid = np.linspace(0, 4, 161)
    beta_grid = np.linspace(0.25, 0.95, 141)
    gg, bb = np.meshgrid(gamma_grid, beta_grid)
    m0, p0, alpha0 = 5.0, 0.2, 0.6
    activity = m0 * np.exp(-gg * m0 * p0) * (alpha0 + gg) * (bb - p0) - (1 - np.exp(-gg * m0 * p0))
    im = axes[1].contourf(gg, bb, activity, levels=[-10, 0, 10], colors=["#e8d9d2", "#d8e6f3"], alpha=0.95)
    axes[1].contour(gg, bb, activity, levels=[0], colors=["black"], linewidths=1.2)
    axes[1].set_xlabel(r"Fresh-entry intensity $\gamma$")
    axes[1].set_ylabel(r"Rider patience $\beta$")
    axes[1].set_title(r"(b) Active marginal rescue region ($\mathcal{A}>0$)")
    axes[1].text(3.0, 0.34, "inactive", color="#6d3a2c", fontsize=8)
    axes[1].text(0.25, 0.83, "active", color=blue, fontsize=8)
    fig.savefig(figure_dir / "boundary_diagnostics.pdf", bbox_inches="tight")
    fig.savefig(figure_dir / "boundary_diagnostics.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # Two-dimensional design maps expose the region where rescue is used and
    # how far the optimal contract departs from flat pricing.
    beta_map = np.linspace(0.25, 0.95, 29)
    delta_map = np.linspace(0.3, 1.0, 29)
    gain_map = np.empty((len(delta_map), len(beta_map)))
    gap_map = np.empty_like(gain_map)
    for i, delta in enumerate(delta_map):
        for j, beta in enumerate(beta_map):
            result = solve_noentry(10.0, beta=float(beta), delta=float(delta))
            gain_map[i, j] = 100 * result.gain
            gap_map[i, j] = result.point.q - result.point.p
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.7), constrained_layout=True)
    extent = [beta_map[0], beta_map[-1], delta_map[0], delta_map[-1]]
    g = axes[0].imshow(gain_map, origin="lower", aspect="auto", extent=extent, cmap="Blues")
    axes[0].contour(beta_map, delta_map, gain_map, levels=[1, 3, 5], colors="black", linewidths=0.6)
    fig.colorbar(g, ax=axes[0], label="Gain (pp)")
    h = axes[1].imshow(gap_map, origin="lower", aspect="auto", extent=extent, cmap="Oranges")
    axes[1].contour(beta_map, delta_map, gap_map, levels=[0.02, 0.08, 0.16], colors="black", linewidths=0.6)
    fig.colorbar(h, ax=axes[1], label=r"$p_2^*-p_1^*$")
    for ax, title in zip(axes, ("(a) Optimized completion gain", "(b) Optimal rescue increment")):
        ax.set_xlabel(r"Rider patience $\beta$")
        ax.set_ylabel(r"Driver patience $\delta$")
        ax.set_title(title)
    fig.savefig(figure_dir / "design_maps.pdf", bbox_inches="tight")
    fig.savefig(figure_dir / "design_maps.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    selected = [(m, solve_noentry(m)) for m in (1.0, 5.0, 10.0, 20.0)]
    write_table(selected, table_dir / "theory_selected_m.tex")
    print(
        f"THEORETICAL ILLUSTRATION ONLY: peak m={peak_m:.8f}, "
        f"gain={peak_gain:.8f} pp"
    )


if __name__ == "__main__":
    main()

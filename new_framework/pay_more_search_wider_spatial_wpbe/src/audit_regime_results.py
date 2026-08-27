"""Deterministic integrity checks for the archived formal regime grid."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "csv" / "regime_comparison.csv"
METADATA = ROOT / "results" / "regime_metadata.json"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    data = pd.read_csv(DATA)
    metadata = json.loads(METADATA.read_text())
    mechanisms = {"incumbent_only", "fixed_arrivals", "expanded_search"}
    keys = ["m", "beta", "delta"]

    _require(len(data) == metadata["row_count"], "row count differs from metadata")
    _require(set(data["mechanism"]) == mechanisms, "mechanism labels are incomplete")
    counts = data.groupby(keys)["mechanism"].nunique()
    _require(bool((counts == 3).all()), "an environment is missing a regime")
    _require(bool(data["certification_stable"].all()), "a final root set is uncertified")
    _require(bool((data["equilibrium_count"] >= 1).all()), "a row has no cutoff-WPBE")
    _require(bool(data["completion"].between(0, 1).all()), "completion leaves [0,1]")
    _require(bool((data["p1"] <= data["p2"] + 1e-10).all()), "p1 exceeds p2")
    _require(bool((data["s"] >= 1 - 1e-10).all()), "search multiplier below one")
    adversarial_seeds = int(metadata["search_config"]["adversarial_seeds"])
    _require(adversarial_seeds >= 1, "formal run lacks adversarial outer search")
    _require(
        bool((data["adversarial_seed_count"] == adversarial_seeds).all()),
        "a row lacks the configured adversarial search",
    )
    _require(
        bool((data["adversarial_evaluations"] > 0).all()),
        "a row reports no adversarial evaluations",
    )
    _require(
        bool((data["adversarial_improvement"] >= -1e-12).all()),
        "adversarial improvement is negative",
    )

    kappa = float(metadata["outer_contact_cost"])
    reconstructed_value = data["completion"] - kappa * data["expected_extra_notifications"]
    _require(
        bool(np.allclose(data["design_value"], reconstructed_value, atol=2e-10)),
        "design value does not equal completion minus outer-contact cost",
    )

    total = (
        data["rescue_incumbent_intensity"]
        + data["rescue_core_fresh_intensity"]
        + data["rescue_outer_fresh_intensity"]
    )
    _require(
        bool(np.allclose(data["rescue_total_intensity"], total, atol=2e-10)),
        "rescue supply components do not add to total intensity",
    )

    incumbent = data[data["mechanism"].eq("incumbent_only")]
    fixed = data[data["mechanism"].eq("fixed_arrivals")]
    expanded = data[data["mechanism"].eq("expanded_search")]
    _require(
        bool(np.allclose(incumbent["rescue_core_fresh_intensity"], 0)),
        "incumbent-only regime contains core fresh supply",
    )
    _require(
        bool(np.allclose(incumbent["rescue_outer_fresh_intensity"], 0)),
        "incumbent-only regime contains outer fresh supply",
    )
    _require(bool(np.allclose(fixed["s"], 1)), "fixed-arrival regime expands search")
    _require(
        bool(np.allclose(fixed["rescue_outer_fresh_intensity"], 0)),
        "fixed-arrival regime contains outer supply",
    )
    _require(
        bool(np.allclose(incumbent["expected_extra_notifications"], 0))
        and bool(np.allclose(fixed["expected_extra_notifications"], 0)),
        "a non-expanded regime pays outer-contact cost",
    )

    expected_outer = (
        (1 - expanded["p1"])
        * np.exp(-expanded["m"] * np.clip(expanded["cutoff"], 0, 1))
        * expanded["rescue_mass"]
        * expanded["m"]
        * (expanded["s"] - 1)
    )
    _require(
        bool(
            np.allclose(
                expanded["expected_extra_notifications"], expected_outer, atol=2e-9
            )
        ),
        "outer-contact accounting does not match execution probability",
    )

    value_pivot = data.pivot_table(index=keys, columns="mechanism", values="design_value")
    gap = value_pivot["expanded_search"] - value_pivot["fixed_arrivals"]
    _require(bool((gap >= -2e-8).all()), "expanded design violates s=1 nesting")

    print(
        json.dumps(
            {
                "rows": len(data),
                "environments": len(counts),
                "all_certified": True,
                "max_equilibrium_count": int(data["equilibrium_count"].max()),
                "minimum_expanded_value_gap": float(gap.min()),
                "maximum_expanded_value_gap": float(gap.max()),
                "adversarial_improvement_count": int(
                    (data["adversarial_improvement"] > 1e-8).sum()
                ),
                "maximum_adversarial_improvement": float(
                    data["adversarial_improvement"].max()
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

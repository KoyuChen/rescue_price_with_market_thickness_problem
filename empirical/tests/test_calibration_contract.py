"""Tests for the empirical schema contract; no observed data are used."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from calibration_contract import synthetic_records, validate_contract  # noqa: E402


class CalibrationContractTests(unittest.TestCase):
    def test_synthetic_topology_contains_both_supply_sources(self) -> None:
        report = validate_contract(*synthetic_records(n_requests=12))
        self.assertEqual(report.requests, 12)
        self.assertEqual(report.announced_requests, 12)
        self.assertGreater(report.universal_rejections, 0)
        self.assertGreater(report.surviving_incumbents, 0)
        self.assertGreater(report.fresh_entrants, 0)

    def test_inconsistent_entrant_flag_is_rejected(self) -> None:
        requests, exposures, states = synthetic_records(n_requests=2)
        second = next(row for row in exposures if row["window"] == 2)
        second["entrant_flag"] = not second["entrant_flag"]
        with self.assertRaisesRegex(ValueError, "entrant_flag inconsistent"):
            validate_contract(requests, exposures, states)

    def test_inconsistent_incumbent_flag_is_rejected(self) -> None:
        requests, exposures, states = synthetic_records(n_requests=2)
        second = next(row for row in exposures if row["window"] == 2)
        second["incumbent_flag"] = not second["incumbent_flag"]
        with self.assertRaisesRegex(ValueError, "incumbent_flag inconsistent"):
            validate_contract(requests, exposures, states)

    def test_second_window_after_first_acceptance_is_rejected(self) -> None:
        requests, exposures, states = synthetic_records(n_requests=2)
        accepted_request = str(requests[0]["request_id"])
        template = next(row for row in exposures if row["window"] == 2).copy()
        template.update(
            {
                "request_id": accepted_request,
                "driver_id": "synthetic-impossible-entrant",
                "incumbent_flag": False,
                "entrant_flag": True,
            }
        )
        exposures.append(template)
        with self.assertRaisesRegex(ValueError, "after first-window acceptance"):
            validate_contract(requests, exposures, states)


if __name__ == "__main__":
    unittest.main()

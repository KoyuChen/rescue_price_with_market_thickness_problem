"""Schema and timing contract for the planned empirical calibration.

This module deliberately contains no observed data and no parameter estimator.
Its synthetic mode validates relational topology, announcement timing, and the
incumbent/entrant classification required by the theoretical model.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import random
from typing import Iterable, Mapping


REQUEST_COLUMNS = {
    "request_id",
    "market_id",
    "request_created_at",
    "first_window_start",
    "first_window_end",
    "second_window_start",
    "second_window_end",
    "p1",
    "p2",
    "p2_announced_at",
    "menu_assignment",
    "rider_action",
    "assigned_driver_id",
    "completed",
    "completion_window",
}

EXPOSURE_COLUMNS = {
    "request_id",
    "driver_id",
    "window",
    "eligible",
    "exposed",
    "payment_shown",
    "exposed_at",
    "response",
    "response_at",
    "selected",
    "incumbent_flag",
    "entrant_flag",
}

SUPPLY_COLUMNS = {
    "request_id",
    "public_thickness_signal",
    "platform_expected_incumbents",
    "platform_realized_eligible",
    "state_generated_at",
}


@dataclass(frozen=True)
class ContractReport:
    requests: int
    exposures: int
    announced_requests: int
    universal_rejections: int
    surviving_incumbents: int
    fresh_entrants: int


def _require_columns(rows: list[Mapping[str, object]], required: set[str], name: str) -> None:
    if not rows:
        raise ValueError(f"{name} is empty")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"{name} is missing columns: {sorted(missing)}")


def validate_contract(
    requests: Iterable[Mapping[str, object]],
    exposures: Iterable[Mapping[str, object]],
    supply_states: Iterable[Mapping[str, object]],
) -> ContractReport:
    req = list(requests)
    exp = list(exposures)
    states = list(supply_states)
    _require_columns(req, REQUEST_COLUMNS, "requests")
    _require_columns(exp, EXPOSURE_COLUMNS, "driver_exposures")
    _require_columns(states, SUPPLY_COLUMNS, "supply_states")

    request_by_id = {str(row["request_id"]): row for row in req}
    if len(request_by_id) != len(req):
        raise ValueError("request_id must be unique in requests")
    state_ids = [str(row["request_id"]) for row in states]
    if len(state_ids) != len(set(state_ids)):
        raise ValueError("request_id must be unique in supply_states")
    if set(state_ids) != set(request_by_id):
        raise ValueError("requests and supply_states must have the same request IDs")

    by_request_window: dict[tuple[str, int], list[Mapping[str, object]]] = defaultdict(list)
    for row in exp:
        request_id = str(row["request_id"])
        if request_id not in request_by_id:
            raise ValueError(f"unknown exposure request_id: {request_id}")
        window = int(row["window"])
        if window not in (1, 2):
            raise ValueError("window must be 1 or 2")
        by_request_window[(request_id, window)].append(row)

    announced = 0
    universal = 0
    survivors = 0
    entrants = 0
    for request_id, row in request_by_id.items():
        if row["p2_announced_at"] <= row["first_window_start"]:
            announced += 1
        first_window = by_request_window[(request_id, 1)]
        first_eligible = [x for x in first_window if x["eligible"]]
        first = [x for x in first_eligible if x["exposed"]]
        if not first:
            raise ValueError(f"request {request_id} has no first-window exposed driver")
        if any(not bool(x["incumbent_flag"]) or bool(x["entrant_flag"]) for x in first_eligible):
            raise ValueError(f"request {request_id} has inconsistent first-window supply flags")
        first_accept = any(x["response"] == "accept" for x in first)
        if not first_accept:
            universal += 1

        first_ids = {str(x["driver_id"]) for x in first_eligible}
        first_response = {str(x["driver_id"]): str(x["response"]) for x in first}
        second = [x for x in by_request_window[(request_id, 2)] if x["eligible"]]
        if first_accept and second:
            raise ValueError(
                f"request {request_id} opens a second window after first-window acceptance"
            )
        if row["rider_action"] in {"no_post", "abandon"} and second:
            raise ValueError(
                f"request {request_id} has second-window supply after rider exit"
            )
        for x in second:
            driver_id = str(x["driver_id"])
            is_entrant = driver_id not in first_ids
            if bool(x["entrant_flag"]) != is_entrant:
                raise ValueError(
                    f"entrant_flag inconsistent for request {request_id}, driver {driver_id}"
                )
            if bool(x["incumbent_flag"]) != (not is_entrant):
                raise ValueError(
                    f"incumbent_flag inconsistent for request {request_id}, driver {driver_id}"
                )
            if is_entrant:
                entrants += 1
            else:
                if first_response.get(driver_id) not in {"reject", "timeout"}:
                    raise ValueError(
                        f"surviving incumbent {driver_id} was not a first-window rejector or timeout"
                    )
                survivors += 1

    return ContractReport(
        requests=len(req),
        exposures=len(exp),
        announced_requests=announced,
        universal_rejections=universal,
        surviving_incumbents=survivors,
        fresh_entrants=entrants,
    )


def synthetic_records(seed: int = 20260827, n_requests: int = 24):
    rng = random.Random(seed)
    origin = datetime(2026, 1, 1, tzinfo=timezone.utc)
    requests: list[dict[str, object]] = []
    exposures: list[dict[str, object]] = []
    states: list[dict[str, object]] = []

    for index in range(n_requests):
        request_id = f"synthetic-{index:04d}"
        start = origin + timedelta(minutes=10 * index)
        end = start + timedelta(minutes=2)
        second_start = end + timedelta(seconds=1)
        second_end = second_start + timedelta(minutes=2)
        p1 = 0.35 + 0.05 * (index % 3)
        p2 = p1 + 0.15
        first_count = 1 + index % 4
        first_ids = [f"driver-{index:04d}-{j}" for j in range(first_count)]
        accepted_first = index % 3 == 0

        requests.append(
            {
                "request_id": request_id,
                "market_id": f"market-{index % 2}",
                "request_created_at": start - timedelta(seconds=5),
                "first_window_start": start,
                "first_window_end": end,
                "second_window_start": second_start,
                "second_window_end": second_end,
                "p1": p1,
                "p2": p2,
                "p2_announced_at": start - timedelta(seconds=30),
                "menu_assignment": "synthetic_announced",
                "rider_action": "repeat" if accepted_first else "rescue",
                "assigned_driver_id": first_ids[0] if accepted_first else "",
                "completed": accepted_first,
                "completion_window": "first" if accepted_first else "none",
            }
        )
        states.append(
            {
                "request_id": request_id,
                "public_thickness_signal": float(first_count),
                "platform_expected_incumbents": float(first_count),
                "platform_realized_eligible": first_count,
                "state_generated_at": start - timedelta(minutes=1),
            }
        )
        for j, driver_id in enumerate(first_ids):
            response = "accept" if accepted_first and j == 0 else "reject"
            exposures.append(
                {
                    "request_id": request_id,
                    "driver_id": driver_id,
                    "window": 1,
                    "eligible": True,
                    "exposed": True,
                    "payment_shown": p1,
                    "exposed_at": start,
                    "response": response,
                    "response_at": start + timedelta(seconds=10 + j),
                    "selected": response == "accept",
                    "incumbent_flag": True,
                    "entrant_flag": False,
                }
            )
        if not accepted_first:
            surviving = first_ids[: max(1, first_count - 1)]
            entrant_ids = [f"entrant-{index:04d}-{j}" for j in range(1 + index % 2)]
            for driver_id in surviving + entrant_ids:
                entrant = driver_id in entrant_ids
                response = "accept" if rng.random() < 0.5 else "reject"
                exposures.append(
                    {
                        "request_id": request_id,
                        "driver_id": driver_id,
                        "window": 2,
                        "eligible": True,
                        "exposed": True,
                        "payment_shown": p2,
                        "exposed_at": second_start,
                        "response": response,
                        "response_at": second_start + timedelta(seconds=10),
                        "selected": False,
                        "incumbent_flag": not entrant,
                        "entrant_flag": entrant,
                    }
                )
    return requests, exposures, states


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()
    if not args.synthetic:
        raise SystemExit("DATA REQUIRED: only --synthetic schema validation is available")
    report = validate_contract(*synthetic_records())
    print("SYNTHETIC SCHEMA ONLY")
    print(report)


if __name__ == "__main__":
    main()

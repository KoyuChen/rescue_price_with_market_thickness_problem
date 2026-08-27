# Required empirical data dictionary

All timestamps must use one documented timezone and a common resolution. Empty
strings are missing values, not zeros.

## `requests.csv`

| Column | Type | Definition |
|---|---|---|
| `request_id` | string | Stable request identifier. |
| `market_id` | string | Market or operational cell. |
| `request_created_at` | timestamp | Request creation time. |
| `first_window_start` | timestamp | Start of first response window. |
| `first_window_end` | timestamp | End of first response window. |
| `second_window_start` | timestamp | Start of continuation window; missing if no continuation. |
| `second_window_end` | timestamp | End of continuation window. |
| `p1` | numeric | Initial payment shown before first-window decisions. |
| `p2` | numeric | Failure-contingent rescue payment. |
| `p2_announced_at` | timestamp | Time at which the exact `p2` became visible and credible. |
| `menu_assignment` | string | Randomized arm, policy rule, or observational assignment label. |
| `rider_action` | category | `no_post`, `abandon`, `repeat`, or `rescue`. |
| `assigned_driver_id` | string | Selected driver, if any. |
| `completed` | boolean | Physical request completion. |
| `completion_window` | category | `none`, `first`, or `second`. |

An announced-menu observation requires
`p2_announced_at <= first_window_start`. Otherwise it belongs to a surprise or
unannounced-rescue benchmark.

## `driver_exposures.csv`

| Column | Type | Definition |
|---|---|---|
| `request_id` | string | Foreign key to `requests.csv`. |
| `driver_id` | string | Persistent driver identifier. |
| `window` | integer | `1` or `2`. |
| `eligible` | boolean | Driver could receive the request in this window. |
| `exposed` | boolean | Driver was actually shown the request and active payment. |
| `payment_shown` | numeric | Payment visible to this driver. |
| `exposed_at` | timestamp | Exposure time. |
| `response` | category | `accept`, `reject`, `timeout`, or `not_seen`. |
| `response_at` | timestamp | Response timestamp, if recorded. |
| `selected` | boolean | Driver was selected conditional on acceptance. |
| `incumbent_flag` | boolean | Driver was exposed in window 1. |
| `entrant_flag` | boolean | Driver first becomes eligible in window 2. |

A surviving incumbent is a window-1 rejector or timeout who remains eligible
in window 2. A fresh entrant is eligible in window 2 and absent from the
window-1 eligible set. The analysis must report how timeouts and `not_seen`
events are treated rather than silently classifying them as rejection.

## `supply_states.csv`

| Column | Type | Definition |
|---|---|---|
| `request_id` | string | Foreign key to `requests.csv`. |
| `public_thickness_signal` | numeric | Pre-decision supply state visible to drivers and rider, if any. |
| `platform_expected_incumbents` | numeric | Logged expected eligible incumbent count. |
| `platform_realized_eligible` | integer | Platform-side realized eligible count, retained as a measurement input rather than equated with public `m`. |
| `state_generated_at` | timestamp | Time at which the state was formed. |

Expected thickness `m` is not the realized count `N_I`. If only a private
platform forecast exists, the theoretical information structure must be
modified or the forecast treated as an econometric proxy rather than a public
primitive.

## Minimum derived outcomes

- first-window exposure count;
- first-window acceptance and universal rejection;
- incumbent survival and fresh-entry counts;
- rider abandon, repeat, and rescue shares after failure;
- terminal acceptance and completion;
- observed-versus-predicted moments by thickness and menu cells.

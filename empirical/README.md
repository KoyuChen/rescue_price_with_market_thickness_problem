# Empirical calibration package

**Status: DATA REQUIRED.** This directory is a pre-specified empirical
contract for the formal manuscript. It contains no observed data and produces
no empirical estimate in its current state.

The theoretical model can be called calibrated only after the following gates
are documented:

1. both `p1` and the failure-contingent `p2` were displayed and credibly
   committed before first-window driver decisions;
2. the initial eligible and exposed driver sets can be reconstructed, so
   universal rejection is distinguishable from zero exposure;
3. persistent driver identifiers separate surviving incumbents from fresh
   second-window entrants;
4. a public pre-decision thickness signal or a defensible measurement model for
   expected thickness is available;
5. rider abandon, repeat, and rescue decisions are recorded;
6. menu assignment is randomized, instrumented, or modeled transparently.

If the available experiment randomizes only the contemporaneous payment, it
may discipline a flat or no-anticipation benchmark. It cannot identify the
strategic anticipation parameter or validate announced rescue.

## Expected restricted inputs

Raw data belong under `empirical/data/`, which is excluded from Git.

- `requests.csv`: request policy, rider events, assignment, and completion;
- `driver_exposures.csv`: one row per request-driver-window exposure;
- `supply_states.csv`: public pre-decision market state and logged eligible
  supply measures;
- `experiment_protocol.md`: what each side observed and when;
- `source_data_dictionary.md`: certified source-field definitions.

The exact required columns and timing restrictions appear in
`data_dictionary.md`. Run the schema-only smoke test with:

```bash
python -m unittest discover -s empirical/tests -p 'test_*.py' -v
python empirical/src/calibration_contract.py --synthetic
```

The synthetic mode validates topology and timing only. It must never be cited
as empirical calibration, model fit, or evidence for strategic waiting.

## Planned estimation order

1. construct request, exposure, continuation, and supply-state moments;
2. classify every primitive as measured, estimated, calibrated, or fixed for
   sensitivity;
3. solve all cutoff-WPBE roots inside each candidate parameter evaluation;
4. match pre-declared moments using the criterion in the manuscript;
5. reserve untargeted moments or markets for validation;
6. re-estimate within each bootstrap draw before optimizing policies;
7. generate disclosure-safe aggregate tables and figures from code.

The initial implementation maintains the formal model's common primitive
driver-cost distribution (F). Allowing different primitive distributions
for incumbents and entrants is a robustness extension that requires a new
equilibrium derivation and solver; it is not part of the baseline estimator.

No number should be typed manually into the formal manuscript.

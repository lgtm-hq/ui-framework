# V1 Baseline Benchmarks

Use this document to capture the baseline run metrics for v1 signoff.

## Baseline Run Metadata

| Field | Value |
|---|---|
| Date | 2026-02-09 |
| Domain | `debs-obrien.github.io` |
| Environment | `baseline` |
| Run directory | `reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08` |
| Command used | `uv run flowscout explore https://debs-obrien.github.io/playwright-movies-app --smart --generate-tests --max-depth 2 --max-states 20 --max-actions 20 --environment baseline` |
| Commit SHA | `39487e4` |

## Commands Used

```bash
uv run flowscout explore https://debs-obrien.github.io/playwright-movies-app --smart --generate-tests --max-depth 2 --max-states 20 --max-actions 20 --environment baseline
uv run flowscout benchmark reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.50.08/result.json
uv run flowscout reliability --url https://debs-obrien.github.io/playwright-movies-app
uv run pytest --cov=flowscout --cov-report=term-missing
```

## Captured Metrics

| Metric | Target | Actual | Source |
|---|---|---|---|
| Runtime duration (seconds) | <= 1800 | 1.97 | `flowscout benchmark` |
| States discovered | n/a | 2 | `flowscout benchmark` |
| Actions executed | n/a | 1 | `flowscout benchmark` |
| Coverage percent | >= 80% | 100% page coverage (17% action coverage) | `flowscout benchmark` |
| Low-confidence transitions | trend down | 1 (<0.60 threshold) | `flowscout benchmark` |
| Flaky action count | trend down | 0 (for this URL in current DB history) | `flowscout benchmark` + `flowscout reliability` |
| Generated tests created | > 0 | Yes (`tests.py`, `pom_tests.py`, `scenario_tests.py`) | run directory artifacts |
| Generated test pass rate | >= baseline target | 362/362 framework tests passed (generated suites not executed yet) | `uv run pytest --cov=flowscout --cov-report=term-missing` |

## Notes on Collection

1. Always benchmark with the same domain and environment label.
2. Keep non-destructive mode enabled unless an approved exception is documented.
3. Attach run artifact paths and a short summary of anomalies.

## Findings and Follow-ups

- Reliability hotspots: one `no_change` transition on search form click with confidence `0.55`.
- Coverage gaps: state/action depth was intentionally shallow (`max-depth=2`, `max-states=20`); navigation edge discovery was limited.
- Selector instability: search interaction currently relies on a brittle container selector in this baseline run.
- Actions for next iteration:
  1. Increase exploration limits (`max-depth`, `max-states`, `max-actions`) for fuller path coverage.
  2. Add explicit auth/navigation bootstrap rules where needed.
  3. Re-run baseline and compare low-confidence count plus flaky-action trend.

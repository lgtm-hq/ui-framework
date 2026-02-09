# V1 Baseline Benchmarks

Use this document to capture the baseline run metrics for v1 signoff.

## Baseline Run Metadata

| Field | Value |
|---|---|
| Date | 2026-02-09 |
| Domain | `debs-obrien.github.io` |
| Environment | `baseline` |
| Run directory | `reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18` |
| Command used | `uv run flowscout explore https://debs-obrien.github.io/playwright-movies-app --smart --generate-tests --max-depth 2 --max-states 20 --max-actions 20 --environment baseline` |
| Commit SHA | `8d02ee4` |

## Commands Used

```bash
uv run flowscout explore https://debs-obrien.github.io/playwright-movies-app --smart --generate-tests --max-depth 2 --max-states 20 --max-actions 20 --environment baseline
uv run flowscout benchmark reports/debs-obrien.github.io/baseline/runs/2026-02-09_09.52.18/result.json
uv run flowscout reliability --url https://debs-obrien.github.io/playwright-movies-app
uv run pytest --cov=flowscout --cov-report=term-missing
```

## Captured Metrics

| Metric | Target | Actual | Source |
|---|---|---|---|
| Runtime duration (seconds) | <= 1800 | 38.87 | `flowscout benchmark` |
| States discovered | n/a | 20 | `flowscout benchmark` |
| Actions executed | n/a | 22 | `flowscout benchmark` |
| Coverage percent | >= 80% | 100% page coverage (36% action coverage) | `flowscout benchmark` |
| Low-confidence transitions | trend down | 1 (<0.60 threshold) | `flowscout benchmark` |
| Flaky action count | trend down | 1 | `flowscout benchmark` + `flowscout reliability` |
| Generated tests created | > 0 | Yes (`tests.py`, `pom_tests.py`, `scenario_tests.py`) | run directory artifacts |
| Generated test pass rate | >= baseline target | 362/362 framework tests passed (generated suites not executed yet) | `uv run pytest --cov=flowscout --cov-report=term-missing` |

## Reliability Trend Review (Repeated Runs)

| Run | Duration (s) | States | Actions | Action Coverage | Avg Confidence | Low Confidence Count | Flaky Count |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2026-02-09_09.50.08` | 1.97 | 2 | 1 | 17% | 0.550 | 1 | 0 |
| `2026-02-09_09.52.18` | 38.87 | 20 | 22 | 36% | 0.927 | 1 | 1 |

Trend summary:

- Exploration depth increased run-to-run (states: `2 -> 20`, actions: `1 -> 22`).
- Confidence improved significantly (`0.550 -> 0.927`) while low-confidence count stayed at `1`.
- One flaky action is now identified: click on the search form container produced both `no_change` and `navigation` outcomes across runs.
- Most navigation selectors remained stable (high repeat navigation success across repeated card clicks).

## Notes on Collection

1. Always benchmark with the same domain and environment label.
2. Keep non-destructive mode enabled unless an approved exception is documented.
3. Attach run artifact paths and a short summary of anomalies.

## Risks and Mitigations for Handoff

- Risk: flaky search-form click transition (`no_change` vs `navigation`).
  Mitigation: prioritize explicit search input/submit selectors and enforce post-click signal checks.
- Risk: action coverage still below desired breadth for deep MBT generation.
  Mitigation: increase `max-depth`, `max-states`, and `max-actions` for release-candidate runs.
- Risk: generated suites are created but not yet executed as standalone artifacts.
  Mitigation: add a smoke stage that executes generated `tests.py`/`scenario_tests.py` against the baseline target.

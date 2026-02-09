# V1 Baseline Benchmarks

Use this document to capture the baseline run metrics for v1 signoff.

## Baseline Run Metadata

| Field | Value |
|---|---|
| Date | |
| Domain | |
| Environment | |
| Run directory | |
| Command used | |
| Commit SHA | |

## Commands Used

```bash
uv run flowscout explore <url> --smart --generate-tests --environment <env>
uv run flowscout reliability --url <url>
uv run pytest --cov=flowscout --cov-report=term-missing
```

## Captured Metrics

| Metric | Target | Actual | Source |
|---|---|---|---|
| Runtime duration (seconds) | <= 1800 | | `result.json` -> `duration_seconds` |
| States discovered | n/a | | `result.json` -> `stats.total_states` |
| Actions executed | n/a | | `result.json` -> `stats.total_actions_executed` |
| Coverage percent | >= 80% | | `result.json` -> `coverage` block |
| Low-confidence transitions | trend down | | generated tests + reliability output |
| Flaky action count | trend down | | `flowscout reliability` |
| Generated tests created | > 0 | | run directory artifacts |
| Generated test pass rate | >= baseline target | | local test execution |

## Notes on Collection

1. Always benchmark with the same domain and environment label.
2. Keep non-destructive mode enabled unless an approved exception is documented.
3. Attach run artifact paths and a short summary of anomalies.

## Findings and Follow-ups

- Reliability hotspots:
- Coverage gaps:
- Selector instability:
- Actions for next iteration:

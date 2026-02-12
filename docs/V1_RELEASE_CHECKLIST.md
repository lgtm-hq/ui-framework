# V1 Release Checklist

Use this checklist to gate deterministic, local-first V1 readiness.

Status snapshot date: 2026-02-09

## M1: Safety and Config Foundation

- [x] Non-destructive policy enabled by default.
- [x] Risky action blocking verified on fixture site.
- [x] Input profiles (`safe`, `contextual`, `negative`) documented and validated.
- [x] Auth configuration references secrets without storing secret values.

## M2: Reliable State Identity

- [x] Layered state keys persisted (`route_key`, `view_key`, `context_key`).
- [x] Query normalization and allow/ignore behavior validated.
- [x] Dynamic context markers (tab/modal/step/form) produce intended state boundaries.
- [x] Regression tests pass for duplicate/noisy URL cases.

## M3: Evidence Integrity

- [x] Screenshot capture is on by default.
- [x] Interacted element highlight appears in action evidence.
- [x] Evidence links to action/state/outcome identifiers.
- [x] Report and JSON artifacts remain consistent for the same run.

## M4: Coverage and MBT Readiness

- [x] Coverage metrics exported in artifacts and surfaced in reports.
- [x] Target threshold is enforced (default: 80%).
- [x] Critical and edge-case scenarios are synthesized in site model output.
- [x] Scenario generation tests pass.

## M5: Generation Quality and Reliability

- [x] Generated POM files compile and import correctly.
- [x] Generated scenario/flow suites are syntactically valid and runnable.
- [x] Low-confidence transitions are explicitly flagged in generated tests.
- [x] Generated steps include traceability identifiers back to source graph edges.

## M6: Release Candidate

- [x] Setup and operations docs are current (`README`, `OPERATIONS_AND_WORKFLOWS`).
- [x] Baseline benchmark template populated (`V1_BASELINE_BENCHMARKS.md`).
- [x] Baseline benchmark run captured:
  - [x] runtime duration
  - [x] coverage percentage
  - [x] low-confidence transition count
  - [x] generated-test pass rate
- [x] Reliability trend reviewed over repeated runs on same target.
- [x] Known risks and mitigations documented for v1 handoff.

## Validation Command Matrix

Core validation commands:

```bash
uv run pytest --cov=flowscout --cov-report=term-missing
uv run flowscout explore https://example.com --smart --generate-tests
uv run flowscout reliability --url https://example.com
```

Optional full lint gate (may include repo-wide pre-existing issues):

```bash
uvx lintro chk
uvx lintro tst
```

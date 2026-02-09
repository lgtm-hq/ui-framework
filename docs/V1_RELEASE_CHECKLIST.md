# V1 Release Checklist

Use this checklist to gate deterministic, local-first V1 readiness.

## M1: Safety and Config Foundation

- [ ] Non-destructive policy enabled by default.
- [ ] Risky action blocking verified on fixture site.
- [ ] Input profiles (`safe`, `contextual`, `negative`) documented and validated.
- [ ] Auth configuration references secrets without storing secret values.

## M2: Reliable State Identity

- [ ] Layered state keys persisted (`route_key`, `view_key`, `context_key`).
- [ ] Query normalization and allow/ignore behavior validated.
- [ ] Dynamic context markers (tab/modal/step/form) produce intended state boundaries.
- [ ] Regression tests pass for duplicate/noisy URL cases.

## M3: Evidence Integrity

- [ ] Screenshot capture is on by default.
- [ ] Interacted element highlight appears in action evidence.
- [ ] Evidence links to action/state/outcome identifiers.
- [ ] Report and JSON artifacts remain consistent for the same run.

## M4: Coverage and MBT Readiness

- [ ] Coverage metrics exported in artifacts and surfaced in reports.
- [ ] Target threshold is enforced (default: 80%).
- [ ] Critical and edge-case scenarios are synthesized in site model output.
- [ ] Scenario generation tests pass.

## M5: Generation Quality and Reliability

- [ ] Generated POM files compile and import correctly.
- [ ] Generated scenario/flow suites are syntactically valid and runnable.
- [ ] Low-confidence transitions are explicitly flagged in generated tests.
- [ ] Generated steps include traceability identifiers back to source graph edges.

## M6: Release Candidate

- [ ] Setup and operations docs are current (`README`, `OPERATIONS_AND_WORKFLOWS`).
- [ ] Baseline benchmark run captured:
  - [ ] runtime duration
  - [ ] coverage percentage
  - [ ] low-confidence transition count
  - [ ] generated-test pass rate
- [ ] Reliability trend reviewed over repeated runs on same target.
- [ ] Known risks and mitigations documented for v1 handoff.

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

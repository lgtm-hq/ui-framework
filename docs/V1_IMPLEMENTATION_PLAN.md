# V1 Implementation Plan

This plan translates product decisions into concrete engineering work for a deterministic, local-first release.

Related documents:

- `PURPOSE_AND_SCOPE.md`
- `ARCHITECTURE_AND_DATA_MODEL.md`
- `V1_PRODUCT_DECISIONS.md`

## 1) V1 Scope Baseline

V1 is complete when a new site can be explored in about 30 minutes and the run produces:

- a reliable state/transition model,
- generated POM + runnable tests,
- human-readable report + machine-level artifacts,
- screenshot evidence by default with interacted-element highlighting,
- repeatable results with run-to-run reliability metrics.

## 2) Non-Negotiable Guardrails

- deterministic runtime behavior only (no AI in crawl/classification/generation),
- non-destructive interaction policy by default,
- secrets-safe handling for auth and evidence,
- per-domain and per-environment output isolation,
- measurable coverage target: at least 80% exploration completeness for in-scope apps.

## 3) Architecture Tracks (Parallel Workstreams)

Implement V1 across six tracks to keep delivery incremental and testable.

### Track A: Policy, Config, and Safety

Goal: centralize risk controls and runtime defaults.

Deliverables:

- policy model for action allow/deny rules,
- query-parameter keep/ignore rules for state identity,
- input profile selector (`safe`, `contextual`, `negative`),
- environment credential references (variable names, secret paths) without secret persistence.

Primary modules:

- `src/flowscout/core/state.py`
- `src/flowscout/cli.py`
- `src/flowscout/discovery/inputs.py`

### Track B: State Identity and Traversal Reliability

Goal: improve model fidelity and reduce duplicate/noisy states.

Deliverables:

- layered state identity (`route_key`, `view_key`, `context_key`),
- normalized route derivation and query allowlist enforcement,
- dynamic-UI stability handling (signal waits + controlled retry),
- transition confidence scoring from repeated attempts/runs.

Primary modules:

- `src/flowscout/core/state.py`
- `src/flowscout/core/browser.py`
- `src/flowscout/core/navigator.py`
- `src/flowscout/analysis/detector.py`

### Track C: Evidence and Traceability

Goal: make outputs audit-friendly for QA/SDET/Dev use.

Deliverables:

- screenshot capture on by default,
- per-action element highlight overlay (bounding box),
- metadata link: screenshot <-> action ID <-> state ID <-> outcome code,
- reason-code standardization for outcome reporting.

Primary modules:

- `src/flowscout/core/browser.py`
- `src/flowscout/reporting/html.py`
- `src/flowscout/reporting/templates/report.html.j2`
- `src/flowscout/analysis/detector.py`

### Track D: Coverage and Scenario Quality

Goal: enforce meaningful exploration instead of raw click counts.

Deliverables:

- coverage calculator aligned to V1 target (80%),
- element/path/edge/scenario coverage breakdown,
- critical-journey and edge-case weighting for MBT planning.

Primary modules:

- `src/flowscout/smart/coverage.py`
- `src/flowscout/smart/planner.py`
- `src/flowscout/smart/scenarios.py`

### Track E: Generated Assets (POM + Tests)

Goal: ensure generated artifacts are runnable and maintainable.

Deliverables:

- stable page-object generation per page type,
- scenario-first generated suites with traceability comments/IDs,
- explicit flags for low-confidence/flaky transitions in generated tests.

Primary modules:

- `src/flowscout/codegen/page_objects.py`
- `src/flowscout/codegen/pom_tests.py`
- `src/flowscout/codegen/scenario_tests.py`
- `src/flowscout/codegen/playwright_tests.py`

### Track F: Storage, Isolation, and Historical Reliability

Goal: preserve clean multi-site history and detect drift/flakiness.

Deliverables:

- domain/env/timestamp output structure,
- run-level and transition-level reliability aggregates,
- exportable history snapshots with confidence annotations.

Primary modules:

- `src/flowscout/storage/db.py`
- `src/flowscout/cli.py`

## 4) Milestones and Exit Criteria

## M1: Safety and Config Foundation

Exit criteria:

- policy defaults enforce non-destructive behavior,
- config supports query allowlist/blocklist and input profile selection,
- auth config references environment secrets without persisting secret values.

Validation:

- unit tests for policy decisions and config parsing,
- integration test proving destructive actions are skipped by default.

## M2: Reliable State Identity

Exit criteria:

- layered identity implemented and persisted in artifacts,
- query noise no longer creates duplicate states,
- context changes (tab/modal/step) create intentional distinct states.

Validation:

- unit tests for identity normalization and hash stability,
- regression test on a dynamic site fixture.

## M3: Evidence Integrity

Exit criteria:

- screenshots enabled by default,
- each recorded action has an evidence image with highlighted target,
- report and JSON artifacts cross-reference action/state/outcome IDs.

Validation:

- integration test asserting screenshot artifact count and metadata links,
- visual spot checks on sample runs.

## M4: Coverage and MBT Readiness

Exit criteria:

- coverage metrics visible in report and result artifacts,
- critical journey and edge-case scenario synthesis implemented,
- run passes configured threshold check (default target 80%).

Validation:

- unit tests for metric calculations,
- end-to-end run verifies threshold reporting behavior.

## M5: Generation Quality and Reliability Signals

Exit criteria:

- generated POM + scenario tests run successfully on baseline fixture site,
- low-confidence transitions explicitly marked in output,
- traceability from generated test step back to graph edge exists.

Validation:

- codegen golden-file tests,
- smoke execution of generated suites.

## M6: V1 Release Candidate

Exit criteria:

- docs updated for setup, operations, and troubleshooting,
- baseline benchmarks captured (runtime, coverage, reliability),
- V1 checklist signed off for deterministic local-first scope.

Validation:

- full test pass,
- lint pass,
- sample-run artifact review against V1 definition.

## 5) Recommended Execution Sequence (First 6 Weeks)

Week 1:

- M1 baseline policy/config,
- initial tests for non-destructive guardrails.

Week 2:

- M2 state identity + query normalization,
- regression tests for noisy URLs and UI contexts.

Week 3:

- M3 evidence highlighting and metadata linkage,
- report updates for evidence traceability.

Week 4:

- M4 coverage model and threshold reporting,
- scenario weighting for business-critical and edge-case flows.

Week 5:

- M5 codegen reliability flags and traceability wiring,
- generated test execution hardening.

Week 6:

- M6 stabilization, docs polish, performance pass, release checklist.

## 6) Metrics and Quality Gates

Track these per run and over time:

- exploration coverage percent (target >= 80%),
- action outcome distribution (`success`, `no_change`, `validation_error`, `execution_error`),
- transition confidence ratio,
- flaky-edge count across repeated runs,
- generated-test pass rate on baseline sites,
- runtime duration and states/actions explored.

Quality gate to merge major features:

- tests green,
- no regression in non-destructive policy behavior,
- artifact schema compatibility maintained.

## 7) Risks and Mitigations

Risk: dynamic/SPA timing causes false `no_change` outcomes.  
Mitigation: signal-based waits, one controlled retry, confidence scoring.

Risk: selector instability in generated assets.  
Mitigation: selector ranking strategy + fallback and confidence labeling.

Risk: evidence volume growth.  
Mitigation: configurable retention/compression and per-run caps.

Risk: sensitive data leakage in artifacts.  
Mitigation: redaction hooks and strict secret handling policy.

## 8) Immediate Kickoff Backlog (Top Priority Tickets)

1. Add policy config schema for non-destructive action controls.
2. Implement query parameter allowlist/blocklist normalization in state identity.
3. Add input profile switch with `safe` default.
4. Add screenshot-on-by-default and per-action target highlight overlay.
5. Extend result artifact schema with coverage and confidence fields.
6. Add transition confidence computation and persistence.
7. Add report panels for coverage, reliability, and evidence traceability.
8. Add integration tests for guardrails, identity stability, and evidence links.

## 9) Definition of Done for V1

V1 is done when:

- deterministic local-only execution is stable on representative test sites,
- outputs are trusted by QA/SDET/Dev stakeholders,
- coverage reaches configured threshold for target environments,
- generated assets run with clear traceability and reliability signals,
- documentation is complete enough to continue roadmap work without context loss.

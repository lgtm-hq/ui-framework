# Architecture and Data Model

For V1-specific defaults and policy decisions (state identity rules, input profiles, evidence defaults, coverage targets), see `V1_PRODUCT_DECISIONS.md`.

## High-Level Pipeline

1. Crawl starts from `start_url`.
2. DOM inspection discovers click and submit actions.
3. Action execution produces transitions.
4. State fingerprints identify unique pages/screens.
5. Transition outcomes are classified.
6. Graph artifacts are written.
7. Test cases are generated from graph structure.
8. Run is persisted to SQLite history.

## Core Concepts

## State

A state is a unique page/screen signature composed of:

- URL
- page title
- visible DOM signals

The framework generates a compact `state_id` from this fingerprint.

V1 layered identity is also captured per state:

- `route_key`: normalized URL route with dynamic IDs collapsed (for example `/products/{id}`)
- `view_key`: hash of route + DOM structure + primary heading
- `context_key`: hash of view + context markers (active nav/tab/modal/step and form state marker)

## Action

An action is an executable interaction:

- `click`
- `submit_form` (with deterministic scenario values)

Actions have labels, selectors, metadata, and stable IDs.

## Action Policy (V1)

V1 adds a non-destructive action policy layer before execution:

- blocks `submit_form` actions by default,
- blocks high-impact actions matched by risky keywords (`delete`, `checkout`, `purchase`, etc.),
- supports allowlisting by selector or label pattern for controlled environments.

This policy is configured via `ExplorerConfig.action_policy`.

## Edge (Transition)

An edge links:

- source state
- action
- target state
- outcome
- confidence score + reason
- details/evidence

Outcomes:

- `success`
- `no_change`
- `validation_error`
- `execution_error`

## Test Case

Generated test cases are derived from edges:

- positive cases from successful paths
- negative cases from non-success outcomes
- reliability annotations per step with confidence score + reason
- explicit `LOW_CONFIDENCE` flag in generated code when confidence is below the V1 threshold (0.60)

Each case keeps:

- start/end states
- readable steps
- action IDs
- edge signatures for traceability

## Persistence Model (SQLite)

Tables:

- `runs`
- `states`
- `actions`
- `edges`
- `transition_facts`

`transition_facts` aggregates repeated transitions across runs so you can identify stable paths, drift, and regressions.

## Artifacts

Per crawl output directory:

- `flow_report.md`
- `flow_report.html`
- `flow_graph.json`
- `flow_bundle.json`
- `test_cases.json`
- `test_cases.md`

History export:

- `history_snapshot.json` via `ui-flow history`

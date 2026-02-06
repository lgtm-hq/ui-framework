# Architecture and Data Model

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

## Action

An action is an executable interaction:

- `click`
- `submit_form` (with deterministic scenario values)

Actions have labels, selectors, metadata, and stable IDs.

## Edge (Transition)

An edge links:

- source state
- action
- target state
- outcome
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

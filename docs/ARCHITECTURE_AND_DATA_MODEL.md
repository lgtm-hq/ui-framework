# Architecture and Data Model

For V1-specific defaults and policy decisions (state identity rules,
input profiles, evidence defaults, coverage targets),
see `V1_PRODUCT_DECISIONS.md`.

## High-Level Pipeline

1. Crawl starts from `start_url`.
2. DOM inspection discovers click and submit actions.
3. Action execution produces transitions.
4. State fingerprints identify unique pages/screens.
5. Transition outcomes are classified.
6. Graph and trace artifacts are written.
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

- `navigation`
- `dom_change`
- `visual_change`
- `no_change`
- `validation_error`
- `network_error`
- `console_error`
- `timeout`
- `exception`

## Test Case

Generated test cases are derived from edges:

- positive cases from successful paths
- negative cases from non-success outcomes
- reliability annotations per step with confidence score + reason
- explicit `LOW_CONFIDENCE` flag in generated code when confidence is below the V1 threshold (0.60)
- explicit per-step trace comments (`action_id`, `source_state -> target_state`, `outcome`) for graph-to-test mapping

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
- `results`
- `flows`

## Artifacts

Per crawl output directory:

- `report.html`
- `result.json`
- `crawl_trace.json` (ordered machine-readable step trace sidecar)
- `evidence/actions/*.png` (when screenshots are enabled)
- `tests.py` (when test generation is enabled)
- `site_model.json` (smart mode)
- `pom_tests.py` (smart mode test generation)
- `tests.feature` / `narrative_report.md` (optional generation modes)

Per site workspace (outside run directory):

- `pages/*.py` (smart mode page objects)
- `scenario_tests.py` (smart mode scenario test generation)

History export:

- terminal table via `flowscout history`

## Human-First Report and Machine Artifacts

Flowscout intentionally separates what humans read from what machines consume.

- `report.html` is optimized for human review.
- `result.json`, `site_model.json`, `crawl_trace.json`, and GraphWalker exports are machine contracts.
- Machine identifiers remain available in machine artifacts for traceability.

### UI policy: no visible machine IDs

The dashboard/report UI must not render raw machine IDs in visible text, including:

- state IDs,
- action IDs,
- database-like internal identifiers.

Technical traceability remains available via machine artifacts and structured `data-*`
hooks used by scripts, without exposing internal IDs in visible UI copy.

### `crawl_trace.json` sidecar contract

`crawl_trace.json` is written beside `report.html` and is stable for MBT consumers.

Top-level keys:

- `schema_version`
- `result_schema_version`
- `generated_at`
- `summary`
- `config`
- `states`
- `actions`
- `steps`

Step-level fields include ordered execution metadata:

- `index`
- `action_id`
- `source_state_id`
- `target_state_id`
- `outcome`
- `result` (full `ActionResult` payload)
- `source_state` and `target_state` compact references
- `action` metadata when available

### GraphWalker compatibility boundary

GraphWalker export behavior remains unchanged and continues to be generated from
the canonical site model (`site_model.json` / `*.graphwalker.json`). The new
`crawl_trace.json` sidecar complements this by preserving concrete crawl order
for timeline-style MBT consumers.

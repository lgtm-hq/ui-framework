# Operations and Workflows

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Run a Crawl

```bash
uv run ui-flow crawl \
  --url "https://example.com" \
  --max-depth 2 \
  --max-states 30 \
  --max-actions-per-state 15 \
  --db-path .ui_flow/history.db \
  --output-dir reports
```

## Run via `just`

```bash
just crawl https://example.com
```

This command loads defaults from `.crawl-config` and runs `ui-flow crawl`.

## `.crawl-config` Runtime Defaults

- File: `.crawl-config` (TOML format)
- Applied at runtime for `ui-flow crawl`
- CLI flags always override config values

Useful keys:

- `max_depth`
- `max_states`
- `max_actions_per_state`
- `navigation_timeout_ms`
- `action_timeout_ms`
- `headless`
- `capture_screenshots`
- `persist_history`
- `output_dir`
- `db_path`
- `screenshots_dir`
- `username`
- `password`

## Traversal Guardrails

- `max-depth`: how many action hops from the start page.
- `max-states`: cap for unique discovered states.
- `max-actions-per-state`: cap for actions attempted per state.

These parameters bound runtime while preserving useful coverage.

## Non-Destructive Policy Controls

For `flowscout explore`, non-destructive mode is on by default.

- `--enforce-non-destructive` keeps high-impact action blocking enabled.
- `--allow-form-submits` allows submit actions when you are in a safe test environment.
- `--screenshot` is enabled by default and captures per-action evidence with target highlighting.

Use `--no-enforce-non-destructive` only in tightly controlled environments.

## Export History Snapshot

```bash
uv run ui-flow history \
  --db-path .ui_flow/history.db \
  --url "https://example.com" \
  --output reports/history_snapshot.json
```

## Run Without DB Persistence

```bash
uv run ui-flow crawl \
  --url "https://example.com" \
  --no-persist-history
```

## Explore Results in Report UI

```bash
cd report-ui
bun install
bun run dev
```

Then load `reports/flow_bundle.json`, or place it at `report-ui/public/flow_bundle.json`.

## Reading the UI

- `Transitions`: user actions from one discovered page to another.
- `Generated Test Cases`: reusable flow candidates derived from transitions.
- `Discovered Pages`: unique crawl pages/screens (graph nodes), with optional technical IDs.

## Recommended Team Workflow

1. Run baseline crawl on target environment.
2. Save artifacts and persisted run in SQLite.
3. Repeat crawl after code/deploy changes.
4. Export history snapshot.
5. Compare transition patterns and generated cases for regressions or new paths.

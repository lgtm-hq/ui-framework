# Flowscout — Project Context

## What this is

Flowscout is an **LLM-free automated web path exploration framework** written in Python. It takes a URL, discovers all interactive elements on the page, systematically traverses paths by interacting with them, builds a state graph, and reports what flows it found. All intelligence comes from heuristics, DOM analysis, and rule-based logic — no LLM calls.

The MVP deliberately avoids LLM integration to push the limits of what deterministic heuristics can achieve. An LLM layer may be added later as an optional upgrade.

## Repository layout

- **Working directory**: This is a git worktree on the `mvp` branch (parent repo: `ui-framework`)
- **Package name**: `flowscout` (installed as editable via `uv sync`)
- **Entry point**: `flowscout.cli:main` (Click CLI)
- **Source**: `src/flowscout/`
- **Tests**: `tests/` (pytest, 78 tests across 7 files)

## How to run

```bash
uv sync                                    # Install deps
uv run playwright install chromium         # Install browser
uv run flowscout explore <url>             # Run exploration
uv run pytest tests/ -v                    # Run tests
uv run lintro chk                          # Lint check
uv run lintro fmt                          # Format
```

## Module responsibilities

| Module        | File                          | Purpose                                                                                                                                                                                                                                                                  |
| ------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Models**    | `core/state.py`               | `PageState`, `ExplorerConfig`, `FingerprintConfig`, `ExplorationStrategy` — all Pydantic models. State fingerprinting via SHA-256 of URL + DOM hash + text hash + form hash.                                                                                             |
| **Browser**   | `core/browser.py`             | Async Playwright wrapper. Launches browser, navigates, captures page state (runs in-browser JS for DOM structure, visible text, form state), executes actions (click/fill/select/check/hover/submit/navigate), waits for DOM stability.                                  |
| **Navigator** | `core/navigator.py`           | Priority-BFS exploration engine. Manages frontier (heapq), visited set, backtracking, group deprioritization. Main `explore()` loop drives the entire crawl.                                                                                                             |
| **Elements**  | `discovery/elements.py`       | Three-layer element discovery: CSS selector sweep (in-browser JS), a11y tree enrichment, pattern detection (dropdowns, tabs, toggles). 19 `ElementType` variants. Selector generation prefers stable selectors (id, data-testid, href, aria-label) over positional ones. |
| **Actions**   | `discovery/actions.py`        | Converts discovered elements to `Action` objects. `ActionType` enum (9 types: CLICK, FILL, SELECT_OPTION, CHECK, UNCHECK, SUBMIT_FORM, PRESS_KEY, HOVER, NAVIGATE). `OutcomeType` enum (9 types). Priority scoring per action type.                                      |
| **Inputs**    | `discovery/inputs.py`         | Heuristic input data generation. Pattern dictionary maps field names/types/placeholders to fake data (emails, passwords, names, addresses, etc.).                                                                                                                        |
| **Detector**  | `analysis/detector.py`        | Outcome classification after an action. Priority: URL change -> network errors -> console errors -> validation errors (error CSS selectors) -> DOM change -> no change.                                                                                                  |
| **Graph**     | `analysis/graph.py`           | NetworkX DiGraph wrapper. `ExplorationGraph` manages states, actions, results as graph nodes/edges. Extracts flows (simple paths root->leaves + cycles). `ExplorationResult` and `Flow` models.                                                                          |
| **Codegen**   | `codegen/playwright_tests.py` | Generates executable test suites from `ExplorationResult`. Supports pytest (Python) and Playwright Test (TS) frameworks. Generates flow tests, navigation tests, and xfail negative tests.                                                                               |
| **Terminal**  | `reporting/terminal.py`       | Rich console reporter. Banner, per-action log lines with colored outcome icons, summary tables.                                                                                                                                                                          |
| **HTML**      | `reporting/html.py`           | Standalone HTML report via Jinja2. Mission-control aesthetic (deep navy, phosphor-green). vis.js force-directed graph, stat cards, flow tables, action log.                                                                                                              |
| **Storage**   | `storage/db.py`               | SQLite persistence (WAL mode). Schema: runs, states, actions, results, flows. Cross-run analysis: new/disappeared states, flaky actions, action reliability. DB at `.flowscout/history.db`.                                                                              |
| **CLI**       | `cli.py`                      | Click CLI with commands: `explore`, `serve`, `history`, `reliability`, `generate`. Wires everything together.                                                                                                                                                            |

## Key design patterns

- **State fingerprinting**: Multi-signal SHA-256 hash distinguishes real state changes from cosmetic ones (e.g. theme CSS changes don't create new states, but a different selected tab does).
- **Priority-BFS**: Navigation links are explored first (priority 10), then forms (15), then tabs (30), then cosmetic variants (50+). After 3+ actions in a group all produce DOM_CHANGE, remaining group members get deprioritized to 80.
- **Backtracking**: Direct URL navigation first, verify fingerprint match. Fallback: replay shortest action path from root via graph.
- **Three-layer discovery**: CSS sweep catches standard elements, a11y tree adds semantic context, pattern detection finds custom widgets (dropdown triggers, tab groups).
- **Selector stability**: ID > data-testid/data-tab > a[href] > aria-label > role > name > input[type] > nth-of-type fallback.

## Report output structure

```
reports/<year>/<month-no>.<month-name>/<dd-mm-yyyy>/<hh.mm.ss>/
  report.html    — Interactive HTML dashboard
  result.json    — Full serialized ExplorationResult
  tests.py       — Generated Playwright tests (if --generate-tests)
```

## Test site

The MVP is tested against https://lgtm-hq.github.io/turbo-themes/ — a public GitHub Pages site with navigation, theme switching, and multiple pages. No authentication required.

## Known behaviors

- Hidden elements in collapsed responsive menus (e.g. "Getting Started", "API Reference") correctly produce TIMEOUT outcomes — they exist in the DOM but can't be clicked.
- "Flaky" actions like clicking "Home" when already on Home correctly show as navigation on some pages and no_change on others — this is expected, not a bug.
- The `_used_names` set in codegen is module-level and cleared at the start of each `_generate_pytest_suite()` call to avoid cross-run name collisions.

# Flowscout — Project Context

## What this is

Flowscout is an **LLM-free automated web path exploration framework**
written in Python. It takes a URL, discovers all interactive elements
on the page, systematically traverses paths by interacting with them,
builds a state graph, and reports what flows it found. All intelligence
comes from heuristics, DOM analysis, and rule-based logic — no LLM calls.

The MVP deliberately avoids LLM integration to push the limits of what
deterministic heuristics can achieve. An LLM layer may be added later
as an optional upgrade.

## Repository layout

- **Working directory**: This is a git worktree on the `mvp` branch
  (parent repo: `ui-framework`)
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

<!-- markdownlint-disable MD013 -->

| Module        | File                          | Purpose                                                                       |
| ------------- | ----------------------------- | ----------------------------------------------------------------------------- |
| **Models**    | `core/state.py`               | Pydantic models. State fingerprinting via SHA-256.                            |
| **Browser**   | `core/browser.py`             | Async Playwright wrapper. Launches browser, captures state, executes actions. |
| **Navigator** | `core/navigator.py`           | Priority-BFS exploration engine. Manages frontier, visited set, backtracking. |
| **Elements**  | `discovery/elements.py`       | Three-layer element discovery: CSS sweep, a11y tree, pattern detection.       |
| **Actions**   | `discovery/actions.py`        | Converts elements to `Action` objects. 9 action types, 9 outcome types.       |
| **Inputs**    | `discovery/inputs.py`         | Heuristic input data generation for form filling.                             |
| **Detector**  | `analysis/detector.py`        | Outcome classification after an action.                                       |
| **Graph**     | `analysis/graph.py`           | NetworkX DiGraph wrapper. Extracts flows (simple paths + cycles).             |
| **Codegen**   | `codegen/playwright_tests.py` | Generates executable test suites from `ExplorationResult`.                    |
| **Terminal**  | `reporting/terminal.py`       | Rich console reporter with colored outcome icons.                             |
| **HTML**      | `reporting/html.py`           | Standalone HTML report via Jinja2 with vis.js graph.                          |
| **Storage**   | `storage/db.py`               | SQLite persistence. Cross-run analysis.                                       |
| **CLI**       | `cli.py`                      | Click CLI: `explore`, `serve`, `history`, `reliability`, `generate`.          |

<!-- markdownlint-enable MD013 -->

## Layer import rules

Flowscout uses a strict Discovery -> Modeling -> Generation pipeline.
Keep imports aligned with these boundaries:

- Layer 1 (`core/`, `discovery/`, `analysis/`, `smart/`) may import from:
  `core/`, `discovery/`, `analysis/`
- Layer 2 (`modeling/`) may import from:
  `core/` (models only), `modeling/`
- Layer 3 (`codegen/`, `mbt/`, `reporting/`) may import from:
  `core/` (models only), `modeling/`
- CLI (`cli/`) may import from all layers
- Storage (`storage/`) may import from `core/` (models only)

## Key design patterns

- **State fingerprinting**: Multi-signal SHA-256 hash distinguishes
  real state changes from cosmetic ones (e.g. theme CSS changes don't
  create new states, but a different selected tab does).
- **Priority-BFS**: Navigation links are explored first (priority 10),
  then forms (15), then tabs (30), then cosmetic variants (50+).
  After 3+ actions in a group all produce DOM_CHANGE, remaining group
  members get deprioritized to 80.
- **Backtracking**: Direct URL navigation first, verify fingerprint
  match. Fallback: replay shortest action path from root via graph.
- **Three-layer discovery**: CSS sweep catches standard elements,
  a11y tree adds semantic context, pattern detection finds custom
  widgets (dropdown triggers, tab groups).
- **Selector stability**: ID > data-testid/data-tab > a[href] >
  aria-label > role > name > input[type] > nth-of-type fallback.

## Report output structure

```text
reports/<year>/<month-no>.<month-name>/<dd-mm-yyyy>/<hh.mm.ss>/
  report.html    — Interactive HTML dashboard
  result.json    — Full serialized ExplorationResult
  tests.py       — Generated Playwright tests (if --generate-tests)
```

## Test site

The MVP is tested against
<https://lgtm-hq.github.io/turbo-themes/> — a public GitHub Pages
site with navigation, theme switching, and multiple pages.
No authentication required.

## Known behaviors

- Hidden elements in collapsed responsive menus (e.g. "Getting
  Started", "API Reference") correctly produce TIMEOUT outcomes —
  they exist in the DOM but can't be clicked.
- "Flaky" actions like clicking "Home" when already on Home correctly
  show as navigation on some pages and no_change on others — this is
  expected, not a bug.
- The `_used_names` set in codegen is module-level and cleared at the
  start of each `_generate_pytest_suite()` call to avoid cross-run
  name collisions.

# Flowscout

LLM-free automated web path exploration framework. Point it at a URL and it discovers interactive elements, traverses every reachable path, builds a state graph, and reports what flows exist — all through heuristics, DOM analysis, and rule-based logic. No LLM required.

## What it does

1. **Discovers** every interactive element on a page (links, buttons, inputs, selects, tabs, dropdowns) using a three-layer detection strategy: CSS selector sweep, accessibility tree enrichment, and pattern detection.
2. **Traverses** paths using priority-BFS exploration — clicking links, filling forms, selecting options — and captures the resulting page state after each action.
3. **Fingerprints** each page state using a multi-signal hash (URL + DOM structure + visible text + form state) to distinguish real state changes from cosmetic ones like theme switches.
4. **Builds a state graph** (NetworkX DiGraph) where nodes are unique page states and edges are actions with their outcomes (navigation, DOM change, no change, timeout, error).
5. **Extracts flows** — all simple paths from root to leaf states, plus cycle detection.
6. **Reports** results via Rich terminal output, an interactive HTML dashboard (vis.js force-directed graph), and JSON export.
7. **Generates executable Playwright test suites** from discovered flows (pytest or Playwright Test format).
8. **Tracks history** in SQLite across runs — detecting new/disappeared states, flaky actions, and reliability trends.

## Installation

```bash
uv sync
uv run playwright install chromium
```

## Usage

```bash
# Basic exploration
flowscout explore https://example.com

# With visible browser and test generation
flowscout explore https://example.com --no-headless --generate-tests

# Tuning parameters
flowscout explore https://example.com \
  --max-depth 3 \
  --max-states 50 \
  --max-actions 20 \
  --strategy priority \
  --output-dir ./reports \
  --screenshot \
  -v

# View history across runs
flowscout history --url https://example.com

# Action reliability report
flowscout reliability --url https://example.com

# Generate tests from a previous JSON result
flowscout generate reports/2026/02.February/06-02-2026/12.58.21/result.json

# Open an HTML report in the browser
flowscout serve reports/2026/02.February/06-02-2026/12.58.21/report.html
```

## Report output structure

Each run produces files in a hierarchical directory:

```
reports/<year>/<month-no>.<month-name>/<dd-mm-yyyy>/<hh.mm.ss>/
  report.html    — Interactive HTML dashboard with state graph
  result.json    — Full exploration result (Pydantic-serialized)
  tests.py       — Generated Playwright test suite (if --generate-tests)
```

## Architecture

```
src/flowscout/
├── cli.py                       # Click CLI (explore, serve, history, reliability, generate)
├── core/
│   ├── state.py                 # Pydantic models: PageState, ExplorerConfig, FingerprintConfig
│   │                            # State fingerprinting: normalize_url, build_fingerprint, make_state_id
│   ├── browser.py               # Async Playwright wrapper: launch, navigate, capture_state, execute_action
│   │                            # In-browser JS for DOM structure, visible text, form state, signals
│   └── navigator.py             # Priority-BFS exploration engine with frontier, backtracking, group deprioritization
├── discovery/
│   ├── elements.py              # Three-layer element discovery (CSS sweep + a11y tree + pattern detection)
│   │                            # InteractiveElement model, ElementType enum (19 types), priority scoring
│   ├── actions.py               # Action generation from elements: Action model, ActionType enum, OutcomeType enum
│   │                            # Maps element types to browser actions (click, fill, select, submit, etc.)
│   └── inputs.py                # Heuristic input data generation: field name/type pattern matching to fake data
├── analysis/
│   ├── detector.py              # Outcome classification: URL change, network errors, console errors, DOM change
│   └── graph.py                 # NetworkX DiGraph wrapper: state graph, flow extraction, path finding
│                                # ExplorationResult and Flow models
├── codegen/
│   └── playwright_tests.py      # Generate pytest or Playwright Test suites from flows
├── reporting/
│   ├── terminal.py              # Rich console output: banner, per-action logs, summary tables
│   └── html.py                  # Standalone HTML report: Jinja2 template with vis.js graph visualization
└── storage/
    └── db.py                    # SQLite persistence: run history, cross-run analysis, flaky action detection
```

## Key design decisions

**State fingerprinting**: SHA-256 of normalized URL + DOM structure hash (tag skeleton, ignoring text/attributes) + visible text hash (headings, active nav, selected tabs) + form state hash (selected options, checked boxes, input values). Theme CSS changes alone don't create new states, but a theme selector's value is part of form state.

**Exploration strategy**: Priority-BFS. Navigation links get highest priority (discover new pages first), then submit buttons, then form inputs, then tabs/dropdowns, then cosmetic variants. After 3+ actions in a group all produce DOM_CHANGE without navigation, remaining group members are deprioritized.

**Backtracking**: Navigate to target state's URL. If fingerprint doesn't match (e.g. tab state was lost), replay the shortest action path from root via the graph.

**No LLM**: All classification uses StrEnums, pattern matching on field names/types/ARIA attributes, and heuristic dictionaries. The framework is designed so an LLM layer can be added later as an optional intelligence upgrade.

**Selector stability**: Prefers stable selectors (id, data-testid, data-tab, href, aria-label) over fragile positional ones (nth-child, nth-of-type) to survive page re-renders.

## Running tests

```bash
uv run pytest tests/ -v --cov=flowscout
```

## Dependencies

| Package    | Purpose                                   |
| ---------- | ----------------------------------------- |
| playwright | Browser automation (async API)            |
| pydantic   | Data models with validation/serialization |
| networkx   | State graph and flow extraction           |
| rich       | Terminal output                           |
| click      | CLI framework                             |
| jinja2     | HTML report templates                     |

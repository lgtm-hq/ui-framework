# Flowscout

LLM-free automated web path exploration and site modeling framework. Give it a URL and it discovers every interactive element, systematically clicks through pages, builds a state graph, classifies page types, maps navigation flows, and generates test code — all using deterministic heuristics, no LLM calls.

## Installation

```bash
uv sync
uv run playwright install chromium
```

Or use the convenience recipe:

```bash
just setup
```

## Quick start

### Explore a site with full site modeling and test generation

```bash
uv run flowscout explore https://example.com --smart --generate-tests
```

`flowscout explore` automatically reads `.crawl-config` (if present). Any CLI flag you pass overrides the file.

This runs both streams:

- **Stream 1 (Explorer)** — discovers elements, clicks through pages, builds a state graph
- **Stream 2 (Site Model)** — groups pages into named page types, maps navigation between them, synthesizes test scenarios, generates POM-backed tests

### View the HTML report

```bash
uv run flowscout serve reports/2026/02.February/07-02-2026/14.30.00/report.html
```

Opens the interactive HTML dashboard in your browser. The report is a standalone file — you can also open it directly in any browser.

## Commands

### `explore`

The main command. Discovers and maps a web application.

```bash
uv run flowscout explore <url> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--smart` | off | Enable smart mode: page archetype recognition, contextual input generation, coverage-aware exploration, and site model building |
| `--generate-tests` / `-g` | off | Generate test suites from exploration results |
| `--test-framework` | `pytest` | `pytest` (Python) or `playwright` (TypeScript) |
| `--max-depth` / `-d` | 3 | Maximum traversal depth from start URL |
| `--max-states` / `-s` | 50 | Maximum unique states to discover |
| `--max-actions` / `-a` | 20 | Maximum actions per state |
| `--headless` / `--no-headless` | headless | Run browser in headless or headed mode |
| `--timeout` / `-t` | 10000 | Navigation timeout in milliseconds |
| `--output-dir` / `-o` | `./reports` | Output directory for reports |
| `--environment` | `dev` | Environment label used in per-site workspace paths |
| `--screenshot` / `--no-screenshot` | on | Capture action evidence screenshots with highlighted targets |
| `--strategy` | `priority` | Exploration strategy: `bfs`, `dfs`, or `priority` |
| `--bdd` | off | Generate Gherkin `.feature` file |
| `--narrative` | off | Generate Markdown narrative report |
| `--no-db` | off | Skip saving to SQLite history |
| `--verbose` / `-v` | off | Verbose output and debug logging |
| `--input-profile` | `safe` | Input generation profile: `safe`, `contextual`, `negative` |
| `--enforce-non-destructive` / `--no-enforce-non-destructive` | on | Block high-impact actions by default |
| `--allow-form-submits` | off | Allow `submit_form` actions (disabled by default for safety) |
| `--config-file` | `.crawl-config` | Path to TOML-style crawl defaults |
| `--auth-config-file` | `.flowscout-auth.toml` | Path to auth profile TOML file |
| `--auth-profile` | unset | Explicit auth profile name |
| `--auth-required` | off | Fail fast when auth profile/credentials are missing |

By default, exploration runs in non-destructive mode:

- form submissions are blocked unless `--allow-form-submits` is passed,
- high-impact actions with destructive keywords are filtered before execution.
- invalid/negative form submissions are only generated when `--input-profile negative` is used.
- action screenshots are captured by default and linked in the execution log.
- each step records a transition confidence score with a reason.
- HTML report includes an exploration diagnostics section for low-confidence and flaky transitions.

**Examples:**

```bash
# Basic exploration (Stream 1 only)
uv run flowscout explore https://example.com

# Full site model with tests (Stream 1 + Stream 2)
uv run flowscout explore https://example.com --smart --generate-tests

# Visible browser, screenshots, verbose logging
uv run flowscout explore https://example.com --smart -g --no-headless --screenshot -v

# TypeScript output
uv run flowscout explore https://example.com --smart -g --test-framework playwright

# Deeper exploration
uv run flowscout explore https://example.com --smart -g --max-depth 5 --max-states 100

# Allow safe form submission testing in a controlled environment
uv run flowscout explore https://example.com --allow-form-submits

# Enable negative validation exploration
uv run flowscout explore https://example.com --input-profile negative --allow-form-submits

# Isolate runs under a specific environment workspace
uv run flowscout explore https://example.com --environment staging
```

### `serve`

Open an HTML report in the browser.

```bash
uv run flowscout serve <path-to-report.html>
```

### `generate`

Regenerate tests from a previously saved `result.json` without re-running the exploration.

```bash
# Regenerate flow tests (Stream 1)
uv run flowscout generate path/to/result.json

# Regenerate site model + scenario tests (Stream 2)
uv run flowscout generate path/to/result.json --site-model

# TypeScript output
uv run flowscout generate path/to/result.json --framework playwright

# Gherkin feature file
uv run flowscout generate path/to/result.json --framework bdd
```

### `history`

Show exploration history from the SQLite database.

```bash
uv run flowscout history
uv run flowscout history --url https://example.com --limit 10
```

### `reliability`

Show action reliability across multiple runs of the same URL. Flags "flaky" actions that produce different outcomes across runs.

```bash
uv run flowscout reliability --url https://example.com
```

### `benchmark`

Summarize baseline metrics from a saved `result.json` artifact (duration, coverage, confidence, low-confidence count, interactive/content element mix, and flaky-action history when DB is available).

```bash
uv run flowscout benchmark path/to/result.json

# Fail if page coverage target is not met
uv run flowscout benchmark path/to/result.json --require-coverage-target

# Fail if low-confidence transitions exceed 2
uv run flowscout benchmark path/to/result.json --max-low-confidence 2
```

## Output structure

Each exploration run is isolated by site + environment:

```
reports/<domain>/<environment>/runs/<timestamp>/
  report.html          Interactive HTML dashboard with state graph
  result.json          Full serialized exploration data
  evidence/actions/    Action screenshots with highlighted targets (--screenshot)
  site_model.json      Site model: page types, navigation, scenarios (--smart)
  tests.py             Flow replay tests (--generate-tests)
  pom_tests.py         POM-based tests (--smart --generate-tests)
  scenario_tests.py    Scenario-based tests from site model (--smart --generate-tests)
  pages/               Page Object Model classes (--smart --generate-tests)
    movie_listing_page.py
    movie_detail_page.py
    ...
```

In smart mode, `result.json` also includes an `element_inventory` summary (interactive vs non-interactive catalog totals and per-page breakdown).

Without `--smart`, only `report.html`, `result.json`, and `tests.py` are generated.

## Crawl configuration file

Use `.crawl-config` to define project defaults such as:

- exploration budgets (`max_depth`, `max_states`, `max_actions_per_state`)
- runtime behavior (`smart`, `headless`, `capture_screenshots`, safety flags)
- timing values (`navigation_timeout_ms`, `action_timeout_ms`, `stability_timeout_ms`)
- persistence/output (`output_dir`, `environment`, `db_path`, `persist_history`)
- optional per-domain + per-environment overrides (`[domains."<pattern>"]`)

Precedence is always:

1. explicit CLI flags
2. `.crawl-config`
3. built-in defaults

Domain-scoped override example:

```toml
max_depth = 2
max_states = 30
environment = "dev"

[domains."*.example.com"]
max_depth = 4
auth_profile = "example_default"

[domains."*.example.com".environments.staging]
max_states = 90
environment = "staging"
auth_profile = "example_staging"
```

## Authentication bootstrap (local-only)

Flowscout supports deterministic login bootstrap before exploration:

1. define profile selectors + env-var references in `.flowscout-auth.toml`
2. export credentials locally:
   - `export E2E_USERNAME="..."`,
   - `export E2E_PASSWORD="..."`,
3. run exploration with a matching profile.

Example:

```bash
cp .flowscout-auth.example.toml .flowscout-auth.toml
export E2E_USERNAME="qa-user"
export E2E_PASSWORD="qa-pass"
uv run flowscout explore https://example.com --environment staging --auth-profile sample_staging --auth-required
```

Security behavior:

- only env-var names are persisted in artifacts (`result.json` config metadata),
- secret values are never written to report or run artifacts,
- if `--auth-required` is set, run aborts when profile or env vars are missing.

## Smart mode

Smart mode (`--smart`) enables Stream 2 — the site model layer that transforms raw exploration data into a structured, human-readable map of the site.

### Page archetype classification

Every discovered page is classified into an archetype using score-based heuristics:

| Archetype | Description |
|-----------|-------------|
| `listing` | Pages with repeated items (product grids, article lists) |
| `detail` | Single-item pages (product detail, article view) |
| `search_results` | Search results with a search input |
| `form` | Pages dominated by form inputs |
| `landing` | Hero sections, marketing pages |
| `error` | 404 / error pages |

### Site model

The site model (`site_model.json`) groups raw states into **page types** by structural signature (DOM skeleton hash). Each page type has:

- A human-readable name inferred from page titles and URL paths
- An archetype classification with confidence score
- A URL pattern (regex) derived from instance URLs
- Feature flags: `has_search`, `has_pagination`, `has_filters`
- An element catalog with selectors, organized by zone (navigation, search, main content, sidebar, footer, etc.)

**Navigation edges** show how page types connect — e.g., "Movies Listing" -> "Movie Detail" via clicking a movie card, with occurrence counts.

**Test scenarios** are synthesized from the page type graph:

| Scenario | Trigger | Priority |
|----------|---------|----------|
| Load & Verify | Every page type | important |
| Browse & View Detail | Listing with edge to Detail | critical |
| Search | Listing with search | critical |
| Pagination | Listing with pagination | important |
| Filter | Listing with filters | important |
| Form Submit | Form page type | critical |
| Round Trip | Any A->B->A cycle | nice-to-have |

The terminal prints summary tables for page types, navigation map, and test scenarios after each smart mode run.

### Generated tests

All generated scenario tests use Page Object Model classes — no raw selectors in test code:

```python
# scenario_tests.py (generated)
from pages.movie_listing_page import MovieListingPage
from pages.movie_detail_page import MovieDetailPage

def test_browse_and_view_detail(page: Page) -> None:
    """Browse listing and click an item to see detail."""
    listing = MovieListingPage(page)
    listing.navigate()
    listing.select_item(0)
    detail = MovieDetailPage(page)
    expect(page).to_have_url(re.compile(r".*/movies/[^/]+"))
```

POM classes are generated in the `pages/` directory, one per page type, with locator properties organized by zone and helper methods for common interactions (navigate, search, select item).

## Architecture

```
src/flowscout/
├── cli.py                       # Click CLI (explore, serve, history, reliability, generate)
├── core/
│   ├── state.py                 # PageState, ExplorerConfig, FingerprintConfig
│   ├── browser.py               # Async Playwright wrapper
│   └── navigator.py             # Priority-BFS exploration engine
├── discovery/
│   ├── elements.py              # Three-layer element discovery (CSS + a11y + pattern detection)
│   ├── actions.py               # Action generation from elements
│   ├── inputs.py                # Heuristic input data generation
│   └── context.py               # Contextual input from page entities
├── analysis/
│   ├── detector.py              # Outcome classification after actions
│   ├── graph.py                 # State graph (NetworkX), flow extraction, ExplorationResult
│   ├── archetype.py             # Page archetype classification, structural analysis, element cataloging
│   ├── expectations.py          # Content expectation verification by archetype
│   └── site_model.py            # Site model: page type grouping, navigation edges, SiteModelBuilder
├── smart/
│   ├── planner.py               # Smart planner: coordinates archetype, coverage, and flow advice
│   ├── coverage.py              # Coverage tracking across exploration
│   └── scenarios.py             # Test scenario synthesis from page type graph
├── codegen/
│   ├── playwright_tests.py      # Flow-based test generation (pytest / Playwright Test)
│   ├── page_objects.py          # POM class generation from element catalogs
│   ├── pom_tests.py             # POM-based test generation
│   ├── scenario_tests.py        # Scenario-based test generation (always POM-backed)
│   └── bdd.py                   # Gherkin feature file and narrative report generation
├── reporting/
│   ├── terminal.py              # Rich console output: banner, action logs, summary tables, site model
│   └── html.py                  # Standalone HTML report with vis.js graph
└── storage/
    └── db.py                    # SQLite persistence: run history, cross-run analysis
```

## Key design decisions

**Two-stream architecture**: Stream 1 (explorer) produces raw exploration data. Stream 2 (site model) is a post-processing layer that consumes the same data and produces structured output. Both run from a single exploration — Stream 1 stays untouched, Stream 2 is a lens over it.

**State fingerprinting**: SHA-256 of normalized URL + DOM structure hash + visible text hash + form state hash. Theme CSS changes alone don't create new states, but a selected tab value does.

**Exploration strategy**: Priority-BFS. Navigation links get highest priority (discover new pages), then submit buttons, then form inputs, then tabs/dropdowns. After 3+ actions in a group all produce DOM_CHANGE, remaining members are deprioritized.

**Structural signature grouping**: Pages with the same DOM skeleton hash are grouped into one page type. This means two "Movie Detail" pages with different content are recognized as the same page type.

**No LLM**: All classification uses StrEnums, pattern matching, and heuristic dictionaries. Designed so an LLM layer can be added later as an optional upgrade.

**Selector stability**: Prefers stable selectors (id, data-testid, href, aria-label) over positional ones (nth-child) for resilient test code.

## Development

```bash
uv run pytest tests/ -v          # Run tests (322 tests)
uv run lintro chk                # Lint check
uv run lintro fmt                # Format
```

## Dependencies

| Package | Purpose |
|---------|---------|
| playwright | Browser automation (async API) |
| pydantic | Data models with validation/serialization |
| networkx | State graph and flow extraction |
| rich | Terminal output |
| click | CLI framework |
| jinja2 | HTML report templates |

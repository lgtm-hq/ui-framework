# Flowscout Roadmap — From Exploration Tool to Test Automation Accelerator

## Vision

Flowscout's purpose is to **eliminate the manual setup grind** of test
automation. Point it at a site, let it explore, and get back:

1. A **page inventory** — how many distinct pages exist, grouped by
   template
2. **Page Object Model classes** — with stable locators, shared
   components, and domain-specific methods
3. **Deduplicated flow templates** — "click any movie tile → detail
   page" shown once with occurrence count, not 15 separate flows
4. **MBT-ready state machine** — walkable graph with coverage metrics
   and standard export formats
5. **Actionable dashboard** — page object previews, locator quality
   scores, flow templates, MBT visualization

The framework discovers and structures. The human adds domain
knowledge, edge cases, and assertions.

---

## Architecture: Three-Layer Pipeline

Everything in this roadmap is built around a strict separation of
three concerns. This separation is **not optional** — every milestone
must respect these boundaries. Violating them creates the kind of
tangled coupling that requires painful refactoring later.

### The Three Layers

````text
┌─────────────────────────────────────────────────────┐
│  LAYER 1: DISCOVERY                                 │
│  "What exists on this site?"                        │
│                                                     │
│  Crawl, interact, observe. Capture raw data.        │
│  No interpretation, no grouping, no generation.     │
│                                                     │
│  Input:  URL + config                               │
│  Output: ExplorationResult (serializable JSON)      │
│                                                     │
│  Modules: core/browser, core/navigator,             │
│           core/state, core/archetypes,               │
│           core/action_types,                         │
│           discovery/elements, discovery/actions,     │
│           discovery/inputs, analysis/detector        │
└──────────────────────┬──────────────────────────────┘
                       │ ExplorationResult
                       ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 2: MODELING                                  │
│  "What does it mean?"                               │
│                                                     │
│  Group states into page types. Extract components.  │
│  Deduplicate flows. Score locators. Build the site   │
│  model (state machine). Infer guards.               │
│                                                     │
│  Input:  ExplorationResult                          │
│  Output: SiteModel (serializable JSON)              │
│                                                     │
│  Modules: modeling/site_model, modeling/archetype,   │
│           modeling/scenarios,                        │
│           analysis/graph (flow dedup only),          │
│           modeling/components, modeling/locators     │
└──────────────────────┬──────────────────────────────┘
                       │ SiteModel
                       ▼
┌─────────────────────────────────────────────────────┐
│  LAYER 3: GENERATION                                │
│  "What to produce?"                                 │
│                                                     │
│  Generate POM classes. Walk the model for MBT paths.│
│  Generate test files. Export to external formats.    │
│  Build the dashboard.                               │
│                                                     │
│  Input:  SiteModel (+ ExplorationResult for detail) │
│  Output: Files on disk (POM, tests, reports, exports)│
│                                                     │
│  Modules: codegen/page_objects, codegen/scenarios,   │
│           mbt/walker, mbt/exporters, reporting/      │
└─────────────────────────────────────────────────────┘
```text

### Pipeline Rules

1. **Each layer's output is a complete, serializable artifact.**
   `ExplorationResult` and `SiteModel` are both JSON-serializable
   Pydantic models. You can run Layer 1 today and Layer 2 tomorrow
   without re-crawling. You can swap Layer 3's codegen strategy
   without touching the model.

2. **Data flows down, never up.** Discovery never imports from
   modeling. Modeling never imports from generation. Generation reads
   from both modeling and discovery (it needs the model for structure
   and the exploration result for detail like screenshots).

3. **Each layer is independently testable.** Discovery tests use
   mock browsers. Modeling tests use fixture `ExplorationResult`
   objects. Generation tests use fixture `SiteModel` objects.

4. **The CLI orchestrates the pipeline.** The CLI is the only place
   where layers are wired together. Individual layers know nothing
   about the CLI.

### CLI Pipeline (Target State)

```bash
# Full pipeline (most common — does everything)
uv run flowscout explore <url>

# Or run layers independently:
uv run flowscout explore <url> --output result.json    # Layer 1 only
uv run flowscout model result.json --output model.json # Layer 2 only
uv run flowscout generate model.json --output ./out    # Layer 3 only

# Layer 3 sub-commands:
uv run flowscout generate model.json --pom             # POM classes
uv run flowscout generate model.json --tests           # Scenario tests
uv run flowscout generate model.json --report          # HTML dashboard
uv run flowscout generate model.json --export dot      # MBT export
uv run flowscout generate model.json --mbt edge        # MBT walk + tests
```text

### Current State vs. Target

| Concern            | Currently Lives In                                                             | Should Live In                                                                    | Migration                      |
| ------------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- | ------------------------------ |
| Flow extraction    | `analysis/graph.py` (Layer 1)                                                  | `analysis/graph.py` (Layer 1 — raw flows) + `modeling/flows.py` (Layer 2 — dedup) | Split in Phase 2.1             |
| Scenario synthesis | `modeling/scenarios.py` (Layer 2)                                              | `modeling/scenarios.py` (Layer 2)                                                 | Done (Phase 1.4)               |
| Page analysis      | `smart/planner.py` (Layer 1 — during crawl)                                    | Keep in Layer 1, shared types in `core/archetypes.py`                             | Done (Phase 1.4)               |
| POM generation     | `codegen/page_objects.py` (Layer 3)                                            | `codegen/page_objects.py` (Layer 3)                                               | No change needed               |
| Report building    | `reporting/html.py` (Layer 3)                                                  | `reporting/html.py` (Layer 3)                                                     | Feed from SiteModel in Phase 4 |
| Test codegen       | `codegen/scenario_tests.py` (primary) + `codegen/playwright_tests.py` (legacy) | `codegen/scenario_tests.py` (Layer 3)                                             | Done (Phase 1.3)               |
| Site model         | `modeling/site_model.py` (Layer 2)                                             | `modeling/site_model.py` (Layer 2)                                                | Done (Phase 1.4)               |
| MBT walking        | Does not exist                                                                 | `mbt/walker.py` (Layer 3)                                                         | Create in Phase 3.1            |

---

## Phase 1: Foundation Reset

**Status**: COMPLETE

**Goal**: Align defaults with the vision and establish the three-layer
boundary.

### 1.1 Make smart mode the default

Smart mode is the product. Non-smart mode becomes `--no-smart`.

**Files to modify**:

- `src/flowscout/cli/explore.py` — flip default for `--smart` flag
  to `True`, add `--no-smart` flag
- `src/flowscout/core/navigator.py` — ensure `SmartPlanner` is
  instantiated by default when config doesn't explicitly disable
- `CLAUDE.md` — update "How to run" examples to remove `--smart` flag

**Acceptance criteria**:

- [x] `uv run flowscout explore <url>` runs with smart mode enabled
- [x] `uv run flowscout explore <url> --no-smart` disables it
- [x] All existing tests pass (update fixtures that assumed non-smart
      default)
- [x] CLI help text reflects the new default

### 1.2 Simplify the verdict system

Replace the 3-level verdict system (pass/fail/warn with confidence
scoring) with a simpler **observation model**. The explorer discovers
what's there — it doesn't judge pass/fail without requirements.

**Current state** (to remove/simplify):

- `StepVerdict` (PASS/FAIL/INCONCLUSIVE) in `analysis/verdict.py`
- `JourneyVerdict` (aggregate) in flow narratives
- Confidence scores (0.0–1.0) with reasons
- Expected/actual assertions on `ActionResult`

**Target state**:

- `ObservationResult` with: outcome (kept), stability_score (replaces
  confidence), observation_notes (replaces verdict_reason)
- `FlowSummary` with: outcomes list, stability_score (aggregate),
  is_stable (bool)
- Remove: verdict, expected, actual, confidence_reason from
  `ActionResult`
- Remove: `StepVerdict`, `JourneyVerdict`,
  `_compute_step_verdict()`, `_compute_journey_verdict()`

**Files to modify**:

- `src/flowscout/analysis/verdict.py` — simplify or remove
- `src/flowscout/core/state.py` — update `ActionResult` model
- `src/flowscout/analysis/graph.py` — update `Flow` model
- `src/flowscout/core/navigator.py` — remove verdict computation
- `src/flowscout/analysis/narrative.py` — simplify narrative
  generation
- `src/flowscout/reporting/html.py` — update context building
- `src/flowscout/reporting/terminal.py` — update summary output
- `src/flowscout/codegen/playwright_tests.py` — remove verdict
  comments
- `src/flowscout/storage/db.py` — update schema (keep columns for
  backward compat, stop writing verdict data)
- All test files referencing verdicts

**Acceptance criteria**:

- [x] `ActionResult` has `stability_score: float` instead of
      `confidence` + `verdict` + `expected` + `actual`
- [x] `Flow` has `stability_score: float` and `is_stable: bool`
      instead of `verdict: JourneyVerdict`
- [x] Reports show stability scores, not pass/fail verdicts
- [x] All tests updated and passing
- [x] No references to `StepVerdict` or `JourneyVerdict` remain

### 1.3 Consolidate codegen output paths

Currently 3 separate codegen paths produce overlapping output:

1. Flat Playwright tests (`codegen/playwright_tests.py`)
2. POM-based scenario tests (`codegen/scenario_tests.py`)
3. BDD feature files (`codegen/bdd.py`)

Consolidate to **one primary output**: POM classes + scenario tests.
Keep BDD as optional. Remove flat Playwright test generation (it
produces inferior output that contradicts the POM vision).

**Files to modify**:

- `src/flowscout/codegen/playwright_tests.py` — deprecate, keep as
  `--legacy-tests` escape hatch
- `src/flowscout/cli/explore.py` — make `--generate-tests` produce
  POM + scenario tests by default
- Remove duplicate test name generation logic between codegen modules

**Acceptance criteria**:

- [x] `--generate-tests` produces `pages/` directory + scenario test
      file by default
- [x] `--generate-tests --legacy` produces old flat scripts
- [x] BDD output still works via `--bdd` flag
- [x] No duplicate codegen logic between modules

### 1.4 Establish the three-layer boundary

This is the structural milestone that prevents tech debt
accumulation. Reorganize modules so the Discovery → Modeling →
Generation pipeline has clean, enforced boundaries.

**Directory structure (target)**:

```text
src/flowscout/
  # Layer 1: Discovery
  core/
    browser.py          # Playwright wrapper
    navigator.py        # Exploration engine (Priority-BFS)
    state.py            # PageState, ExplorerConfig, fingerprinting
  discovery/
    elements.py         # Element discovery (CSS + a11y + patterns)
    actions.py          # Action generation from elements
    inputs.py           # Heuristic input data generation
    intent.py           # Action intent inference
  analysis/
    detector.py         # Outcome classification
    graph.py            # ExplorationGraph, raw flow extraction
  smart/
    planner.py          # Real-time exploration guidance (stays L1)
    coverage.py         # Exploration coverage tracking (stays L1)

  # Layer 2: Modeling
  modeling/
    __init__.py
    site_model.py       # SiteModel, PageType, NavigationEdge
    archetype.py        # Page archetype classification
    components.py       # SharedComponent extraction (new)
    flows.py            # FlowTemplate deduplication (new)
    locators.py         # Locator stability scoring (new)
    scenarios.py        # Scenario synthesis from model

  # Layer 3: Generation
  codegen/
    page_objects.py     # POM class generation
    scenario_tests.py   # Scenario test generation (primary)
    playwright_tests.py # Legacy flat tests (--legacy escape hatch)
    bdd.py              # BDD feature file generation (optional)
  mbt/
    __init__.py
    walker.py           # Graph walking strategies (new)
    coverage.py         # MBT coverage metrics (new)
    exporters/          # GraphWalker, DOT, Mermaid (new)
  reporting/
    html.py             # HTML dashboard
    terminal.py         # Terminal reporter

  # Cross-cutting (no layer — used by all)
  storage/
    db.py               # SQLite persistence
  plugins/
    __init__.py         # Plugin registry
  cli/
    __init__.py         # CLI (orchestrates pipeline)
    explore.py          # explore command
    model.py            # model command (new)
    generate.py         # generate command (new)
````

**Migration steps**:

1. Create `src/flowscout/modeling/` package
2. Move `analysis/site_model.py` →
   `modeling/site_model.py` (update all imports)
3. Move `analysis/archetype.py` →
   `modeling/archetype.py` (update all imports)
4. Move `smart/scenarios.py` →
   `modeling/scenarios.py` (update all imports)
5. Create `modeling/components.py` (stub for Phase 2.2)
6. Create `modeling/flows.py` (stub for Phase 2.1)
7. Create `modeling/locators.py` (stub for Phase 2.5)
8. Verify no circular imports between layers
9. Add `cli/model.py` with `model` command (reads
   `ExplorationResult`, outputs `SiteModel`)
10. Add `cli/generate.py` with `generate` command (reads
    `SiteModel`, produces files)
11. Update `cli/explore.py` to run full pipeline by default but
    support `--output` for Layer 1-only mode

**Import rules to enforce** (add to CLAUDE.md):

````text
# Layer 1 (discovery/) may import from: core/, discovery/, analysis/
# Layer 2 (modeling/)   may import from: core/ (models only), modeling/
# Layer 3 (codegen/, mbt/, reporting/) may import from:
#          core/ (models only), modeling/
# CLI (cli/) may import from: all layers
# Storage (storage/) may import from: core/ (models only)
```text

**Acceptance criteria**:

- [x] `modeling/` package exists with all Layer 2 modules
- [x] `mbt/` package exists (stubs for Phase 3)
- [x] No Layer 1 module imports from `modeling/` or `codegen/`
- [x] No Layer 2 module imports from `codegen/`, `mbt/`, or
      `reporting/`
- [x] `flowscout model result.json` CLI command works
- [x] `flowscout generate model.json` CLI command works
- [x] Full pipeline (`flowscout explore <url>`) still works
      end-to-end
- [x] All existing tests pass
- [x] Import rules documented in CLAUDE.md

### 1.5 Define serialization contracts between layers

Formalize the JSON schemas for `ExplorationResult` and `SiteModel`
so that Layer 2 can always consume Layer 1 output and Layer 3 can
always consume Layer 2 output, even across versions.

**Implementation**:

- Add `version` field to `ExplorationResult` and `SiteModel`
- Add `schema_version` constant to each
- Document the contract: what fields Layer 2 requires from Layer 1,
  what Layer 3 requires from Layer 2
- Add validation: `SiteModel.from_exploration_result()` raises clear
  errors if required fields are missing

**Files to create/modify**:

- `src/flowscout/core/state.py` — add `schema_version` to
  `ExplorationResult`
- `src/flowscout/modeling/site_model.py` — add `schema_version` to
  `SiteModel`, add `from_exploration_result()` with validation
- `tests/test_schema_contracts.py` — test round-trip
  serialization/deserialization across layers

**Acceptance criteria**:

- [x] `ExplorationResult` has `schema_version: str`
- [x] `SiteModel` has `schema_version: str`
- [x] `SiteModel.from_exploration_result(result)` validates input
- [x] Round-trip test: explore → serialize → deserialize → model →
      serialize → deserialize → generate
- [x] Clear error messages when schema versions mismatch

---

## Phase 1b: Real-World Site Readiness

**Goal**: Make the crawler work reliably on real-world sites that have
bot protection, authentication walls, and access controls. Without
this, all later phases are moot for production use.

**Context**: Testing against clean demo sites works fine. But real
test/UAT environments often have WAFs, bot detection, cookie consent
walls, and authentication — even in non-production. These milestones
add a graduated set of capabilities: detect when you're blocked,
reduce how often it happens, and provide escape hatches when it does.

### 1b.1 Blocked page detection

When the crawler lands on a page that's blocked (access denied, CAPTCHA,
WAF challenge, cookie consent wall), it currently treats it as a normal
page with 0 elements — a silent dead-end. The crawler should detect
these situations and surface them clearly.

**Layer**: 1 (Discovery)

**Detection signals**:

| Signal                  | Detected Via                                   | Classification    |
| ----------------------- | ---------------------------------------------- | ----------------- |
| HTTP 401/403            | Response status code                           | `ACCESS_DENIED`   |
| "Access Denied" text    | DOM content scan                               | `ACCESS_DENIED`   |
| CAPTCHA iframe          | reCAPTCHA/hCaptcha/Turnstile element detection | `CAPTCHA`         |
| "Verify you're human"   | DOM content scan                               | `CAPTCHA`         |
| Cookie consent modal    | Common consent framework selectors             | `CONSENT_WALL`    |
| Cloudflare challenge    | `cf-challenge` page markers                    | `WAF_CHALLENGE`   |
| 0 elements + error text | Heuristic fallback                             | `BLOCKED_UNKNOWN` |

**Design**:

```python
# core/state.py
class PageBlockReason(StrEnum):
    NONE = auto()
    ACCESS_DENIED = auto()
    CAPTCHA = auto()
    CONSENT_WALL = auto()
    WAF_CHALLENGE = auto()
    BLOCKED_UNKNOWN = auto()

# On PageState
block_reason: PageBlockReason = PageBlockReason.NONE
block_detail: str = ""   # Human-readable description
````

**Behavior when blocked**:

- Log a clear warning: "Page blocked: ACCESS_DENIED — 'Access Denied'
  detected in page title"
- Mark the `PageState` with `block_reason` and `block_detail`
- Surface in terminal report and HTML report
- Still capture a screenshot (useful for debugging)
- Skip element discovery (don't waste time scanning a blocked page)
- Continue exploration from other frontier items

**Files to create/modify**:

- `src/flowscout/core/state.py` — add `PageBlockReason` enum, add
  fields to `PageState`
- `src/flowscout/analysis/detector.py` — add `detect_page_block()`
  function with DOM content scanning
- `src/flowscout/core/navigator.py` — call block detection before
  element discovery, skip discovery if blocked
- `src/flowscout/reporting/terminal.py` — surface blocked states with
  clear warning
- `src/flowscout/reporting/html.py` — show blocked states in report

**Acceptance criteria**:

- [ ] Pages returning HTTP 401/403 are classified as `ACCESS_DENIED`
- [ ] Pages with "Access Denied" / "Forbidden" in title/body are
      detected
- [ ] CAPTCHA pages (reCAPTCHA, hCaptcha, Turnstile) are detected
- [ ] Blocked states are clearly reported in terminal and HTML output
- [ ] Element discovery is skipped for blocked pages
- [ ] Exploration continues from remaining frontier items
- [ ] Screenshot is still captured for blocked pages

### 1b.2 Browser stealth defaults

Add baseline anti-detection measures so the crawler doesn't get
blocked by simple bot checks on sites the user has legitimate access
to. This is not about evading sophisticated security — it's about
not failing on standard WAF configurations in test/UAT environments.

**Layer**: 1 (Discovery)

**Implementation**:

- Integrate `playwright-stealth` (or equivalent inline patches) to
  mask common automation indicators:
  - `navigator.webdriver` set to `undefined`
  - Chrome runtime properties present
  - Plugin/mime type arrays populated
  - WebGL vendor/renderer strings set to real values
  - Language and platform properties consistent
- Set a realistic User-Agent header matching the Chromium version
- Add `--disable-blink-features=AutomationControlled` browser arg
- Add `--stealth/--no-stealth` CLI flag (default: `--stealth`)

**Files to modify**:

- `src/flowscout/core/browser.py` — apply stealth patches during
  browser launch, add realistic User-Agent, add browser args
- `src/flowscout/cli/explore.py` — add `--stealth/--no-stealth` flag
- `pyproject.toml` — add `playwright-stealth` dependency (if using
  the package rather than inline patches)

**Acceptance criteria**:

- [ ] `navigator.webdriver` returns `undefined` on pages
- [ ] User-Agent matches a real Chrome browser string
- [ ] `--no-stealth` disables all stealth patches
- [ ] Stealth is enabled by default
- [ ] Sites with basic bot detection (webdriver check) no longer
      block the crawler
- [ ] No impact on existing test suite

### 1b.3 Persistent browser context

Allow saving and restoring browser state (cookies, localStorage,
sessionStorage) between runs. This enables:

- Solving a CAPTCHA once, then reusing the session
- Logging in manually once, then exploring authenticated pages
- Passing a WAF challenge once, then crawling freely

**Layer**: 1 (Discovery) + CLI

**Design**:

````bash
# Save browser state after exploration
uv run flowscout explore <url> --save-context ./ctx/mysite.json

# Restore browser state for next run
uv run flowscout explore <url> --load-context ./ctx/mysite.json

# Combined: load existing context, save updated context after
uv run flowscout explore <url> --context ./ctx/mysite.json
```text

**Implementation**:

- After browser context creation, load cookies/storage from file if
  `--load-context` or `--context` is provided
- After exploration completes, save cookies/storage to file if
  `--save-context` or `--context` is provided
- Context file format: JSON with `cookies`, `localStorage`,
  `sessionStorage`, `origins` sections
- Use Playwright's `context.storage_state()` and
  `browser.new_context(storage_state=...)` APIs

**Files to modify**:

- `src/flowscout/core/browser.py` — add `save_context()` and
  `load_context()` methods using Playwright's storage state API
- `src/flowscout/cli/explore.py` — add `--context`,
  `--save-context`, `--load-context` CLI flags
- `src/flowscout/core/state.py` — add context path to
  `ExplorerConfig`

**Acceptance criteria**:

- [ ] `--save-context` writes browser state to JSON file
- [ ] `--load-context` restores browser state before navigation
- [ ] `--context` combines load + save (round-trip)
- [ ] Cookies from a previous session are present on subsequent runs
- [ ] Context file format is documented
- [ ] Works with `--no-headless` for manual login → save → headless
      explore workflow

### 1b.4 CDP connection to existing browser

The ultimate escape hatch for hardened environments. Instead of
launching a new browser, connect to one the user already has open
with an active session. This completely sidesteps bot detection
because it's a real browser with real user activity history.

**Layer**: 1 (Discovery) + CLI

**Workflow**:

```bash
# User launches Chrome with remote debugging
google-chrome --remote-debugging-port=9222

# User navigates to site, passes any challenges manually

# Flowscout connects and explores
uv run flowscout explore <url> --cdp-endpoint ws://localhost:9222
````

**Implementation**:

- Add `--cdp-endpoint` CLI flag
- When provided, use `playwright.chromium.connect_over_cdp(endpoint)`
  instead of `playwright.chromium.launch()`
- Use existing page/tab or create a new one in the connected browser
- Skip browser launch/close lifecycle when using CDP
- All other exploration logic remains unchanged

**Files to modify**:

- `src/flowscout/core/browser.py` — add CDP connection path in
  `launch()`, use `connect_over_cdp()` when endpoint provided, skip
  `close()` for CDP sessions (don't close the user's browser)
- `src/flowscout/cli/explore.py` — add `--cdp-endpoint` flag
- `src/flowscout/core/state.py` — add `cdp_endpoint` to
  `ExplorerConfig`

**Acceptance criteria**:

- [ ] `--cdp-endpoint ws://localhost:9222` connects to running Chrome
- [ ] Exploration works on the connected browser's pages
- [ ] Browser is NOT closed when exploration ends (user's browser)
- [ ] All existing exploration features work over CDP
- [ ] Falls back to normal launch when `--cdp-endpoint` not provided
- [ ] Clear error message if CDP connection fails

---

## Phase 2: Output Quality

**Status**: COMPLETE

**Goal**: Make what comes out of exploration immediately usable by a
test engineer. All work in this phase lives in **Layer 2 (Modeling)**
or **Layer 3 (Generation)** — never modifying Layer 1 discovery logic.

### 2.1 Flow deduplication by page-type sequence

**Layer**: 2 (Modeling)

The single most impactful change. Flows that traverse the same
page-type sequence should be collapsed into one **flow template**
with an occurrence count.

**Design**:

```python
# modeling/flows.py (NEW — Layer 2)
class FlowTemplate(BaseModel):
    template_id: str
    name: str                          # "Browse Listing → Detail"
    page_type_sequence: list[str]      # ["listing_sig", "detail_sig"]
    occurrence_count: int              # 12
    representative_flow_id: str        # Flow ID with highest stability
    instance_flow_ids: list[str]       # All 12 flow IDs
    action_type_sequence: list[str]    # ["CLICK", "CLICK"]
    stability_score: float             # Aggregate across instances
```

**Implementation**:

- Create `modeling/flows.py` with `FlowTemplate` model and
  `deduplicate_flows()` function
- Takes raw `flows` + `state_to_page_type` lookup as input
- Groups flows by their page-type sequence
- Keeps one representative (highest stability score), tracks count
- Add `flow_templates: list[FlowTemplate]` to `SiteModel`

**Files to create/modify**:

- `src/flowscout/modeling/flows.py` — new (Layer 2)
- `src/flowscout/modeling/site_model.py` — integrate flow templates
- `src/flowscout/reporting/terminal.py` — show templates with counts
  (Layer 3)
- `src/flowscout/reporting/html.py` — show templates in report
  (Layer 3)

**Acceptance criteria**:

- [x] Clicking 10 movie tiles produces 1 flow template with
      `occurrence_count: 10`
- [x] Representative flow has full step details
- [x] Terminal reporter shows: "Browse Listing → Detail
      (10 instances)"
- [x] HTML report groups by template, expands to show instances
- [x] Raw flows still accessible on `ExplorationResult` (Layer 1
      output unchanged)
- [x] `FlowTemplate` lives in `modeling/` not `analysis/`

### 2.2 Component-level POM extraction

**Layer**: 2 (Modeling)

Detect shared element groups across pages (nav bar, theme dropdown,
footer) and generate reusable component objects.

**Design**:

```python
# modeling/components.py (NEW — Layer 2)
class SharedComponent(BaseModel):
    component_id: str
    name: str                          # "NavigationBar"
    class_name: str                    # "NavigationComponent"
    entries: list[CatalogEntry]        # Shared locators
    appears_on: list[str]              # Page type IDs
    frequency: float                   # % of pages that have it
    zone: ZoneType                     # NAVIGATION, FOOTER, etc.
```

**Implementation**:

- After building all `PageCatalog` objects, compare element sets
  across page types
- Elements appearing on 60%+ of pages with matching selectors →
  shared component
- Group by zone (NAVIGATION zone → `NavigationComponent`,
  FOOTER → `FooterComponent`)
- Add `shared_components: list[SharedComponent]` to `SiteModel`
- POM generation (Layer 3) reads components from `SiteModel`

**Files to create/modify**:

- `src/flowscout/modeling/components.py` — new (Layer 2)
- `src/flowscout/modeling/site_model.py` — call component extraction
  during build, add to `SiteModel`
- `src/flowscout/codegen/page_objects.py` — generate component
  classes, compose into page classes (Layer 3)

**Generated output structure**:

```text
pages/
  components/
    navigation_component.py
    theme_dropdown.py
  movie_listing_page.py        # Imports NavigationComponent
  movie_detail_page.py         # Imports NavigationComponent
```

**Acceptance criteria**:

- [x] Nav bar appearing on all pages → `NavigationComponent` class
- [x] Page classes import and use components via composition
- [x] Component has its own locators and methods
- [x] No duplicate locators between component and page class
- [x] `SharedComponent` lives in `modeling/` — codegen reads it from
      `SiteModel`

### 2.3 Inheritance-aware POM generation

**Layer**: 3 (Generation) — reads from Layer 2's `SiteModel`

Generate a `BasePage` class with common locators and methods, with
page-specific subclasses.

**Design**:

- Elements from shared components become `BasePage` properties
- Each `PageType` generates a subclass with page-specific locators
- `BasePage` gets `navigate()` method; subclasses override with
  specific URL
- Codegen reads `SiteModel.shared_components` and
  `SiteModel.page_types` — no direct access to `ExplorationResult`

**Files to modify**:

- `src/flowscout/codegen/page_objects.py` — generate `BasePage` +
  subclasses (Layer 3)
- Template logic: components with `frequency >= 0.8` → BasePage;
  others → subclass-level composition

**Generated output**:

```python
class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.nav = NavigationComponent(page)
        self.theme_dropdown = ThemeDropdown(page)

    def navigate(self, path: str) -> None:
        self.page.goto(path)
        self.page.wait_for_load_state("networkidle")

class MovieListingPage(BasePage):
    URL = "https://example.com/movies"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.movie_card = page.locator(".movie-card")
        self.search_input = page.locator("input[type='search']")
```

**Acceptance criteria**:

- [x] `BasePage` generated with shared locators + components
- [x] Each page type generates a subclass
- [x] No duplicated locators between base and subclass
- [x] Generated code is syntactically valid and importable
- [x] Codegen reads only from `SiteModel`, not `ExplorationResult`
      directly

### 2.4 Interaction pattern detection for POM methods

**Layer**: 2 (detection in Modeling) + 3 (method generation in
Generation)

When the explorer opens a dropdown and selects options, codegen
should produce `open()` / `close()` / `select(value)` methods — not
just `click()` calls.

**Patterns to detect** (Layer 2 — `modeling/components.py`):

| Interaction Pattern | Detected Via                            | Stored As                       |
| ------------------- | --------------------------------------- | ------------------------------- |
| Dropdown open/close | `DROPDOWN_TRIGGER` + `DROPDOWN_OPTION`  | `InteractionPattern.DROPDOWN`   |
| Tab switching       | `TAB` element type + DOM_CHANGE outcome | `InteractionPattern.TABS`       |
| Search submit       | `is_search` metadata + FILL + PRESS_KEY | `InteractionPattern.SEARCH`     |
| Form fill + submit  | `SUBMIT_FORM` with field_values         | `InteractionPattern.FORM`       |
| Pagination          | Pagination zone elements                | `InteractionPattern.PAGINATION` |
| Toggle              | CHECK/UNCHECK actions                   | `InteractionPattern.TOGGLE`     |

**Methods generated** (Layer 3 — `codegen/page_objects.py`):

| Pattern    | Generated Methods                    |
| ---------- | ------------------------------------ |
| DROPDOWN   | `open()`, `close()`, `select(value)` |
| TABS       | `switch_to(tab_name)`                |
| SEARCH     | `search(query)`                      |
| FORM       | `fill_and_submit(**fields)`          |
| PAGINATION | `next_page()`, `previous_page()`     |
| TOGGLE     | `toggle(name)`, `is_checked(name)`   |

**Files to create/modify**:

- `src/flowscout/modeling/components.py` — add
  `InteractionPattern` enum and detection logic (Layer 2)
- `src/flowscout/codegen/page_objects.py` — add pattern-based
  method generation (Layer 3)

**Acceptance criteria**:

- [x] Patterns detected in Layer 2 and stored on `SiteModel`
- [x] Methods generated in Layer 3 from `SiteModel` data
- [x] Dropdown triggers generate `open()` + `close()` +
      `select(value)`
- [x] Search inputs generate `search(query)` method
- [x] Forms generate `fill_and_submit()` with field parameters
- [x] Tabs generate `switch_to(tab_name)` method
- [x] Generated methods match Playwright API correctly

### 2.5 Locator stability scoring

**Layer**: 2 (Modeling)

Score each locator by its stability tier and surface this in reports.

**Scoring**:

| Tier | Selector Pattern              | Score |
| ---- | ----------------------------- | ----- |
| 1    | `#id`                         | 100   |
| 2    | `[data-testid]`, `[data-tab]` | 95    |
| 3    | `a[href]`                     | 85    |
| 4    | `[aria-label]`                | 80    |
| 5    | `[role]`                      | 70    |
| 6    | `[name]`                      | 65    |
| 7    | `input[type]`                 | 50    |
| 8    | `tag:nth-of-type(n)`          | 20    |

**Aggregate per page type**: average of all locator scores.

**Files to create/modify**:

- `src/flowscout/modeling/locators.py` — new: `score_locator()`,
  `score_page_type()`, locator recommendations (Layer 2)
- `src/flowscout/modeling/site_model.py` — add
  `locator_quality_score: float` to `PageType`, add
  `locator_recommendations: list[str]` to `SiteModel`
- `src/flowscout/reporting/html.py` — surface in dashboard (Layer 3)

**Acceptance criteria**:

- [x] Each element has a stability score (computed in Layer 2)
- [x] Each page type has an aggregate locator quality score on
      `SiteModel`
- [x] Dashboard shows "Locator Quality: 85% stable" per page type
- [x] Fragile locators flagged with recommendations
- [x] Scoring logic lives in `modeling/locators.py`, not in
      discovery

### 2.6 XPath fallback construction

**Layer**: 1 (Discovery — extends element capture) + 2 (Modeling —
decides which to prefer)

Add XPath as a fallback strategy for elements where CSS selectors
produce fragile nth-of-type paths.

**Files to modify**:

- `src/flowscout/js/discovery.ts` — add `getXPath()` function
  alongside `getSelector()` (Layer 1)
- `src/flowscout/discovery/elements.py` — add
  `xpath: str | None` field to `InteractiveElement` (Layer 1)
- `src/flowscout/modeling/locators.py` — add logic to prefer CSS
  when stable, flag XPath as alternative when CSS score < 50
  (Layer 2)
- `src/flowscout/codegen/page_objects.py` — use preferred locator
  from model (Layer 3)

**Acceptance criteria**:

- [x] Elements with fragile CSS selectors also have XPath
      alternatives captured in Layer 1
- [x] Layer 2 decides which locator to prefer based on stability
      score
- [x] POM generation uses the preferred locator from the model
- [x] XPath stored in element data for reporting

---

## Phase 3: Model-Based Testing

**Goal**: Turn the site model into a real MBT engine with graph
walking, coverage metrics, and standard exports. All work lives in
**Layer 3 (Generation)** — consuming the `SiteModel` from Layer 2.

### 3.1 Graph walker with coverage strategies

**Layer**: 3 (Generation)

Implement a `ModelWalker` that algorithmically traverses the site
model state machine.

**Design**:

```python
# mbt/walker.py (NEW — Layer 3)
class ModelWalker:
    def walk_edge_coverage(
        self, model: SiteModel,
    ) -> list[FlowScenario]:
        """Minimum set of paths covering every NavigationEdge."""

    def walk_state_coverage(
        self, model: SiteModel,
    ) -> list[FlowScenario]:
        """Minimum set of paths visiting every PageType."""

    def walk_random(
        self, model: SiteModel, steps: int = 20,
    ) -> FlowScenario:
        """Random walk for exploratory/fuzz testing."""

    def walk_all_paths(
        self, model: SiteModel, max_depth: int = 5,
    ) -> list[FlowScenario]:
        """All simple paths up to max_depth."""
```

**Implementation**:

- Build NetworkX DiGraph from `SiteModel.page_types` (nodes) and
  `SiteModel.navigation_edges` (edges)
- Edge coverage: Chinese Postman / Eulerian path algorithm
- **3.1 expansion**: use a directed CPP approximation per weakly
  connected component:
  - If component is strongly connected, balance in/out degree
    imbalances with min-cost shortest-path matching, then run
    Eulerian traversal.
  - If CPP preconditions fail, fall back to deterministic
    shortest-path stitching between uncovered transitions.
- State coverage: minimum spanning walk
- Random walk: weighted random selection (weight by
  `occurrence_count`)
- All paths: `nx.all_simple_paths()` with depth limit

**Key design point**: The walker reads **only** from `SiteModel`. It
never touches `ExplorationResult`. This is what makes it a proper
MBT tool — it works from the model, not from observed behavior.

**Files to create/modify**:

- `src/flowscout/mbt/walker.py` — new (Layer 3)
- `src/flowscout/mbt/__init__.py` — exports
- `src/flowscout/cli/generate.py` — add `--mbt` flag with strategy
  options (edge, state, random, all_paths)
- `src/flowscout/codegen/tests.py` — generate tests from walker
  output

**Acceptance criteria**:

- [ ] `walk_edge_coverage()` returns scenarios that collectively
      touch every `NavigationEdge`
- [ ] `walk_state_coverage()` returns scenarios visiting every
      `PageType`
- [ ] Coverage is verified: all edges/states accounted for
- [ ] Generated scenarios are valid `FlowScenario` objects
- [ ] Walker reads only from `SiteModel` (no `ExplorationResult`
      imports)
- [ ] Tests for walker correctness on known graphs

### 3.2 Coverage metrics and reporting

**Layer**: 3 (Generation) — consumes `SiteModel` + scenarios

Track and report explicit coverage of the site model.

**Design**:

```python
# mbt/coverage.py (NEW — Layer 3)
class ModelCoverage(BaseModel):
    state_coverage: float              # % of PageTypes covered
    edge_coverage: float               # % of NavigationEdges covered
    path_coverage: float               # % of unique paths exercised
    uncovered_states: list[str]        # PageType IDs not in scenarios
    uncovered_edges: list[tuple]       # (from, to, action) not covered
    coverage_matrix: dict              # PageType x ActionType matrix
```

**Files to create/modify**:

- `src/flowscout/mbt/coverage.py` — `ModelCoverage` computation
  (Layer 3)
- `src/flowscout/reporting/terminal.py` — print coverage metrics
- `src/flowscout/reporting/html.py` — coverage visualization

**Acceptance criteria**:

- [x] Coverage metrics computed for any set of scenarios against a
      model
- [x] Uncovered edges/states explicitly listed
- [x] Terminal shows: "Edge coverage: 85% (17/20 edges)"
- [x] HTML report has coverage matrix visualization

### 3.3 Standard MBT export formats

**Layer**: 3 (Generation)

Export the site model in formats consumable by external MBT tools.

**Formats**:

1. **GraphWalker JSON** — for the GraphWalker MBT tool
2. **DOT** — for Graphviz visualization
3. **Mermaid** — for documentation embedding

**Files to create**:

- `src/flowscout/mbt/exporters/graphwalker.py` (Layer 3)
- `src/flowscout/mbt/exporters/dot.py` (Layer 3)
- `src/flowscout/mbt/exporters/mermaid.py` (Layer 3)
- `src/flowscout/cli/generate.py` — add `--export` sub-command

**CLI**:

```bash
uv run flowscout generate model.json --export graphwalker
uv run flowscout generate model.json --export dot
uv run flowscout generate model.json --export mermaid
```

**Acceptance criteria**:

- [x] GraphWalker JSON output is valid and importable by GraphWalker
- [x] DOT output renders correctly with Graphviz
- [x] Mermaid output renders in GitHub Markdown
- [x] Edge labels include action type and occurrence count
- [x] All exporters read only from `SiteModel`

### 3.4 Guard conditions on transitions

**Layer**: 2 (Modeling — infer guards) + 3 (Generation — respect
guards)

Add preconditions to navigation edges, inferred from exploration
context.

**Design**:

```python
# On NavigationEdge (Layer 2 — modeling/site_model.py)
guards: list[str] = []             # ["requires_search_input"]
inferred_from: str = ""            # How the guard was detected
```

**Guard inference rules** (Layer 2):

- Edge only traversed after a FILL action → `requires_input`
- Edge only traversed from states with specific features →
  `requires_<feature>`
- Edge only traversed after SUBMIT_FORM →
  `requires_form_submission`

**Files to modify**:

- `src/flowscout/modeling/site_model.py` — add guard inference
  (Layer 2)
- `src/flowscout/mbt/walker.py` — respect guards during path
  generation (Layer 3)

**Acceptance criteria**:

- [ ] Guards inferred from exploration patterns (Layer 2)
- [ ] Walker respects guards (Layer 3)
- [ ] Guards visible in dashboard and export formats

---

## Phase 4: Dashboard Restructuring

**Goal**: Reshape the report from "exploration results viewer" to
"test automation accelerator." All work in **Layer 3 (Generation)**
— the dashboard reads from `SiteModel`.

### 4.1 Restructure tab navigation

Replace current 6 tabs with a structure aligned to the vision:

| Current     | New               | Purpose                                              |
| ----------- | ----------------- | ---------------------------------------------------- |
| Overview    | **Dashboard**     | Keep — refine with top issues callout                |
| Diagnostics | **Quality**       | Merge diagnostics + locator health + recommendations |
| Test Suites | **Test Flows**    | Show flow templates (deduplicated)                   |
| Elements    | **Page Objects**  | POM preview per page type                            |
| Model       | **Site Map**      | PageType-level state machine                         |
| All Actions | **Execution Log** | Keep as "Advanced"                                   |

**Key design point**: The report reads primarily from `SiteModel`
for structure (page types, edges, components, flow templates) and
from `ExplorationResult` for detail (screenshots, timing,
individual action results). This matches the layer architecture.

**Files to modify**:

- `src/flowscout/reporting/templates/report.html.j2`
- `src/flowscout/reporting/html.py`

**Acceptance criteria**:

- [ ] Tab names updated
- [ ] Navigation reflects new structure
- [ ] Report reads from `SiteModel` for structure data
- [ ] All existing data still accessible (nothing lost)

### 4.2 Page Objects tab

New tab showing POM previews for each page type.

**Content per page type card**:

- Class name (e.g., `MovieListingPage`)
- Archetype badge (LISTING, DETAIL, FORM, etc.)
- URL pattern
- Instance count ("seen 12 times")
- Locator quality score with color coding
- Expand to see:
  - Full locator table: selector, stability tier, zone, exercised
  - Code preview toggle: generated Python or TypeScript POM class
  - Recommendations: "Add data-testid to 3 elements"

**Files to modify**:

- `src/flowscout/reporting/templates/report.html.j2` — new section
- `src/flowscout/reporting/html.py` — add POM preview data
- `src/flowscout/codegen/page_objects.py` — expose generated code
  as string for embedding in report

**Acceptance criteria**:

- [ ] Each page type shown as a card with key metrics
- [ ] Locator table with stability scoring
- [ ] Code preview toggleable (Python/TypeScript)
- [ ] Recommendations for improving locator quality

### 4.3 Site Map tab with MBT visualization

Replace raw exploration graph with PageType-level state machine.

**Visualization**:

- Nodes = PageTypes (5-8 nodes, not 50 raw states)
- Node size proportional to instance count
- Node color by archetype
- Edges = NavigationEdges with action label + occurrence count
- Edge thickness proportional to occurrence count
- Coverage overlay toggle: uncovered edges shown dashed/red
- Click node → Page Objects tab for that page type
- Click edge → flow template using that transition

**Files to modify**:

- `src/flowscout/reporting/html.py` — generate site-model-level
  graph data
- `src/flowscout/reporting/templates/report.html.j2` — update graph
  section

**Acceptance criteria**:

- [ ] Graph shows PageTypes as nodes (not raw states)
- [ ] Edge labels show action + count
- [ ] Coverage overlay toggle works
- [ ] Clicking nodes/edges navigates to relevant detail

### 4.4 Flow Templates in Test Flows tab

Replace raw flow list with deduplicated flow templates.

**Structure**:

- Flow template card: name, occurrence count, stability score, tags
- Expand: representative flow with full step timeline
- "Show all instances" toggle to see individual flows
- Filter by: template type, stability, tags

**Files to modify**:

- `src/flowscout/reporting/templates/report.html.j2`
- `src/flowscout/reporting/html.py`

**Acceptance criteria**:

- [ ] Flow templates shown with occurrence counts
- [ ] Representative flow expandable with full details
- [ ] Individual instances accessible via toggle
- [ ] Filtering works by template/stability/tags

### 4.5 Quality tab with actionable recommendations

Merge diagnostics with locator health and provide actionable items.

**Sections**:

1. **Locator Health**: fragile selectors ranked by page, with
   "add data-testid" recommendations
2. **Flaky Actions**: transitions with inconsistent outcomes
3. **Low-Stability Steps**: unreliable interactions
4. **Improvement Recommendations**: prioritized list of changes

**Files to modify**:

- `src/flowscout/reporting/templates/report.html.j2`
- `src/flowscout/reporting/html.py`

**Acceptance criteria**:

- [ ] Locator health visible per page type
- [ ] Recommendations are actionable
- [ ] Flaky and low-stability items surfaced prominently
- [ ] Items link to relevant page object / flow detail

### 4.6 Dashboard refinements

Surface top issues directly on the landing page.

**Add to Overview**:

- "Top Issues" callout: 3-5 worst locator health / flaky items
- Site structure summary: "5 page types, 12 navigation paths,
  3 flow templates"
- Quick link to Page Objects tab

**Files to modify**:

- `src/flowscout/reporting/templates/report.html.j2`
- `src/flowscout/reporting/html.py`

**Acceptance criteria**:

- [ ] Top issues visible on dashboard without clicking into tabs
- [ ] Site structure summary shows page type count, edge count,
      template count
- [ ] Click-through to relevant tabs works

---

## Phase 5: Polish and Validation

**Goal**: Ensure generated output is correct and the framework is
production-ready.

### 5.1 Generated test validation

**Layer**: 3 (Generation)

Add round-trip test: generate POM + tests → lint → verify
importable.

**Files to create/modify**:

- `tests/test_codegen_validation.py` — new test file
- `src/flowscout/codegen/validator.py` — syntax + import checking

**Acceptance criteria**:

- [ ] Generated Python code passes `py_compile`
- [ ] Generated TypeScript code passes `tsc --noEmit`
- [ ] POM imports in scenario tests resolve correctly
- [ ] Locator API usage matches Playwright's actual API

### 5.2 Merge element catalogs across page type instances

**Layer**: 2 (Modeling)

POM classes should include locators from ALL instances of a page
type, not just the representative.

**Files to modify**:

- `src/flowscout/modeling/site_model.py` — merge catalogs in
  `_build_page_types()`

**Acceptance criteria**:

- [ ] POM classes include locators found on any instance
- [ ] No duplicate locators
- [ ] Element count reflects union across instances

### 5.3 Cross-run comparison in reports

**Layer**: 3 (Generation) + Storage (cross-cutting)

Enable comparison between exploration runs to detect regressions.

**Files to modify**:

- `src/flowscout/storage/db.py` — add comparison queries
- `src/flowscout/reporting/html.py` — add diff section to dashboard

**Acceptance criteria**:

- [ ] Dashboard shows "3 new pages, 1 disappeared, 2 changed
      locators"
- [ ] Changed items highlighted in relevant tabs
- [ ] Works when previous run exists in database

### 5.4 Parametric test generation

**Layer**: 2 (Modeling — detect data variants) + 3 (Generation —
produce parameterized tests)

When flow templates have multiple instances with varying data,
generate parameterized tests.

**Files to modify**:

- `src/flowscout/modeling/flows.py` — extract data variants from
  flow template instances (Layer 2)
- `src/flowscout/codegen/tests.py` — generate
  `@pytest.mark.parametrize` (Layer 3)

**Acceptance criteria**:

- [ ] 10 movie detail flows → 1 parametrized test with 10 data sets
- [ ] Parameters include URL, content identifiers
- [ ] Generated tests are syntactically valid

---

## Milestone Summary

| Phase | ID   | Milestone                  | Layer  | Key Deliverable                   | Depends On | Status |
| ----- | ---- | -------------------------- | ------ | --------------------------------- | ---------- | ------ |
| 1     | 1.1  | Smart default              | CLI    | `--smart` on by default           | —          | DONE   |
| 1     | 1.2  | Verdict simplification     | L1+L3  | Observation model                 | —          | DONE   |
| 1     | 1.3  | Codegen consolidation      | L3     | POM + scenarios primary           | —          | DONE   |
| 1     | 1.4  | Three-layer boundary       | All    | `modeling/` package, CLI pipeline | 1.1–1.3    | DONE   |
| 1     | 1.5  | Serialization contracts    | L1+L2  | Versioned schemas                 | 1.4        | DONE   |
| 1b    | 1b.1 | Blocked page detection     | L1     | Block reason classification       | 1.5        | —      |
| 1b    | 1b.2 | Browser stealth defaults   | L1     | Anti-detection baseline           | 1b.1       | —      |
| 1b    | 1b.3 | Persistent browser context | L1+CLI | Cookie/storage persistence        | 1b.2       | —      |
| 1b    | 1b.4 | CDP connection             | L1+CLI | Connect to existing browser       | 1b.2       | —      |
| 2     | 2.1  | Flow deduplication         | L2     | Flow templates                    | 1.4        | DONE   |
| 2     | 2.2  | Component extraction       | L2     | Shared components                 | 1.4        | DONE   |
| 2     | 2.3  | POM inheritance            | L3     | BasePage + subclasses             | 2.2        | DONE   |
| 2     | 2.4  | Interaction patterns       | L2+L3  | Domain-specific methods           | 2.2        | DONE   |
| 2     | 2.5  | Locator scoring            | L2     | Stability tiers + scores          | 1.4        | DONE   |
| 2     | 2.6  | XPath fallback             | L1+L2  | Alternative selectors             | 2.5        | DONE   |
| 3     | 3.1  | Graph walker               | L3     | MBT coverage strategies           | 2.1        | —      |
| 3     | 3.2  | Coverage metrics           | L3     | State/edge/path coverage          | 3.1        | —      |
| 3     | 3.3  | MBT export                 | L3     | GraphWalker, DOT, Mermaid         | 3.1        | —      |
| 3     | 3.4  | Guard conditions           | L2+L3  | Inferred preconditions            | 3.1        | —      |
| 4     | 4.1  | Tab restructure            | L3     | New IA                            | 2.x        | —      |
| 4     | 4.2  | Page Objects tab           | L3     | POM preview + quality             | 2.3, 2.5   | —      |
| 4     | 4.3  | Site Map tab               | L3     | MBT state machine viz             | 3.2        | —      |
| 4     | 4.4  | Flow Templates tab         | L3     | Deduplicated flow display         | 2.1        | —      |
| 4     | 4.5  | Quality tab                | L3     | Actionable recommendations        | 2.5        | —      |
| 4     | 4.6  | Dashboard refinements      | L3     | Top issues on landing             | 4.5        | —      |
| 5     | 5.1  | Codegen validation         | L3     | Round-trip verification           | 2.3        | —      |
| 5     | 5.2  | Catalog merging            | L2     | Union of locators                 | 2.2        | —      |
| 5     | 5.3  | Cross-run comparison       | L3     | Regression detection              | 3.2        | —      |
| 5     | 5.4  | Parametric tests           | L2+L3  | Data-driven generation            | 2.1        | —      |

---

## Testing Requirements

Every milestone must:

1. **Pass all existing tests** (no regressions)
2. **Add tests for new functionality** with meaningful assertions
3. **Pass linting**: `uv run lintro chk`
4. **Include edge case coverage**: empty inputs, single-page sites,
   sites with no forms, etc.
5. **Be verified against the turbo-themes test site**:
   `https://lgtm-hq.github.io/turbo-themes/`
6. **Respect layer boundaries**: no imports crossing layer
   boundaries in the wrong direction

---

## Milestone Assessment Prompt

Use the following prompt after completing each milestone to evaluate
progress. Provide it to an agent along with the milestone ID (e.g.,
"2.1") and it will assess implementation quality against the plan.

````markdown
## Milestone Assessment: [MILESTONE_ID]

You are evaluating the implementation of milestone [MILESTONE_ID]
from the Flowscout ROADMAP.md. Your job is to assess whether the
implementation meets the acceptance criteria, follows project
standards, and maintains alignment with the overall vision.

### Instructions

1. **Read ROADMAP.md** at the project root to understand the full
   milestone requirements, acceptance criteria, and dependencies.

2. **Read CLAUDE.md** for project context and coding standards.

3. **Check each acceptance criterion** by reading the modified files
   and verifying the implementation:
   - For each criterion, report: PASS, PARTIAL, or FAIL
   - For PARTIAL/FAIL, explain what's missing or incorrect

4. **Run the test suite**: `uv run pytest tests/ -v`
   - Report: total tests, passed, failed, errors
   - Flag any new test files added for this milestone
   - Flag any "nothing burger" tests that don't meaningfully
     validate

5. **Run linting**: `uv run lintro chk`
   - Report: clean or list violations

6. **Verify layer boundaries**:
   - Check imports in all modified files
   - Confirm no Layer 1 module imports from `modeling/` or
     `codegen/`
   - Confirm no Layer 2 module imports from `codegen/`, `mbt/`, or
     `reporting/`
   - Report any violations

7. **Verify against turbo-themes**: If applicable, run
   `uv run flowscout explore https://lgtm-hq.github.io/turbo-themes/ --generate-tests`
   and check that the milestone's feature works on a real site.

8. **Architecture alignment check**:
   - Does this implementation move toward the vision described in
     ROADMAP.md's opening section?
   - Does it respect the three-layer pipeline architecture?
   - Are there any shortcuts taken that will create tech debt?
   - Does the implementation follow existing patterns in the
     codebase?
   - Are there any unintended side effects on other modules?

9. **Dependency check**:
   - Were all prerequisite milestones completed before this one?
   - Does this milestone unblock dependent milestones as expected?

### Output Format

```
## Milestone [ID]: [Title]
Status: COMPLETE | PARTIAL | BLOCKED

### Acceptance Criteria
- [ ] Criterion 1: PASS/PARTIAL/FAIL — notes
- [ ] Criterion 2: PASS/PARTIAL/FAIL — notes
...

### Test Results
- Total: X | Passed: X | Failed: X | Errors: X
- New test files: list
- Test quality: assessment

### Lint Results
- Status: clean / X violations

### Layer Boundary Check
- Violations: none / list
- Import direction: correct / issues

### Integration Verification
- Ran against turbo-themes: yes/no
- Result: description

### Architecture Alignment
- Vision alignment: HIGH/MEDIUM/LOW — notes
- Three-layer compliance: FULL/PARTIAL/VIOLATION — notes
- Tech debt introduced: none / description
- Pattern adherence: notes

### Dependencies
- Prerequisites met: yes/no
- Unblocks: list of milestone IDs

### Recommendations
- Numbered list of improvements or follow-ups

### Overall Score: X/10
```
````

---

## How to Use This Document

1. **Between chats**: Reference this file by path
   (`/Users/eiteldagnin/Code/ui-framework/ROADMAP.md`) or instruct
   the agent to read it at the start of each session.

2. **Starting a milestone**: Tell the agent:
   "Read ROADMAP.md and implement milestone [X.Y]."

3. **After completing a milestone**: Tell the agent:
   "Read ROADMAP.md and run the milestone assessment for [X.Y]."

4. **Tracking progress**: Check off acceptance criteria as they're
   completed. The milestone summary table gives a bird's-eye view.

5. **Adjusting the plan**: This document is living — update it as
   requirements evolve or as implementation reveals new needs.

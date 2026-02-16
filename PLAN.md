# Flowscout V2 — Implementation Plan

## Context

Flowscout is an LLM-free automated web path exploration framework. V1 produces
an interactive HTML report from Priority-BFS crawling of interactive elements.
V2 transforms it into a **comprehensive test automation platform** that:

1. Catalogs **all** elements on every page (not just interactive ones)
2. Generates **framework-agnostic Page Object Models** as drop-in files
3. Produces a **SolidJS SPA dashboard** instead of a monolithic Jinja2 template
4. Exposes an optional **FastAPI API layer** (CLI-first workflow)
5. Feeds **GraphWalker MBT** with richer models
6. Eventually integrates **LLM intelligence** (future phase)

### Technology choices

| Layer      | Technology                                                   |
| ---------- | ------------------------------------------------------------ |
| Frontend   | SolidJS + Vite + Bun + turbo-themes CSS                      |
| API        | FastAPI + SQLite (existing)                                  |
| Config     | `.crawl-config` (TOML) with Pydantic validation              |
| POM output | Actual `.py` / `.ts` files, framework-agnostic with adapters |

### Issue tracker

| Phase                   | Issue                                                  | Depends on  |
| ----------------------- | ------------------------------------------------------ | ----------- |
| 1. Full Element Catalog | [#1](https://github.com/lgtm-hq/ui-framework/issues/1) | —           |
| 2. Config Validation    | [#2](https://github.com/lgtm-hq/ui-framework/issues/2) | Phase 1     |
| 3. SolidJS Dashboard    | [#3](https://github.com/lgtm-hq/ui-framework/issues/3) | Phase 1     |
| 4. POM Architecture     | [#4](https://github.com/lgtm-hq/ui-framework/issues/4) | Phase 1     |
| 5. FastAPI API          | [#5](https://github.com/lgtm-hq/ui-framework/issues/5) | Phases 1-4  |
| 6. GraphWalker          | [#6](https://github.com/lgtm-hq/ui-framework/issues/6) | Phases 1, 4 |
| 7. LLM Integration      | [#7](https://github.com/lgtm-hq/ui-framework/issues/7) | All         |

---

## Phase 1: Full Element Catalog (Foundation)

**Goal**: Extend crawling to catalog ALL elements per page with rich metadata.

### Problem

`discover_elements()` in `src/flowscout/discovery/elements.py` only finds interactive
elements. Non-interactive elements (headings, paragraphs, images, labels, containers)
are invisible to the crawl output. `page_analysis.js` already collects `element_catalog`
and `content_metrics` but this data is only used by smart-mode planning, never persisted.

### Changes

### 1.1 New `PageInventory` model

**File**: `src/flowscout/core/types.py` or new `core/models.py`

```python
class InventoryElement(BaseModel):
    selector: str
    xpath: str | None = None
    dom_id: str | None = None
    tag: str
    element_type: str          # "heading", "paragraph", "image", "link", "button", ...
    zone: str = ""             # "nav", "main", "footer", "sidebar", "header"
    label: str = ""
    visible_text: str = ""
    aria_label: str | None = None
    aria_role: str | None = None
    href: str | None = None
    src: str | None = None
    name: str | None = None
    input_type: str | None = None
    is_interactive: bool = False
    is_visible: bool = True
    bounding_box: BoundingBox | None = None
    computed_styles: dict[str, str] = Field(default_factory=dict)
    parent_selector: str | None = None
    parent_tag: str | None = None
    data_attributes: dict[str, str] = Field(default_factory=dict)
    locator_score: float = 0.0
    preferred_selector: str = ""
    preferred_strategy: str = ""

class FormStructure(BaseModel):
    form_selector: str
    action: str | None = None
    method: str = "GET"
    fields: list[FormField] = Field(default_factory=list)
    submit_selector: str | None = None

class FormField(BaseModel):
    selector: str
    name: str | None = None
    input_type: str = "text"
    label: str = ""
    is_required: bool = False
    placeholder: str | None = None
    options: list[str] = Field(default_factory=list)
    validation_pattern: str | None = None

class PageInventory(BaseModel):
    url: str
    state_id: str
    elements: list[InventoryElement] = Field(default_factory=list)
    forms: list[FormStructure] = Field(default_factory=list)
    content_metrics: ContentMetrics | None = None
    zone_hints: ZoneHints | None = None
    structural_skeleton: str = ""
    timestamp: str = ""
```

### 1.2 Extend JS collection

**File**: `src/flowscout/js/page_analysis.ts`

- Add `visible_text` (trimmed to 200 chars)
- Add `computed_styles` (font-size, color, display, position)
- Add `parent_selector` and `parent_tag`
- Add `src` for images and media
- Form structure with field-level detail (validation patterns, labels, required)

### 1.3 New `discover_page_inventory()` function

**File**: `src/flowscout/discovery/inventory.py` (new)

Calls `page_analysis.js` and maps the returned `element_catalog` + `content_metrics`
into `PageInventory`. Runs always, not just in smart mode.

### 1.4 Integrate into Navigator

**File**: `src/flowscout/core/navigator.py`

In `_explore_state`, after `discover_elements()`, also call `discover_page_inventory()`.
Store in `ExplorationResult.page_inventories: dict[str, PageInventory]`.

### 1.5 Persist inventory in ExplorationResult

**File**: `src/flowscout/analysis/graph.py`

Add `page_inventories` field to `ExplorationResult`. Bump `schema_version`.

### 1.6 Configuration defaults

| Feature                       | Default   | Configurable                      |
| ----------------------------- | --------- | --------------------------------- |
| Interactive element discovery | Always on | No                                |
| Full page inventory           | Always on | No                                |
| Form structure catalog        | Always on | No                                |
| Computed styles               | Off       | Yes (`collect_computed_styles`)   |
| Bounding boxes                | On        | Yes (`collect_bounding_boxes`)    |
| Screenshots                   | On        | Yes (existing `take_screenshots`) |

---

## Phase 2: Configuration Validation

**Goal**: Add Pydantic validation to `.crawl-config` on load.

### 2.1 CrawlConfig Pydantic model

**File**: `src/flowscout/cli/config.py` (extend)

Full Pydantic model with constraints (e.g. `max_depth` 1-20, `max_states` 1-500),
enum validation for `input_profile` / `outcome_mode` / `link_scope_mode`, timing
minimums, and new `allowed_domains: list[str]` for microservices.

### 2.2 Validation on load

`load_config()` parses TOML, validates with Pydantic, raises friendly errors.

### 2.3 Domain allowlist

**File**: `src/flowscout/discovery/actions.py`

Modify `_is_external_origin_link()` and `_actions_for_element()` to respect
`allowed_domains` for multi-domain microservices crawling.

---

## Phase 3: SolidJS SPA Dashboard

**Goal**: Replace monolithic Jinja2 report with a SolidJS SPA.

### Architecture

```text
reports/<date>/<time>/
  index.html          ← SolidJS SPA (all JS/CSS inlined via Vite)
  report-data.json    ← Serialized exploration data
  result.json         ← Full ExplorationResult (existing)
  screenshots/        ← State screenshots (existing)
```

### 3.1 Report data contract

**File**: `src/flowscout/reporting/data_contract.py` (new)

`ReportData` Pydantic model: `meta`, `summary`, `pages`, `flows`, `graph`, `coverage`, `test_cases`.

### 3.2 Frontend SPA

**Directory**: `src/flowscout/reporting/dashboard/`

SolidJS + Vite + turbo-themes. Components: `Summary`, `PageList`, `PageDetail`,
`FlowView`, `GraphView`, `Coverage`, `TestCases`, `ElementTable`, `Timeline`.

**Three-tier information architecture:**

1. **Summary** — one-glance crawl health
2. **Detail** — per-page element inventory, action outcomes, flow steps
3. **Raw** — full JSON data, debug trace, DOM snapshots

### 3.3 Build integration

**File**: `src/flowscout/reporting/build.py` (new)

Vite build produces self-contained `index.html`. Data injected inline via
`<script>window.__REPORT_DATA__ = {...}</script>`.

### 3.4 Report generator rewrite

**File**: `src/flowscout/reporting/html.py` (rewrite from 2291 lines to ~50)

Thin function: build report data, load dashboard shell, inject data.

### 3.5 Styling

turbo-themes with dark mode support.

---

## Phase 4: Framework-Agnostic POM Architecture

**Goal**: Generate POMs as actual drop-in files for any test framework.

### Pipeline

```text
PageInventory → PageObjectModel (intermediate) → Adapter → Output files
```

### 4.1 Intermediate POM model

**File**: `src/flowscout/codegen/pom_model.py` (new)

`PageObjectModel`, `POMElement`, `POMAction`, `POMAssertion` — framework-agnostic
intermediate representation.

### 4.2 POM builder

**File**: `src/flowscout/codegen/pom_builder.py` (new)

`build_page_objects()` from SiteModel + PageInventory.

### 4.3 Framework adapters

**Directory**: `src/flowscout/codegen/adapters/`

Abstract `POMAdapter` with `render_page_object()`, `render_base_page()`, `file_extension()`.
Concrete: `PlaywrightPythonAdapter`, `PlaywrightTSAdapter`. Future stubs: Selenium, Cypress.

### 4.4 File writer

**File**: `src/flowscout/codegen/writer.py` (new)

`write_page_objects()` writes POM files to disk.

### 4.5 Refactor existing codegen

**File**: `src/flowscout/codegen/page_objects.py`

Extract existing Playwright generation into adapter classes.

---

## Phase 5: FastAPI API Layer

**Goal**: Optional API server for cross-run analysis.

### 5.1 FastAPI application

**File**: `src/flowscout/serve/api.py` (new)

Endpoints: runs CRUD, page inventories, flows, graph data, coverage, report data
(same contract as SPA), async exploration trigger, cross-run comparison.

### 5.2 Database schema extension

**File**: `src/flowscout/storage/db.py`

Add tables: `page_inventories`, `form_structures`, `pom_snapshots`.

### 5.3 CLI integration

`flowscout serve [--port 8765]` starts the API server.

### 5.4 Auto-generated docs

Pydantic response models for all endpoints. FastAPI provides `/docs` and `/redoc`.

---

## Phase 6: GraphWalker Integration Improvements

**Goal**: Feed GraphWalker with richer models, bridge to POM actions.

### 6.1 Enriched model export

**File**: `src/flowscout/mbt/exporters/graphwalker.py`

Add element inventory per vertex, form field data for data-driven edges,
shared component markers.

### 6.2 Test sequence generation

**File**: `src/flowscout/mbt/walker.py`

`generate_test_sequences()` outputs sequences mapping to POM action methods.

### 6.3 Coverage model alignment

Element-level coverage tracking aligned with `PageInventory`.

---

## Phase 7: LLM Integration (Future)

**Status**: Deferred — placeholder only. No code changes.

Integration points to design for:

- Smart mode decisions (`src/flowscout/smart/`)
- Element semantic classification
- Test case naming and description
- Exploration strategy optimization
- Context-aware form filling

---

## Implementation Order

```text
Phase 1: Full Element Catalog          ← Everything depends on this
  |
  ├─ Phase 2: Config Validation        ← Quick win, needed for new options
  |
  ├─ Phase 3: SolidJS Dashboard        ← Needs PageInventory data
  |     (parallel)
  ├─ Phase 4: POM Architecture         ← Needs PageInventory data
  |
  └─ Phase 5: FastAPI API              ← Needs new data models
      └─ Phase 6: GraphWalker          ← Needs enriched models
          └─ Phase 7: LLM             ← Future
```

---

## Critical files

| File                                         | Change                                               |
| -------------------------------------------- | ---------------------------------------------------- |
| `src/flowscout/core/types.py`                | `InventoryElement`, `FormStructure`, `PageInventory` |
| `src/flowscout/js/page_analysis.ts`          | Extend element catalog                               |
| `src/flowscout/discovery/inventory.py`       | New: page inventory discovery                        |
| `src/flowscout/core/navigator.py`            | Integrate inventory into exploration                 |
| `src/flowscout/analysis/graph.py`            | `page_inventories` on `ExplorationResult`            |
| `src/flowscout/cli/config.py`                | `CrawlConfig` Pydantic model                         |
| `src/flowscout/discovery/actions.py`         | Domain allowlist                                     |
| `src/flowscout/reporting/html.py`            | Rewrite as SPA data injector                         |
| `src/flowscout/reporting/data_contract.py`   | New: `ReportData` contract                           |
| `src/flowscout/reporting/dashboard/`         | New: SolidJS SPA                                     |
| `src/flowscout/codegen/pom_model.py`         | New: intermediate POM                                |
| `src/flowscout/codegen/pom_builder.py`       | New: POM builder                                     |
| `src/flowscout/codegen/adapters/`            | New: framework adapters                              |
| `src/flowscout/codegen/page_objects.py`      | Refactor to adapters                                 |
| `src/flowscout/serve/api.py`                 | New: FastAPI app                                     |
| `src/flowscout/storage/db.py`                | Schema extension                                     |
| `src/flowscout/mbt/exporters/graphwalker.py` | Enriched export                                      |

---

## Verification

| Phase | Test                                                                                      |
| ----- | ----------------------------------------------------------------------------------------- |
| 1     | `flowscout explore <url>` produces `result.json` with `page_inventories`. All tests pass. |
| 2     | Invalid `.crawl-config` produces clear errors. `allowed_domains` filters correctly.       |
| 3     | `report.html` opens as self-contained SPA. Three tiers work. No external deps.            |
| 4     | `flowscout generate --format playwright-python` produces drop-in POM files.               |
| 5     | `flowscout serve` starts. `/docs` shows endpoints. `/api/runs` returns data.              |
| 6     | GW export includes inventories. Test sequences map to POM methods.                        |

```bash
uv run pytest tests/ -v      # Full test suite
uv run lintro chk             # Lint check
```

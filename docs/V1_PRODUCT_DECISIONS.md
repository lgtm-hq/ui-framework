# V1 Product Decisions (Deterministic, Local-First)

This document captures agreed V1 defaults and explains how they work.  
These decisions are intended to keep the framework deterministic, security-first, and useful for QA/SDET/Dev teams without AI dependencies.

## V1 Success Definition

For a new site, the target outcome is:

- within about 30 minutes, produce a trustworthy site model,
- generate runnable tests and page objects,
- provide human-readable evidence and reports.

## Target Users (V1)

- QA engineers
- SDETs
- Developers

Future (post-V1): AI-assisted workflows for non-technical users, built on top of deterministic artifacts.

## Coverage Goal (V1)

- default quality target: **80%** meaningful exploration coverage.

Coverage should include:

- interactive elements identified per page,
- discovered outgoing paths from each state,
- scenario/path coverage across N-step traversals,
- transition/edge discovery completeness.

## State Identity Strategy

V1 state identity uses three layers so equivalent screens map together while meaningful UI state changes still split correctly.

1. `route_key`: normalized path pattern.
2. `view_key`: `route_key + dom_structure_hash + primary_heading`.
3. `context_key`: `view_key + ui_state_markers` (active tab, open modal, wizard step).

This prevents cosmetic drift from creating false new states, while preserving functional UI context.

### Query Parameter Rules

Only keep query params that change page meaning. Ignore tracking/session volatility.

Typical keep list:

- `page`
- `sort`
- `filter`
- `category`
- `tab`
- `view`
- `q`
- `lang`

Typical ignore list:

- `utm_*`
- `gclid`
- `fbclid`
- `session`, `sid`
- `token`, `auth`
- `ts`, `_`
- cache-busting variants

Example:

- input URL: `/products?category=shoes&page=2&sort=price_asc&utm_source=google`
- identity-relevant query: `category=shoes&page=2&sort=price_asc`
- ignored query: `utm_source=google`

Implementation config fields:

- `FingerprintConfig.query_allowlist`
- `FingerprintConfig.ignore_url_params`
- `FingerprintConfig.ignore_url_param_patterns`

## Input Generation Profiles

Input generation must be deterministic and safety-oriented.

### `safe` (default)

- non-destructive values,
- valid data formats,
- no finalizing submissions.

Examples:

- email: `qa.user@example.com`
- quantity: `1`
- name: `Automation Test`

### `contextual`

- derives values from field hints (`name`, `placeholder`, label text, type),
- still constrained to safe behavior.

Examples:

- `zip` field gets zip-format data,
- `date` field gets valid ISO date,
- `phone` field gets a stable synthetic number.

### `negative` (opt-in)

- boundary and invalid values for validation coverage,
- disabled by default to reduce unintended side effects.

Examples:

- malformed email,
- empty required field,
- out-of-range numeric values.

## Non-Destructive Action Policy

V1 explorer must avoid concrete or irreversible operations by default.

Do not auto-execute actions such as:

- purchase/checkout/place order,
- destructive deletes,
- account creation that triggers external side effects,
- final submission flows that commit data.

Require explicit allowlisting to execute high-impact actions.

## Evidence Defaults

V1 evidence behavior:

- screenshots: **on by default**,
- video capture: **off by default**.

For each action screenshot:

- visually highlight the interacted element (bounding box/overlay),
- store linked metadata (action ID, selector, state ID, timestamp),
- include reason codes for outcomes (`success`, `no_change`, `validation_error`, `execution_error`).

This makes findings trustworthy for both technical and product stakeholders.

## Tenant / Environment Isolation

Storage layout should be isolated by:

1. domain,
2. environment under domain (`dev`, `staging`, `prod`, etc.),
3. timestamped run directory.

Example shape:

```text
reports/
  <domain>/
    <env>/runs/
      <yyyy-mm-dd_hh.mm.ss>/
```

## AI Boundary (Post-V1)

AI should not replace deterministic crawling, classification, or evidence capture.

Approved future role for AI:

- analyze deterministic artifacts to identify likely coverage gaps,
- propose additional candidate flows and edge cases,
- prioritize follow-up tests based on observed risk patterns.

Deterministic runtime remains the source of truth.

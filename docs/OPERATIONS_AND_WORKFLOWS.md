# Operations and Workflows

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Core Run Commands

Baseline exploration (safe defaults):

```bash
uv run flowscout explore https://example.com
```

Full V1 run (site model + generated tests):

```bash
uv run flowscout explore https://example.com \
  --smart \
  --generate-tests \
  --environment dev
```

Regenerate tests from an existing run artifact:

```bash
uv run flowscout generate reports/<domain>/<env>/runs/<timestamp>/result.json
```

Show historical reliability summary:

```bash
uv run flowscout reliability --url https://example.com
```

Build a benchmark snapshot from run artifacts:

```bash
uv run flowscout benchmark reports/<domain>/<env>/runs/<timestamp>/result.json
```

## Safety Defaults and Overrides

`flowscout explore` is non-destructive by default:

- high-impact actions are blocked,
- submit actions are blocked,
- screenshots are enabled and highlighted by default.

Use these controls explicitly:

- `--allow-form-submits`:
  enable submit actions only for controlled test environments.
- `--no-enforce-non-destructive`:
  disables high-impact blocking; use only with explicit approval in isolated environments.
- `--input-profile <safe|contextual|negative>`:
  controls generated input behavior.

## Auth and Secret Handling

V1 design is reference-based for credentials:

- provide secret references via environment variables or local secret files,
- never persist raw secrets in generated artifacts,
- keep auth/session setup deterministic and reproducible.

Recommended pattern:

1. Export credentials into env vars before run.
2. Configure the target login path or pre-auth bootstrap flow.
3. Verify generated evidence does not expose sensitive values.

## Run Tuning for V1 Target (80% Coverage)

Main levers:

- `--max-depth`: traversal depth.
- `--max-states`: unique state cap.
- `--max-actions`: actions attempted per state.
- `--timeout`: navigation timeout.
- `--strategy priority`: prefers discovery-efficient actions.

Example:

```bash
uv run flowscout explore https://example.com \
  --smart \
  --generate-tests \
  --max-depth 4 \
  --max-states 120 \
  --max-actions 25 \
  --timeout 12000
```

## Output Isolation and Layout

Runs are isolated by domain and environment:

```text
reports/<domain>/<environment>/runs/<timestamp>/
  report.html
  result.json
  evidence/actions/
  site_model.json
  tests.py
  pom_tests.py
  scenario_tests.py
  pages/
```

## Evidence and Reliability Signals

For each recorded step:

- screenshot evidence path (default on),
- highlighted interacted element,
- confidence score + reason,
- explicit `LOW_CONFIDENCE` flag in generated tests when confidence < `0.60`,
- trace comment linking generated step to the source graph edge (`action_id`, `source`, `target`, `outcome`).

## Troubleshooting

Low coverage (<80%):

1. Increase `--max-depth` and `--max-states`.
2. Raise `--max-actions` for interaction-heavy pages.
3. Confirm auth succeeds before exploration begins.

Too many `no_change` or low-confidence transitions:

1. Increase `--timeout`.
2. Run headed mode (`--no-headless`) for dynamic UI diagnosis.
3. Inspect selectors in generated POM and evidence screenshots.

Unexpected risky interactions:

1. Keep `--enforce-non-destructive` enabled.
2. Remove `--allow-form-submits` unless required by test scope.
3. Add allowlist/denylist policy rules for target app patterns.

## Recommended Team Workflow

1. Run baseline exploration in `dev` with safety defaults.
2. Review `report.html`, `result.json`, and screenshot evidence.
3. Run smart generation (`--smart --generate-tests`) for POM/scenario suites.
4. Track reliability over repeated runs (`flowscout reliability`).
5. Record baseline metrics in `docs/V1_BASELINE_BENCHMARKS.md`.
6. Promote to `staging` environment workspace and compare drift before release.

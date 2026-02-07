set shell := ["zsh", "-cu"]

default:
  @just --list

# Run a crawl against a URL with .crawl-config defaults.
crawl url:
  uv run flowscout explore "{{url}}" --max-depth 2 --max-states 30 --max-actions 15 --timeout 10000 --screenshot

# Run a crawl in headed (visible browser) mode.
crawl-headed url:
  uv run flowscout explore "{{url}}" --max-depth 2 --max-states 30 --max-actions 15 --timeout 10000 --screenshot --no-headless

# Export history snapshot, optionally filtered by URL.
history url="":
  #!/usr/bin/env zsh
  if [[ -z "{{url}}" ]]; then
    uv run flowscout history
  else
    uv run flowscout history --url "{{url}}"
  fi

# Open the most recent HTML report in the browser.
report:
  uv run flowscout serve "$(find reports -name 'report.html' | sort | tail -1)"

# Start the report UI dev server.
report-ui:
  cd report-ui && bun run dev

# Build the report UI for production.
report-ui-build:
  cd report-ui && bun run build

# Compile TypeScript browser scripts to JS.
build-js:
  cd src/flowscout/js && bunx tsc -p tsconfig.json

# Install all project dependencies.
setup:
  uv sync --extra dev
  uv run playwright install chromium
  cd report-ui && bun install

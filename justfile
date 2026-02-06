set shell := ["zsh", "-cu"]

default:
  @just --list

# Run a crawl against a URL using defaults from .crawl-config.
crawl url:
  uv run ui-flow crawl --url "{{url}}" --crawl-config .crawl-config

# Run a crawl in headed (visible browser) mode.
crawl-headed url:
  uv run ui-flow crawl --url "{{url}}" --crawl-config .crawl-config --headed

# Export history snapshot, optionally filtered by URL.
history url="":
  #!/usr/bin/env zsh
  if [[ -z "{{url}}" ]]; then
    uv run ui-flow history
  else
    uv run ui-flow history --url "{{url}}"
  fi

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
  uv sync
  uv run playwright install chromium
  cd report-ui && bun install

set shell := ["zsh", "-cu"]

default:
  @just --list

# Run a crawl against a URL using `.crawl-config` defaults.
crawl url:
  uv run flowscout explore "{{url}}" --config-file .crawl-config

# Run a crawl in headed (visible browser) mode.
crawl-headed url:
  uv run flowscout explore "{{url}}" --config-file .crawl-config --no-headless

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

# Compile TypeScript browser scripts to JS.
build-js:
  cd src/flowscout/js && bunx tsc -p tsconfig.json

# Install all project dependencies.
setup:
  uv sync --extra dev
  uv run playwright install chromium

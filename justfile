set shell := ["zsh", "-cu"]

default:
  @just --list

# Run a crawl against a URL using `.crawl-config` defaults.
crawl url:
  #!/usr/bin/env zsh
  uv run flowscout explore "{{url}}" --config-file .crawl-config
  mkdir -p .flowscout
  latest_report=$(print -r -- reports/**/report.html(Nom[1]))
  if [[ -n "${latest_report}" ]]; then
    print -r -- "${latest_report}" > .flowscout/last_report_path
    echo "Recorded last report: ${latest_report}"
  fi

# Run a crawl in headed (visible browser) mode.
crawl-headed url:
  #!/usr/bin/env zsh
  uv run flowscout explore "{{url}}" --config-file .crawl-config --no-headless
  mkdir -p .flowscout
  latest_report=$(print -r -- reports/**/report.html(Nom[1]))
  if [[ -n "${latest_report}" ]]; then
    print -r -- "${latest_report}" > .flowscout/last_report_path
    echo "Recorded last report: ${latest_report}"
  fi

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
  #!/usr/bin/env zsh
  latest_report=""
  if [[ -f .flowscout/last_report_path ]]; then
    recorded=$(<.flowscout/last_report_path)
    if [[ -n "${recorded}" && -f "${recorded}" ]]; then
      latest_report="${recorded}"
    fi
  fi
  if [[ -z "${latest_report}" ]]; then
    latest_report=$(print -r -- reports/**/report.html(Nom[1]))
  fi
  if [[ -z "${latest_report}" ]]; then
    echo "No report.html found under reports/"
    exit 1
  fi
  echo "Opening report: ${latest_report}"
  uv run flowscout serve "${latest_report}"

# Compile TypeScript browser scripts to JS.
build-js:
  cd src/flowscout/js && bunx tsc -p tsconfig.json

# Install all project dependencies.
setup:
  uv sync --extra dev
  uv run playwright install chromium
  just build-js

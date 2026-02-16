"""Contract tests to keep docs aligned with runtime behavior."""

from __future__ import annotations

from pathlib import Path
import re

from click.testing import CliRunner

from flowscout.cli import main
from flowscout.core.action_types import OutcomeType


def _readme_option_default(*, option: str) -> str:
    """Return the default column value for a README option table row."""
    readme = Path("README.md").read_text()
    for line in readme.splitlines():
        if line.strip().startswith(f"| `{option}`"):
            columns = [part.strip() for part in line.split("|")]
            if len(columns) >= 4:
                return columns[2].strip("`")
            break
    raise AssertionError(f"Could not find default for option {option} in README")


def test_readme_defaults_match_explore_help() -> None:
    """README option defaults should align with `flowscout explore --help`."""
    result = CliRunner().invoke(main, ["explore", "--help"])
    assert result.exit_code == 0, result.output
    help_text = result.output

    assert _readme_option_default(option="--smart") == "on"
    assert "--smart / --no-smart" in help_text
    assert "[default: smart]" in help_text

    assert _readme_option_default(option="--outcome-mode") == "legacy"
    assert "--outcome-mode [legacy|document-only]" in help_text
    assert re.search(r"\[default:\s*legacy\]", help_text) is not None

    assert _readme_option_default(option="--link-scope-mode") == "legacy"
    assert "--link-scope-mode [legacy|origin]" in help_text
    assert re.search(r"\[default:\s*legacy\]", help_text) is not None


def test_architecture_outcome_taxonomy_matches_runtime_enum() -> None:
    """Architecture doc outcome bullets should match OutcomeType enum values."""
    architecture_doc = Path("docs/ARCHITECTURE_AND_DATA_MODEL.md").read_text()

    for outcome in OutcomeType:
        assert f"`{outcome.value}`" in architecture_doc

    assert "`success`" not in architecture_doc
    assert "`execution_error`" not in architecture_doc

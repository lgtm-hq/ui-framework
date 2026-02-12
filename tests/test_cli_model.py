"""Tests for ``flowscout model`` command behavior."""

import json
from pathlib import Path

from click.testing import CliRunner

from flowscout.analysis.graph import ExplorationResult
from flowscout.cli import main
from flowscout.core.state import PageState


def test_model_generates_site_model_json() -> None:
    """Ensure model command builds and writes a SiteModel artifact."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result_path = Path("result.json")
        output_path = Path("site_model.json")

        state = PageState(
            state_id="s1",
            url="https://example.com",
            title="Home",
            fingerprint="f" * 64,
            depth=0,
            dom_structure_hash="dom",
            visible_text_hash="text",
            form_state_hash="form",
        )
        exploration = ExplorationResult(
            config={"start_url": "https://example.com"},
            states={"s1": state},
        )
        result_path.write_text(exploration.model_dump_json(indent=2))

        result = runner.invoke(
            main,
            [
                "model",
                str(result_path),
                "--output",
                str(output_path),
            ],
        )

        assert result.exit_code == 0, result.output
        payload = json.loads(output_path.read_text())
        assert "page_types" in payload

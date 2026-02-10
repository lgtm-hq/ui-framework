"""Tests for ``flowscout generate`` command behavior."""

from pathlib import Path

from click.testing import CliRunner

from flowscout.cli import main


def test_generate_site_model_rejects_bdd_framework() -> None:
    """Ensure unsupported site-model + bdd combination fails fast."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result_path = Path("result.json")
        result_path.write_text("{}")

        result = runner.invoke(
            main,
            [
                "generate",
                str(result_path),
                "--site-model",
                "--framework",
                "bdd",
            ],
        )

    assert result.exit_code != 0
    assert "--site-model does not support framework 'bdd'" in result.output

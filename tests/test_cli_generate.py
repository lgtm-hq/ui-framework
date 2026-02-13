"""Tests for ``flowscout generate`` command behavior."""

import json
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


def test_generate_accepts_site_model_input_without_flag() -> None:
    """Ensure SiteModel JSON is auto-detected and generates scenario tests."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        model_path = Path("model.json")
        model_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "version": "1.0.0",
                    "page_types": [
                        {
                            "page_type_id": "pt_home",
                            "name": "Home",
                            "archetype": "landing",
                            "url_pattern": "https://example.com/",
                            "structural_signature": "sig_home",
                            "instance_count": 1,
                            "representative_url": "https://example.com/",
                            "representative_state_id": "s1",
                        },
                    ],
                    "navigation_edges": [],
                    "test_scenarios": [
                        {
                            "scenario_id": "scenario-1",
                            "name": "Load home page",
                            "description": "Navigate to home page and verify content",
                            "page_type_sequence": ["pt_home"],
                            "steps": [
                                {
                                    "page_type": "pt_home",
                                    "action_description": "Navigate to Home",
                                },
                            ],
                            "priority": "important",
                            "template": "load_verify",
                            "tags": ["smoke"],
                        },
                    ],
                    "summary": {
                        "total_page_types": 1,
                        "total_navigation_edges": 0,
                        "total_scenarios": 1,
                    },
                },
            ),
        )

        result = runner.invoke(
            main,
            [
                "generate",
                str(model_path),
                "--output",
                "out",
            ],
        )

        assert result.exit_code == 0, result.output
        assert Path("out/scenario_tests.py").exists()


def test_generate_with_mbt_strategy_produces_scenarios() -> None:
    """Ensure --mbt strategy generates scenario tests from SiteModel edges."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        model_path = Path("model.json")
        model_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "version": "1.0.0",
                    "page_types": [
                        {
                            "page_type_id": "pt_home",
                            "name": "Home",
                            "archetype": "landing",
                            "url_pattern": "https://example.com/",
                            "structural_signature": "sig_home",
                            "instance_count": 1,
                            "representative_url": "https://example.com/",
                            "representative_state_id": "s1",
                        },
                        {
                            "page_type_id": "pt_products",
                            "name": "Products",
                            "archetype": "listing",
                            "url_pattern": "https://example.com/products",
                            "structural_signature": "sig_products",
                            "instance_count": 1,
                            "representative_url": "https://example.com/products",
                            "representative_state_id": "s2",
                        },
                    ],
                    "navigation_edges": [
                        {
                            "from_page_type": "pt_home",
                            "to_page_type": "pt_products",
                            "trigger": "Open products",
                            "action_type": "click",
                            "outcome": "navigation",
                            "occurrence_count": 2,
                        },
                    ],
                    "test_scenarios": [],
                    "summary": {
                        "total_page_types": 2,
                        "total_navigation_edges": 1,
                        "total_scenarios": 0,
                    },
                },
            ),
        )

        result = runner.invoke(
            main,
            [
                "generate",
                str(model_path),
                "--mbt",
                "edge",
                "--output",
                "out",
            ],
        )

        assert result.exit_code == 0, result.output
        output_path = Path("out/scenario_tests.py")
        assert output_path.exists()
        assert "mbt_edge_coverage" in output_path.read_text()


def test_generate_rejects_mbt_with_non_test_format() -> None:
    """Ensure --mbt cannot be used with markdown/junit formats."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result_path = Path("result.json")
        result_path.write_text("{}")

        result = runner.invoke(
            main,
            [
                "generate",
                str(result_path),
                "--mbt",
                "edge",
                "--format",
                "markdown",
            ],
        )

        assert result.exit_code != 0
        assert "--mbt supports only '--format tests'" in result.output

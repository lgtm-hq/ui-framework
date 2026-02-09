"""Tests for HTML report helper utilities."""

from pathlib import Path

from flowscout.reporting.html import _to_report_asset_href


def test_to_report_asset_href_none() -> None:
    report_dir = Path("/tmp/reports/run")
    assert _to_report_asset_href(None, report_dir=report_dir) is None


def test_to_report_asset_href_relative_path() -> None:
    report_dir = Path("/tmp/reports/run")
    href = _to_report_asset_href("evidence/actions/a.png", report_dir=report_dir)
    assert href == "evidence/actions/a.png"


def test_to_report_asset_href_inside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")
    path = report_dir / "evidence" / "actions" / "shot.png"
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == "evidence/actions/shot.png"


def test_to_report_asset_href_outside_report_dir() -> None:
    report_dir = Path("/tmp/reports/run")
    path = Path("/tmp/other/location/shot.png")
    href = _to_report_asset_href(str(path), report_dir=report_dir)
    assert href == path.as_uri()

"""Tests for HTML report accessibility (WCAG 2.1 AA)."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.analysis.narrative import FlowNarrative, NarrativeStep
from flowscout.analysis.verdict import JourneyVerdict, Verdict
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.reporting.html import HTMLReporter


def _generate_report(tmp_path: Path) -> str:
    """Generate a report and return its HTML content."""
    output = tmp_path / "report.html"
    result = ExplorationResult(
        config={"start_url": "https://example.com", "strategy": "priority"},
        states={
            "s0": PageState(
                state_id="s0",
                url="https://example.com",
                title="Home",
                fingerprint="a" * 64,
                depth=0,
                dom_structure_hash="dom-0",
                visible_text_hash="text-0",
                form_state_hash="form-0",
            ),
            "s1": PageState(
                state_id="s1",
                url="https://example.com/about",
                title="About",
                fingerprint="b" * 64,
                depth=1,
                dom_structure_hash="dom-1",
                visible_text_hash="text-1",
                form_state_hash="form-1",
            ),
            "s2": PageState(
                state_id="s2",
                url="https://example.com/contact",
                title="Contact",
                fingerprint="c" * 64,
                depth=1,
                dom_structure_hash="dom-2",
                visible_text_hash="text-2",
                form_state_hash="form-2",
            ),
        },
        actions={
            "a0": Action(
                action_id="a0",
                action_type=ActionType.CLICK,
                target_selector="a[href='/about']",
                label="Click About",
            ),
        },
        results=[
            ActionResult(
                action_id="a0",
                source_state_id="s0",
                target_state_id="s1",
                outcome=OutcomeType.NAVIGATION,
                duration_ms=120.0,
                url_before="https://example.com",
                url_after="https://example.com/about",
            ),
        ],
        flows=[
            Flow(
                flow_id="flow-0",
                name="Navigate to About",
                description="Click About link from Home",
                state_ids=["s0", "s1"],
                action_ids=["a0"],
                outcomes=[OutcomeType.NAVIGATION],
                depth=1,
                verdict=JourneyVerdict(verdict=Verdict.PASS, summary="Passed"),
                narrative=FlowNarrative(
                    title="Navigate to About",
                    precondition="User is on the Home page",
                    steps=[
                        NarrativeStep(
                            step_number=1,
                            action_description="Click About link",
                            verdict=Verdict.PASS,
                        ),
                    ],
                    conclusion="Navigation successful",
                ),
            ),
        ],
        duration_seconds=1.5,
    )
    HTMLReporter().generate(result, str(output))
    return output.read_text()


class _TagCollector(HTMLParser):
    """Collect tags with specific attributes from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append({"tag": tag, "attrs": dict(attrs)})


class TestSkipToContent:
    def test_skip_link_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'class="skip-to-content"' in html
        assert 'href="#main-content"' in html

    def test_main_content_id_exists(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'id="main-content"' in html


class TestAriaLandmarks:
    def test_header_has_role_banner(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'role="banner"' in html

    def test_main_has_role_main(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'role="main"' in html

    def test_footer_has_role_contentinfo(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'role="contentinfo"' in html

    def test_page_nav_has_role_navigation(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'role="navigation"' in html
        assert 'aria-label="Report sections"' in html

    def test_filter_toolbar_has_role(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'role="toolbar"' in html
        assert 'aria-label="Filter test cases"' in html


class TestAriaExpandedOnCollapsibles:
    def test_collapsible_sections_have_aria_expanded(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        parser = _TagCollector()
        parser.feed(html)
        collapsible_headers = [
            t
            for t in parser.tags
            if t["tag"] == "div"
            and "section-header" in t["attrs"].get("class", "")
            and "role" in t["attrs"]
        ]
        assert len(collapsible_headers) >= 3
        for header in collapsible_headers:
            assert header["attrs"].get("role") == "button"
            assert "aria-expanded" in header["attrs"]
            assert header["attrs"].get("tabindex") == "0"

    def test_suite_header_has_aria_expanded(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'class="suite-header"' in html
        parser = _TagCollector()
        parser.feed(html)
        suite_headers = [
            t
            for t in parser.tags
            if t["tag"] == "div" and "suite-header" in t["attrs"].get("class", "")
        ]
        assert len(suite_headers) >= 1
        for header in suite_headers:
            assert header["attrs"].get("aria-expanded") == "true"
            assert header["attrs"].get("role") == "button"
            assert header["attrs"].get("tabindex") == "0"


class TestModalAccessibility:
    def test_modals_have_dialog_role(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        parser = _TagCollector()
        parser.feed(html)
        dialogs = [t for t in parser.tags if t["attrs"].get("role") == "dialog"]
        assert len(dialogs) >= 2
        for dialog in dialogs:
            assert dialog["attrs"].get("aria-modal") == "true"

    def test_modals_have_aria_labelledby(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'aria-labelledby="execution-modal-title"' in html
        assert 'aria-labelledby="elements-modal-title"' in html

    def test_escape_key_closes_modals(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert "event.key === 'Escape'" in html

    def test_focus_trap_logic_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert "_trapFocus" in html
        assert "_releaseFocusTrap" in html
        assert "_lastFocusedElement" in html


class TestTableAccessibility:
    def test_all_tables_have_captions(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        parser = _TagCollector()
        parser.feed(html)
        tables = [t for t in parser.tags if t["tag"] == "table"]
        captions = [t for t in parser.tags if t["tag"] == "caption"]
        assert len(tables) > 0
        assert len(captions) >= len(tables)


class TestSearchAccessibility:
    def test_search_box_has_aria_label(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'aria-label="Search test cases"' in html


class TestFocusIndicators:
    def test_focus_visible_styles_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert ":focus-visible" in html


class TestResponsiveDesign:
    def test_viewport_meta_tag_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert 'name="viewport"' in html
        assert "width=device-width" in html

    def test_tablet_breakpoint_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert "@media (max-width: 768px)" in html

    def test_mobile_breakpoint_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert "@media (max-width: 480px)" in html

    def test_sr_only_class_present(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert ".sr-only" in html


class TestKeyboardNavigation:
    def test_collapsible_headers_respond_to_keyboard(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        assert "event.key==='Enter'" in html or 'event.key==="Enter"' in html

    def test_suite_headers_respond_to_keyboard(self, tmp_path: Path) -> None:
        html = _generate_report(tmp_path)
        matches = re.findall(r'class="suite-header"[^>]*onkeydown', html)
        assert len(matches) >= 1

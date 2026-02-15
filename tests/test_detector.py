"""Tests for outcome detection."""

import pytest

from flowscout.analysis.detector import OutcomeDetector, detect_page_block
from flowscout.core.state import OutcomeMode, PageBlockReason
from flowscout.discovery.actions import OutcomeType


class TestOutcomeDetector:
    def setup_method(self) -> None:
        self.detector = OutcomeDetector()

    def test_url_change_is_navigation(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com/a",
            url_after="https://example.com/b",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=[],
            console_errors=[],
            network_errors=[],
        )
        assert result == OutcomeType.NAVIGATION

    def test_network_error(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=[],
            network_errors=[{"url": "/api", "status": "500"}],
        )
        assert result == OutcomeType.NETWORK_ERROR

    def test_console_error(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=["TypeError: x is not a function"],
            network_errors=[],
        )
        assert result == OutcomeType.CONSOLE_ERROR

    def test_validation_error(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=["Email is required"],
            console_errors=[],
            network_errors=[],
        )
        assert result == OutcomeType.VALIDATION_ERROR

    def test_dom_change(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=[],
            console_errors=[],
            network_errors=[],
        )
        assert result == OutcomeType.DOM_CHANGE

    def test_no_change(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=[],
            network_errors=[],
        )
        assert result == OutcomeType.NO_CHANGE

    def test_priority_navigation_over_dom_change(self) -> None:
        """Navigation takes priority even when DOM also changed."""
        result = self.detector.classify(
            url_before="https://example.com/a",
            url_after="https://example.com/b",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=["some error"],
            console_errors=["js error"],
            network_errors=[],
        )
        assert result == OutcomeType.NAVIGATION

    def test_400_is_network_error(self) -> None:
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=[],
            network_errors=[{"url": "/api", "status": "404"}],
        )
        assert result == OutcomeType.NETWORK_ERROR

    def test_multiple_error_types_priority(self) -> None:
        """When network errors, console errors, and validation errors all occur,
        network error should take priority."""
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=["Field is required"],
            console_errors=["TypeError: null"],
            network_errors=[{"url": "/api", "status": "500"}],
        )
        assert result == OutcomeType.NETWORK_ERROR

    def test_document_only_mode_ignores_subresource_http_errors(self) -> None:
        detector = OutcomeDetector(outcome_mode=OutcomeMode.DOCUMENT_ONLY)
        result = detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=[],
            console_errors=[],
            network_errors=[
                {
                    "url": "https://example.com/api",
                    "status": "404",
                    "is_document": False,
                    "is_navigation": False,
                }
            ],
        )
        assert result == OutcomeType.DOM_CHANGE

    def test_document_only_mode_keeps_document_navigation_http_errors(self) -> None:
        detector = OutcomeDetector(outcome_mode=OutcomeMode.DOCUMENT_ONLY)
        result = detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=[],
            network_errors=[
                {
                    "url": "https://example.com/private",
                    "status": "403",
                    "is_document": True,
                    "is_navigation": True,
                }
            ],
        )
        assert result == OutcomeType.NETWORK_ERROR

    def test_legacy_mode_keeps_prior_network_error_behavior(self) -> None:
        detector = OutcomeDetector(outcome_mode=OutcomeMode.LEGACY)
        result = detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="aaa",
            error_messages=[],
            console_errors=[],
            network_errors=[{"url": "/api", "status": "500"}],
        )
        assert result == OutcomeType.NETWORK_ERROR

    def test_console_and_validation_errors(self) -> None:
        """Console errors take priority over validation errors in the detector."""
        result = self.detector.classify(
            url_before="https://example.com",
            url_after="https://example.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=["Email is required"],
            console_errors=["Warning: something"],
            network_errors=[],
        )
        assert result == OutcomeType.CONSOLE_ERROR

    def test_describe_transition_detects_hard_navigation(self) -> None:
        kind, detail = self.detector.describe_transition(
            outcome=OutcomeType.NAVIGATION,
            url_before="https://example.com/a",
            url_after="https://example.com/b",
            network_errors=[],
            console_errors=[],
            document_navigation_events=[
                {
                    "url": "https://example.com/b",
                    "status": "200",
                    "is_navigation": True,
                    "is_document": True,
                }
            ],
        )
        assert kind == "hard_navigation"
        assert "document navigation" in detail.lower()

    def test_describe_transition_detects_redirect_navigation(self) -> None:
        kind, detail = self.detector.describe_transition(
            outcome=OutcomeType.NAVIGATION,
            url_before="https://example.com/a",
            url_after="https://example.com/b",
            network_errors=[],
            console_errors=[],
            document_navigation_events=[
                {
                    "url": "https://example.com/a",
                    "status": "302",
                    "is_navigation": True,
                    "is_document": True,
                },
                {
                    "url": "https://example.com/b",
                    "status": "200",
                    "is_navigation": True,
                    "is_document": True,
                },
            ],
        )
        assert kind == "redirect_navigation"
        assert "redirect" in detail.lower()

    def test_describe_transition_detects_client_route_navigation(self) -> None:
        kind, detail = self.detector.describe_transition(
            outcome=OutcomeType.NAVIGATION,
            url_before="https://example.com/a",
            url_after="https://example.com/b",
            network_errors=[],
            console_errors=[],
            document_navigation_events=[],
        )
        assert kind == "client_route_navigation"
        assert "without a top-level document navigation" in detail.lower()


class _FakePage:
    """Minimal page stub for testing find_error_messages."""

    def __init__(self, return_value: list[str]) -> None:
        self._return_value = return_value

    async def evaluate(self, js, *args):
        return self._return_value


class TestFindErrorMessages:
    @pytest.mark.asyncio
    async def test_returns_error_texts(self):
        page = _FakePage(["Email is required", "Password too short"])
        detector = OutcomeDetector()
        errors = await detector.find_error_messages(page)
        assert errors == ["Email is required", "Password too short"]

    @pytest.mark.asyncio
    async def test_filters_empty_strings(self):
        page = _FakePage(["Error", "", "Another error"])
        detector = OutcomeDetector()
        errors = await detector.find_error_messages(page)
        assert errors == ["Error", "Another error"]

    @pytest.mark.asyncio
    async def test_returns_empty_on_exception(self):
        class _ErrorPage:
            async def evaluate(self, js, *args):
                raise RuntimeError("Page crashed")

        detector = OutcomeDetector()
        errors = await detector.find_error_messages(_ErrorPage())
        assert errors == []

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_errors(self):
        page = _FakePage([])
        detector = OutcomeDetector()
        errors = await detector.find_error_messages(page)
        assert errors == []


class _FakeBlockedPage:
    """Minimal page stub for blocked-page detection tests."""

    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    async def evaluate(self, js, *args):
        return self._payload


class TestDetectPageBlock:
    @pytest.mark.asyncio
    async def test_detects_http_access_denied(self) -> None:
        detection = await detect_page_block(
            page=_FakeBlockedPage({}),
            status_code=403,
        )
        assert detection.is_blocked is True
        assert detection.reason == PageBlockReason.ACCESS_DENIED

    @pytest.mark.asyncio
    async def test_detects_access_denied_text(self) -> None:
        page = _FakeBlockedPage(
            {
                "title": "Access Denied",
                "bodyText": "Forbidden",
                "hasRecaptcha": False,
                "hasHCaptcha": False,
                "hasTurnstile": False,
            }
        )
        detection = await detect_page_block(page=page)
        assert detection.is_blocked is True
        assert detection.reason == PageBlockReason.ACCESS_DENIED

    @pytest.mark.asyncio
    async def test_detects_captcha_markers(self) -> None:
        page = _FakeBlockedPage(
            {
                "title": "Please Verify",
                "bodyText": "",
                "hasRecaptcha": True,
                "hasHCaptcha": False,
                "hasTurnstile": False,
                "hasConsentWall": False,
            }
        )
        detection = await detect_page_block(page=page)
        assert detection.is_blocked is True
        assert detection.reason == PageBlockReason.CAPTCHA

    @pytest.mark.asyncio
    async def test_detects_consent_wall_markers(self) -> None:
        page = _FakeBlockedPage(
            {
                "title": "Privacy Preferences",
                "bodyText": "Manage cookies for this site.",
                "hasRecaptcha": False,
                "hasHCaptcha": False,
                "hasTurnstile": False,
                "hasConsentWall": True,
            }
        )
        detection = await detect_page_block(page=page)
        assert detection.is_blocked is True
        assert detection.reason == PageBlockReason.CONSENT_WALL

    @pytest.mark.asyncio
    async def test_returns_unblocked_when_no_signals(self) -> None:
        page = _FakeBlockedPage(
            {
                "title": "Home",
                "bodyText": "Welcome",
                "hasRecaptcha": False,
                "hasHCaptcha": False,
                "hasTurnstile": False,
                "hasConsentWall": False,
            }
        )
        detection = await detect_page_block(page=page, status_code=200)
        assert detection.is_blocked is False
        assert detection.reason == PageBlockReason.NONE

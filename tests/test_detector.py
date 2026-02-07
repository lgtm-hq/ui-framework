"""Tests for outcome detection."""

import pytest

from flowscout.analysis.detector import OutcomeDetector
from flowscout.discovery.actions import OutcomeType


class TestOutcomeDetector:
    def setup_method(self):
        self.detector = OutcomeDetector()

    def test_url_change_is_navigation(self):
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

    def test_network_error(self):
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

    def test_console_error(self):
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

    def test_validation_error(self):
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

    def test_dom_change(self):
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

    def test_no_change(self):
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

    def test_priority_navigation_over_dom_change(self):
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

    def test_400_is_network_error(self):
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

    def test_multiple_error_types_priority(self):
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

    def test_console_and_validation_errors(self):
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


class _FakePage:
    """Minimal page stub for testing find_error_messages."""

    def __init__(self, return_value):
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

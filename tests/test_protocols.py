"""Verify protocol interfaces match existing concrete classes."""

from __future__ import annotations

import pytest

from flowscout.core.protocols import (
    IBrowser,
    IElementDiscoverer,
    IOutcomeDetector,
    IReporter,
    IStorage,
    ITerminalReporter,
)


class TestIOutcomeDetectorProtocol:
    """OutcomeDetector must satisfy IOutcomeDetector."""

    def test_structural_subtype(self) -> None:
        from flowscout.analysis.detector import OutcomeDetector

        assert isinstance(OutcomeDetector(), IOutcomeDetector)

    def test_classify_signature(self) -> None:
        from flowscout.analysis.detector import OutcomeDetector

        det = OutcomeDetector()
        result = det.classify(
            url_before="http://a.com",
            url_after="http://b.com",
            dom_hash_before="aaa",
            dom_hash_after="bbb",
            error_messages=[],
            console_errors=[],
            network_errors=[],
        )
        assert result is not None


class TestIReporterProtocol:
    """HTMLReporter must satisfy IReporter."""

    def test_structural_subtype(self) -> None:
        from flowscout.reporting.html import HTMLReporter

        assert isinstance(HTMLReporter(), IReporter)


class TestITerminalReporterProtocol:
    """TerminalReporter must satisfy ITerminalReporter."""

    def test_structural_subtype(self) -> None:
        from flowscout.reporting.terminal import TerminalReporter

        assert isinstance(TerminalReporter(), ITerminalReporter)


class TestIStorageProtocol:
    """FlowscoutDB must satisfy IStorage."""

    def test_structural_subtype(self) -> None:
        from flowscout.storage.db import FlowscoutDB

        db = FlowscoutDB(db_path=":memory:")
        try:
            assert isinstance(db, IStorage)
        finally:
            db.close()


class TestIElementDiscovererProtocol:
    """Protocol only requires a discover(page) method — verify the
    function-based API can be wrapped trivially."""

    def test_protocol_requires_discover(self) -> None:
        # IElementDiscoverer requires: async def discover(page) -> list
        import inspect

        hints = {}
        for name, method in inspect.getmembers(
            IElementDiscoverer, predicate=inspect.isfunction
        ):
            if not name.startswith("_"):
                hints[name] = method
        assert "discover" in hints


class TestIBrowserProtocol:
    """Verify BrowserManager satisfies IBrowser structurally.

    We can't instantiate BrowserManager without a config, so we check
    that the class has all required methods.
    """

    def test_has_required_methods(self) -> None:
        from flowscout.core.browser import BrowserManager

        required = [
            "launch",
            "close",
            "navigate",
            "capture_state",
            "execute_action",
            "get_dom_hash",
            "take_screenshot",
            "analyze_page_structure",
        ]
        for method_name in required:
            has = hasattr(BrowserManager, method_name)
            assert has, f"BrowserManager missing {method_name}"


class TestProtocolsAreRuntimeCheckable:
    """All protocols must be @runtime_checkable for isinstance checks."""

    @pytest.mark.parametrize(
        "protocol",
        [
            IBrowser,
            IOutcomeDetector,
            IStorage,
            IReporter,
            ITerminalReporter,
            IElementDiscoverer,
        ],
    )
    def test_runtime_checkable(self, protocol: type) -> None:
        # runtime_checkable protocols have _is_runtime_protocol set
        is_rt = getattr(protocol, "_is_runtime_protocol", False)
        assert is_rt, f"{protocol.__name__} is not @runtime_checkable"

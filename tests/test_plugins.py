"""Tests for the plugin registry."""

from __future__ import annotations

from unittest.mock import patch

from flowscout.plugins.registry import PluginRegistry


class _MockReporter:
    def generate(self, result, output_path):
        pass


class _MockDetector:
    def classify(self, **kwargs):
        pass

    async def find_error_messages(self, page):
        return []


class _MockDiscoverer:
    async def discover(self, page):
        return []


class TestPluginRegistry:

    def test_register_and_get_reporter(self) -> None:
        registry = PluginRegistry()
        registry.register_reporter("mock", _MockReporter)
        assert registry.get_reporter("mock") is _MockReporter

    def test_get_unknown_reporter_returns_none(self) -> None:
        registry = PluginRegistry()
        assert registry.get_reporter("nonexistent") is None

    def test_list_reporters(self) -> None:
        registry = PluginRegistry()
        registry.register_reporter("beta", _MockReporter)
        registry.register_reporter("alpha", _MockReporter)
        assert registry.list_reporters() == ["alpha", "beta"]

    def test_register_and_get_detector(self) -> None:
        registry = PluginRegistry()
        registry.register_detector("mock", _MockDetector)
        assert registry.get_detector("mock") is _MockDetector

    def test_get_unknown_detector_returns_none(self) -> None:
        registry = PluginRegistry()
        assert registry.get_detector("nonexistent") is None

    def test_list_detectors(self) -> None:
        registry = PluginRegistry()
        registry.register_detector("zeta", _MockDetector)
        registry.register_detector("alpha", _MockDetector)
        assert registry.list_detectors() == ["alpha", "zeta"]

    def test_register_and_get_discoverer(self) -> None:
        registry = PluginRegistry()
        registry.register_discoverer("mock", _MockDiscoverer)
        assert registry.get_discoverer("mock") is _MockDiscoverer

    def test_get_unknown_discoverer_returns_none(self) -> None:
        registry = PluginRegistry()
        assert registry.get_discoverer("nonexistent") is None

    def test_list_discoverers(self) -> None:
        registry = PluginRegistry()
        registry.register_discoverer("b", _MockDiscoverer)
        registry.register_discoverer("a", _MockDiscoverer)
        assert registry.list_discoverers() == ["a", "b"]


class TestEntryPointLoading:

    def test_load_from_entry_points_no_plugins(self) -> None:
        registry = PluginRegistry()
        registry.load_from_entry_points()
        assert registry.list_reporters() == []
        assert registry.list_detectors() == []
        assert registry.list_discoverers() == []

    def test_load_from_entry_points_with_mock(self) -> None:
        class _FakeEntryPoint:
            name = "test_reporter"

            def load(self):
                return _MockReporter

        with patch(
            "flowscout.plugins.registry.importlib.metadata.entry_points"
        ) as mock_eps:
            def _fake_eps(group):
                if group == "flowscout.reporters":
                    return [_FakeEntryPoint()]
                return []

            mock_eps.side_effect = _fake_eps

            registry = PluginRegistry()
            registry.load_from_entry_points()
            assert registry.get_reporter("test_reporter") is _MockReporter

    def test_load_from_entry_points_handles_errors(self) -> None:
        class _BrokenEntryPoint:
            name = "broken"

            def load(self):
                raise ImportError("broken plugin")

        with patch(
            "flowscout.plugins.registry.importlib.metadata.entry_points"
        ) as mock_eps:
            def _fake_eps(group):
                if group == "flowscout.reporters":
                    return [_BrokenEntryPoint()]
                return []

            mock_eps.side_effect = _fake_eps

            registry = PluginRegistry()
            registry.load_from_entry_points()
            # Broken plugin should not be registered
            assert registry.get_reporter("broken") is None

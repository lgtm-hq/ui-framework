"""Verify constant dataclasses: values, immutability, and defaults."""

from __future__ import annotations

import dataclasses

import pytest

from flowscout.core.constants import (
    LOW_CONFIDENCE_THRESHOLD,
    ActionPriorities,
    BrowserDefaults,
    DEFAULT_BROWSER,
    DEFAULT_LIMITS,
    DEFAULT_PRIORITIES,
    DEFAULT_SELECTORS,
    DetectionSelectors,
    ExplorationLimits,
)


class TestExplorationLimits:
    def test_default_values(self) -> None:
        limits = ExplorationLimits()
        assert limits.diversity_interval == 5
        assert limits.deprioritized_priority == 80
        assert limits.dom_change_saturation_count == 3
        assert limits.max_reveal_triggers == 5
        assert limits.max_paths_per_leaf == 25
        assert limits.max_total_linear_flows == 500
        assert limits.max_cycle_flows == 200
        assert limits.max_backtrack_retries == 3

    def test_frozen(self) -> None:
        limits = ExplorationLimits()
        with pytest.raises(dataclasses.FrozenInstanceError):
            limits.diversity_interval = 10

    def test_custom_values(self) -> None:
        limits = ExplorationLimits(diversity_interval=10, max_paths_per_leaf=50)
        assert limits.diversity_interval == 10
        assert limits.max_paths_per_leaf == 50
        # Others retain defaults
        assert limits.deprioritized_priority == 80


class TestBrowserDefaults:
    def test_default_values(self) -> None:
        bd = BrowserDefaults()
        assert bd.viewport_width == 1280
        assert bd.viewport_height == 720
        assert bd.stability_poll_interval_s == 0.2
        assert bd.dropdown_reveal_delay_s == 0.35
        assert bd.post_click_delay_s == 0.3

    def test_frozen(self) -> None:
        bd = BrowserDefaults()
        with pytest.raises(dataclasses.FrozenInstanceError):
            bd.viewport_width = 1920


class TestActionPriorities:
    def test_ordering_invariants(self) -> None:
        """Core ordering: navigation < submit < form < generic < disabled."""
        p = ActionPriorities()
        assert p.navigation_link < p.submit_button
        assert p.submit_button < p.form_input
        assert p.form_input < p.generic_button
        assert p.generic_button < p.generic_clickable
        assert p.generic_clickable < p.deprioritized
        assert p.deprioritized < p.disabled

    def test_specific_values(self) -> None:
        p = ActionPriorities()
        assert p.navigation_link == 10
        assert p.submit_button == 15
        assert p.dropdown_option == 15
        assert p.search_widget == 18
        assert p.action_button == 20
        assert p.form_input == 25
        assert p.generic_button == 30
        assert p.tab == 35
        assert p.select == 40
        assert p.anchor_link == 40
        assert p.checkbox == 50
        assert p.generic_clickable == 55
        assert p.deprioritized == 80
        assert p.external_link == 90
        assert p.saturated == 90
        assert p.disabled == 100

    def test_frozen(self) -> None:
        p = ActionPriorities()
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.navigation_link = 1


class TestDetectionSelectors:
    def test_error_selectors_content(self) -> None:
        ds = DetectionSelectors()
        assert ".error" in ds.error_selectors
        assert ".alert-danger" in ds.error_selectors
        assert "[aria-invalid='true']" in ds.error_selectors

    def test_success_selectors_content(self) -> None:
        ds = DetectionSelectors()
        assert ".success" in ds.success_selectors
        assert ".alert-success" in ds.success_selectors

    def test_frozen(self) -> None:
        ds = DetectionSelectors()
        with pytest.raises(dataclasses.FrozenInstanceError):
            ds.error_selectors = ()


class TestModuleLevelDefaults:
    def test_defaults_are_instances(self) -> None:
        assert isinstance(DEFAULT_LIMITS, ExplorationLimits)
        assert isinstance(DEFAULT_BROWSER, BrowserDefaults)
        assert isinstance(DEFAULT_PRIORITIES, ActionPriorities)
        assert isinstance(DEFAULT_SELECTORS, DetectionSelectors)

    def test_low_confidence_threshold(self) -> None:
        assert LOW_CONFIDENCE_THRESHOLD == 0.6
        assert 0 < LOW_CONFIDENCE_THRESHOLD < 1

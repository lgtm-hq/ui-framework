"""Centralized constants — replaces magic numbers scattered across the codebase."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplorationLimits:
    """Thresholds and caps for the exploration engine."""

    # After this many consecutive click-only actions, prefer a diverse type
    diversity_interval: int = 5

    # Priority assigned to deprioritized (saturated) actions
    deprioritized_priority: int = 80

    # After N DOM_CHANGE outcomes in a group, deprioritize remaining members
    dom_change_saturation_count: int = 3

    # Maximum dropdown triggers to click during element discovery
    max_reveal_triggers: int = 5

    # Flow extraction caps
    max_paths_per_leaf: int = 25
    max_total_linear_flows: int = 500
    max_cycle_flows: int = 200

    # Backtracking retry limit
    max_backtrack_retries: int = 3


@dataclass(frozen=True)
class BrowserDefaults:
    """Default values for browser configuration."""

    viewport_width: int = 1280
    viewport_height: int = 720

    # Delay between DOM hash polls during stability detection (seconds)
    stability_poll_interval_s: float = 0.2

    # Delay after clicking a dropdown trigger to allow options to render
    dropdown_reveal_delay_s: float = 0.35

    # Brief post-click delay for DOM updates
    post_click_delay_s: float = 0.3


@dataclass(frozen=True)
class ActionPriorities:
    """Priority values for action ordering (lower = explored first)."""

    navigation_link: int = 10
    submit_button: int = 15
    dropdown_option: int = 15
    search_widget: int = 18
    action_button: int = 20
    form_input: int = 25
    generic_button: int = 30
    tab: int = 35
    select: int = 40
    anchor_link: int = 40
    checkbox: int = 50
    generic_clickable: int = 55
    deprioritized: int = 80
    external_link: int = 90
    saturated: int = 90
    disabled: int = 100


@dataclass(frozen=True)
class DetectionSelectors:
    """CSS selectors for heuristic outcome detection."""

    error_selectors: tuple[str, ...] = (
        ".error",
        ".alert-error",
        ".alert-danger",
        ".validation-error",
        ".form-error",
        ".field-error",
        ".invalid-feedback",
        "[aria-invalid='true']",
    )

    success_selectors: tuple[str, ...] = (
        ".success",
        ".alert-success",
        ".notification-success",
    )


# Confidence threshold below which transitions are flagged as low-confidence
LOW_CONFIDENCE_THRESHOLD: float = 0.6

# Default exploration limits, browser defaults, and action priorities
DEFAULT_LIMITS = ExplorationLimits()
DEFAULT_BROWSER = BrowserDefaults()
DEFAULT_PRIORITIES = ActionPriorities()
DEFAULT_SELECTORS = DetectionSelectors()

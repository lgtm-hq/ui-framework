"""Tests for modeling locator scoring and preference heuristics."""

from __future__ import annotations

from flowscout.core.archetypes import CatalogEntry, ZoneType
from flowscout.modeling.locators import (
    LocatorStability,
    choose_preferred_locator,
    recommend_locator_improvements,
    score_locator,
    score_page_type,
)


def _entry(selector: str, *, xpath: str | None = None) -> CatalogEntry:
    return CatalogEntry(
        selector=selector,
        xpath=xpath,
        tag="button",
        label="Action",
        zone_type=ZoneType.MAIN_CONTENT,
    )


def test_score_locator_id_selector_is_highest_tier() -> None:
    score = score_locator("#primary-cta")
    assert score.score == 100
    assert score.tier == 1
    assert score.stability == LocatorStability.HIGH


def test_score_locator_positional_selector_is_low_tier() -> None:
    score = score_locator("main > div:nth-of-type(3) > button:nth-of-type(2)")
    assert score.score == 20
    assert score.tier == 8
    assert score.stability == LocatorStability.LOW


def test_score_page_type_averages_locator_scores() -> None:
    avg = score_page_type(
        [
            _entry("#primary-cta"),
            _entry("a[href='/movies']"),
            _entry("main > div:nth-of-type(2) > button"),
        ]
    )
    assert avg == 68.33


def test_choose_preferred_locator_uses_xpath_when_css_is_fragile() -> None:
    preferred = choose_preferred_locator(
        css_selector="main > div:nth-of-type(4) > button",
        xpath_selector="/html/body/main/div[4]/button",
    )
    assert preferred.strategy == "xpath"
    assert preferred.selector == "xpath=/html/body/main/div[4]/button"


def test_choose_preferred_locator_keeps_css_when_stable() -> None:
    preferred = choose_preferred_locator(
        css_selector="#search-input",
        xpath_selector="/html/body/header/input",
    )
    assert preferred.strategy == "css"
    assert preferred.selector == "#search-input"


def test_recommend_locator_improvements_reports_fragile_entries() -> None:
    recommendations = recommend_locator_improvements(
        page_type_name="Movie Listing",
        entries=[
            _entry(
                "main > div:nth-of-type(2) > button",
                xpath="/html/body/main/div[2]/button",
            ),
            _entry("button"),
        ],
    )
    assert len(recommendations) == 2
    assert any(
        "prefer XPath fallback" in recommendation for recommendation in recommendations
    )
    assert any("data-testid" in recommendation for recommendation in recommendations)

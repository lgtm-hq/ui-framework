"""Locator stability scoring and preference heuristics (Layer 2)."""

from __future__ import annotations

from collections import Counter
from enum import StrEnum, auto
from typing import Iterable

from pydantic import BaseModel

from flowscout.core.archetypes import CatalogEntry


class LocatorStability(StrEnum):
    """Locator stability bands for report-friendly summaries."""

    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class LocatorScore(BaseModel):
    """Scored locator metadata."""

    selector: str
    score: int
    tier: int
    stability: LocatorStability = LocatorStability.MEDIUM


class PreferredLocator(BaseModel):
    """Preferred selector strategy chosen by modeling."""

    selector: str
    strategy: str
    css_selector: str
    xpath_selector: str | None = None
    score: int


def score_locator(selector: str) -> LocatorScore:
    """Score a selector using Flowscout's stability tiers."""
    normalized = selector.strip()
    lower = normalized.lower()

    if ":nth-of-type(" in lower:
        return LocatorScore(
            selector=selector,
            score=20,
            tier=8,
            stability=LocatorStability.LOW,
        )
    if normalized.startswith("#"):
        return LocatorScore(
            selector=selector,
            score=100,
            tier=1,
            stability=LocatorStability.HIGH,
        )
    if "[data-testid" in lower or "[data-tab" in lower:
        return LocatorScore(
            selector=selector,
            score=95,
            tier=2,
            stability=LocatorStability.HIGH,
        )
    if lower.startswith("a[") and "href=" in lower:
        return LocatorScore(
            selector=selector,
            score=85,
            tier=3,
            stability=LocatorStability.HIGH,
        )
    if "[aria-label" in lower:
        return LocatorScore(
            selector=selector,
            score=80,
            tier=4,
            stability=LocatorStability.HIGH,
        )
    if "[role=" in lower:
        return LocatorScore(
            selector=selector,
            score=70,
            tier=5,
            stability=LocatorStability.MEDIUM,
        )
    if "[name=" in lower:
        return LocatorScore(
            selector=selector,
            score=65,
            tier=6,
            stability=LocatorStability.MEDIUM,
        )
    if lower.startswith("input[type="):
        return LocatorScore(
            selector=selector,
            score=50,
            tier=7,
            stability=LocatorStability.MEDIUM,
        )

    return LocatorScore(
        selector=selector,
        score=40,
        tier=9,
        stability=LocatorStability.LOW,
    )


def score_page_type(entries: Iterable[CatalogEntry]) -> float:
    """Return average locator score for a page type catalog."""
    scored = [
        score_locator(entry.selector).score for entry in entries if entry.selector
    ]
    if not scored:
        return 0.0
    return round(sum(scored) / len(scored), 2)


def choose_preferred_locator(
    *,
    css_selector: str,
    xpath_selector: str | None,
) -> PreferredLocator:
    """Choose CSS by default, with XPath fallback for fragile CSS selectors."""
    css_score = score_locator(css_selector)
    if css_score.score < 50 and xpath_selector:
        return PreferredLocator(
            selector=_normalize_xpath_selector(xpath_selector),
            strategy="xpath",
            css_selector=css_selector,
            xpath_selector=xpath_selector,
            score=css_score.score,
        )
    return PreferredLocator(
        selector=css_selector,
        strategy="css",
        css_selector=css_selector,
        xpath_selector=xpath_selector,
        score=css_score.score,
    )


def recommend_locator_improvements(
    *,
    page_type_name: str,
    entries: Iterable[CatalogEntry],
) -> list[str]:
    """Generate recommendations for fragile selectors on a page type."""
    recommendations: list[str] = []
    low_scores: Counter[str] = Counter()

    for entry in entries:
        score = score_locator(entry.selector)
        if score.score >= 50:
            continue

        if ":nth-of-type(" in entry.selector:
            low_scores["nth"] += 1
            if entry.xpath:
                recommendations.append(
                    f"{page_type_name}: prefer XPath fallback for '{entry.selector}'."
                )
            else:
                recommendations.append(
                    f"{page_type_name}: replace positional selector "
                    f"'{entry.selector}' with a stable data attribute."
                )
            continue

        low_scores["generic"] += 1
        recommendations.append(
            f"{page_type_name}: add data-testid or semantic attributes for "
            f"'{entry.selector}'."
        )

    if not recommendations and low_scores["nth"] == 0 and low_scores["generic"] == 0:
        return []

    return sorted(set(recommendations))


def _normalize_xpath_selector(xpath_selector: str) -> str:
    """Normalize XPath selectors for Playwright locator usage."""
    trimmed = xpath_selector.strip()
    if not trimmed:
        return trimmed
    if trimmed.startswith("xpath="):
        return trimmed
    return f"xpath={trimmed}"

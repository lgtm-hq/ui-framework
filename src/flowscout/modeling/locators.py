"""Locator stability scoring stubs (implemented in Phase 2.5)."""

from __future__ import annotations

from enum import StrEnum, auto

from pydantic import BaseModel


class LocatorStability(StrEnum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


class LocatorScore(BaseModel):
    """Placeholder model for locator quality scoring."""

    selector: str
    score: float
    stability: LocatorStability = LocatorStability.MEDIUM

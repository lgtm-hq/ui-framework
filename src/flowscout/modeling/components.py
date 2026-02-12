"""Shared component extraction stubs (implemented in Phase 2.2)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SharedComponent(BaseModel):
    """Placeholder model for reusable page components."""

    component_id: str
    name: str
    selectors: list[str] = Field(default_factory=list)

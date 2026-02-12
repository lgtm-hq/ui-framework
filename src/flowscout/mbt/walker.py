"""Graph walker stubs for MBT path generation (Phase 3.1)."""

from __future__ import annotations

from pydantic import BaseModel


class WalkRequest(BaseModel):
    """Placeholder request for MBT traversal configuration."""

    strategy: str = "edge"


def walk_model(_: WalkRequest) -> list[str]:
    """Return an empty walk result until MBT implementation lands."""
    return []

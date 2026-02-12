"""Flow template deduplication stubs (implemented in Phase 2.1)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FlowTemplate(BaseModel):
    """Placeholder model for deduplicated flow templates."""

    template_id: str
    name: str
    page_type_sequence: list[str] = Field(default_factory=list)
    occurrence_count: int = 0

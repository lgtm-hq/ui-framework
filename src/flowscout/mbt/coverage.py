"""Coverage metric stubs for MBT (Phase 3.2)."""

from __future__ import annotations

from pydantic import BaseModel


class CoverageSummary(BaseModel):
    """Placeholder MBT coverage summary."""

    edge_coverage_pct: float = 0.0
    state_coverage_pct: float = 0.0

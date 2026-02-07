"""Coverage tracking for smart exploration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CoverageState(BaseModel):
    """Serializable snapshot of coverage progress."""

    archetypes_seen: dict[str, int] = Field(default_factory=dict)
    structural_signatures_seen: dict[str, int] = Field(default_factory=dict)
    features_tested: set[str] = Field(default_factory=set)
    flow_templates_attempted: dict[str, int] = Field(default_factory=dict)


class CoverageTracker:
    """Tracks exploration coverage and determines saturation."""

    ARCHETYPE_INSTANCE_LIMIT = 3
    MIN_FEATURES_BEFORE_STOP = 3
    MIN_ARCHETYPES_BEFORE_STOP = 2

    def __init__(self) -> None:
        self._state = CoverageState()

    @property
    def state(self) -> CoverageState:
        return self._state

    def record_archetype(self, archetype: str, signature: str) -> None:
        """Record discovery of an archetype instance."""
        self._state.archetypes_seen[archetype] = (
            self._state.archetypes_seen.get(archetype, 0) + 1
        )
        self._state.structural_signatures_seen[signature] = (
            self._state.structural_signatures_seen.get(signature, 0) + 1
        )

    def record_feature(self, feature: str) -> None:
        """Record that a feature has been tested (e.g., 'search', 'pagination')."""
        self._state.features_tested.add(feature)

    def record_flow_template(self, template: str) -> None:
        """Record an attempted flow template."""
        self._state.flow_templates_attempted[template] = (
            self._state.flow_templates_attempted.get(template, 0) + 1
        )

    def is_saturated(self) -> bool:
        """Check if exploration has covered enough ground to stop.

        Saturated when: enough distinct archetypes explored AND enough features tested.
        """
        distinct_archetypes = len(self._state.archetypes_seen)
        features_count = len(self._state.features_tested)
        return (
            distinct_archetypes >= self.MIN_ARCHETYPES_BEFORE_STOP
            and features_count >= self.MIN_FEATURES_BEFORE_STOP
        )

    def should_deprioritize_archetype(self, signature: str) -> bool:
        """Check if a structural signature has been explored enough."""
        return (
            self._state.structural_signatures_seen.get(signature, 0)
            >= self.ARCHETYPE_INSTANCE_LIMIT
        )

    def summary(self) -> dict:
        """Return a summary dict for reporting."""
        return {
            "archetypes_seen": dict(self._state.archetypes_seen),
            "signatures_seen": len(self._state.structural_signatures_seen),
            "features_tested": sorted(self._state.features_tested),
            "flow_templates": dict(self._state.flow_templates_attempted),
            "is_saturated": self.is_saturated(),
        }

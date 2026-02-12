"""Coverage tracking for smart exploration."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CoverageState(BaseModel):
    """Serializable snapshot of coverage progress."""

    archetypes_seen: dict[str, int] = Field(default_factory=dict)
    structural_signatures_seen: dict[str, int] = Field(default_factory=dict)
    features_tested: set[str] = Field(default_factory=set)
    flow_templates_attempted: dict[str, int] = Field(default_factory=dict)


class CoverageTracker:
    """Tracks exploration coverage and determines saturation."""

    def __init__(
        self,
        *,
        archetype_instance_limit: int = 3,
        min_features_before_stop: int = 3,
        min_archetypes_before_stop: int = 2,
        stop_on_saturation: bool = True,
    ) -> None:
        self._state = CoverageState()
        self._archetype_instance_limit = max(1, int(archetype_instance_limit))
        self._min_features_before_stop = max(0, int(min_features_before_stop))
        self._min_archetypes_before_stop = max(0, int(min_archetypes_before_stop))
        self._stop_on_saturation = bool(stop_on_saturation)

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
        if not self._stop_on_saturation:
            return False

        distinct_archetypes = len(self._state.archetypes_seen)
        features_count = len(self._state.features_tested)
        return (
            distinct_archetypes >= self._min_archetypes_before_stop
            and features_count >= self._min_features_before_stop
        )

    def should_deprioritize_archetype(self, signature: str) -> bool:
        """Check if a structural signature has been explored enough."""
        return (
            self._state.structural_signatures_seen.get(signature, 0)
            >= self._archetype_instance_limit
        )

    def summary(self) -> dict[str, Any]:
        """Return a summary dict for reporting."""
        return {
            "archetypes_seen": dict(self._state.archetypes_seen),
            "signatures_seen": len(self._state.structural_signatures_seen),
            "features_tested": sorted(self._state.features_tested),
            "flow_templates": dict(self._state.flow_templates_attempted),
            "is_saturated": self.is_saturated(),
            "stop_on_saturation": self._stop_on_saturation,
            "min_features_before_stop": self._min_features_before_stop,
            "min_archetypes_before_stop": self._min_archetypes_before_stop,
        }

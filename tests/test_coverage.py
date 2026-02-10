"""Tests for the coverage tracker."""

from __future__ import annotations

from flowscout.smart.coverage import CoverageTracker


class TestCoverageTracker:
    """Coverage state tracking and saturation."""

    def test_record_archetype(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        assert tracker.state.archetypes_seen["listing"] == 1
        assert tracker.state.structural_signatures_seen["sig1"] == 1

    def test_record_archetype_increments(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_archetype("listing", "sig1")
        assert tracker.state.archetypes_seen["listing"] == 2
        assert tracker.state.structural_signatures_seen["sig1"] == 2

    def test_record_feature(self):
        tracker = CoverageTracker()
        tracker.record_feature("search")
        assert "search" in tracker.state.features_tested

    def test_feature_deduplication(self):
        tracker = CoverageTracker()
        tracker.record_feature("search")
        tracker.record_feature("search")
        assert len(tracker.state.features_tested) == 1

    def test_record_flow_template(self):
        tracker = CoverageTracker()
        tracker.record_flow_template("browse")
        assert tracker.state.flow_templates_attempted["browse"] == 1

    def test_not_saturated_initially(self):
        tracker = CoverageTracker()
        assert tracker.is_saturated() is False

    def test_not_saturated_one_archetype(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_feature("f1")
        tracker.record_feature("f2")
        tracker.record_feature("f3")
        assert tracker.is_saturated() is False  # Only 1 archetype

    def test_not_saturated_few_features(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_archetype("detail", "sig2")
        tracker.record_feature("f1")
        assert tracker.is_saturated() is False  # Only 1 feature

    def test_saturated_when_enough(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_archetype("detail", "sig2")
        tracker.record_feature("f1")
        tracker.record_feature("f2")
        tracker.record_feature("f3")
        assert tracker.is_saturated() is True

    def test_should_deprioritize(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_archetype("listing", "sig1")
        assert tracker.should_deprioritize_archetype("sig1") is False
        tracker.record_archetype("listing", "sig1")
        assert tracker.should_deprioritize_archetype("sig1") is True

    def test_should_not_deprioritize_unknown_sig(self):
        tracker = CoverageTracker()
        assert tracker.should_deprioritize_archetype("unknown") is False

    def test_summary(self):
        tracker = CoverageTracker()
        tracker.record_archetype("listing", "sig1")
        tracker.record_feature("search")
        s = tracker.summary()
        assert s["archetypes_seen"]["listing"] == 1
        assert s["signatures_seen"] == 1
        assert "search" in s["features_tested"]
        assert isinstance(s["is_saturated"], bool)

    def test_custom_saturation_thresholds(self):
        tracker = CoverageTracker(
            min_archetypes_before_stop=1,
            min_features_before_stop=2,
        )
        tracker.record_archetype("listing", "sig1")
        tracker.record_feature("f1")
        assert tracker.is_saturated() is False
        tracker.record_feature("f2")
        assert tracker.is_saturated() is True

    def test_saturation_can_be_disabled(self):
        tracker = CoverageTracker(
            stop_on_saturation=False,
            min_archetypes_before_stop=1,
            min_features_before_stop=1,
        )
        tracker.record_archetype("listing", "sig1")
        tracker.record_feature("f1")
        assert tracker.is_saturated() is False

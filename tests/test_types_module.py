"""Coverage and contract checks for typed runtime-shape aliases."""

from __future__ import annotations

import flowscout.core.types as types_module


def test_types_module_exports_expected_shapes() -> None:
    """Core TypedDict aliases should be importable and present."""
    assert hasattr(types_module, "RawElement")
    assert hasattr(types_module, "PageAnalysis")
    assert hasattr(types_module, "NetworkError")

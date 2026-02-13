"""Model-based testing primitives."""

from __future__ import annotations

from flowscout.mbt.coverage import ModelCoverage, compute_model_coverage
from flowscout.mbt.walker import ModelWalker

__all__ = [
    "ModelCoverage",
    "ModelWalker",
    "compute_model_coverage",
]

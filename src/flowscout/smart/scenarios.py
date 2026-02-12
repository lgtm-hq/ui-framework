"""Backward-compatible import shim for moved modeling module."""

from __future__ import annotations

from flowscout.modeling import scenarios as _scenarios_module

_EXPORTED_NAMES = [name for name in dir(_scenarios_module) if not name.startswith("__")]
__all__ = [name for name in _EXPORTED_NAMES if not name.startswith("_")]
globals().update({name: getattr(_scenarios_module, name) for name in _EXPORTED_NAMES})

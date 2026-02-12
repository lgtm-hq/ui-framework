"""Layer 2 modeling package: site semantics built from exploration data."""

from __future__ import annotations

from flowscout.modeling import archetype as _archetype_module
from flowscout.modeling import components as _components_module
from flowscout.modeling import flows as _flows_module
from flowscout.modeling import scenarios as _scenarios_module
from flowscout.modeling import site_model as _site_model_module

_modules = (
    _archetype_module,
    _components_module,
    _flows_module,
    _scenarios_module,
    _site_model_module,
)
__all__ = sorted(
    {name for module in _modules for name in dir(module) if not name.startswith("_")}
)
for _module in _modules:
    globals().update(
        {name: getattr(_module, name) for name in dir(_module) if name in __all__}
    )

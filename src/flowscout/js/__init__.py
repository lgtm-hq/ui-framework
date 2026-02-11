"""Runtime loader for browser-injected JavaScript scripts."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_JS_DIR = Path(__file__).parent
_DIST_DIR = _JS_DIR / "dist"


@lru_cache(maxsize=16)
def load_script(name: str) -> str:
    """Load a compiled JavaScript script by name from ``dist/``.

    Requires ``tsc`` to have been run first (``just build-js``).
    """
    compiled = _DIST_DIR / f"{name}.js"
    if compiled.exists():
        return compiled.read_text()

    if (_JS_DIR / f"{name}.ts").exists():
        msg = (
            f"TypeScript source found for '{name}' but compiled JS is missing. "
            f"Run 'just build-js' to compile TypeScript scripts."
        )
        raise RuntimeError(msg)

    msg = f"Script not found: {name} (looked in {_DIST_DIR})"
    raise FileNotFoundError(msg)

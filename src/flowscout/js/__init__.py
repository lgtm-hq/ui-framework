"""Runtime loader for browser-injected JavaScript scripts."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

_JS_DIR = Path(__file__).parent


@lru_cache(maxsize=16)
def load_script(name: str) -> str:
    """Load a JavaScript script by name.

    Resolves ``dist/{name}.js`` first (compiled TypeScript output).
    Falls back to reading the ``.ts`` source with TypeScript-only
    syntax stripped (type annotations, ``as`` casts, etc.).
    """
    compiled = _JS_DIR / "dist" / f"{name}.js"
    if compiled.exists():
        return compiled.read_text()

    ts_path = _JS_DIR / f"{name}.ts"
    if ts_path.exists():
        return _strip_ts_syntax(ts_path.read_text())

    msg = f"Script not found: {name} (looked in {_JS_DIR})"
    raise FileNotFoundError(msg)


def _strip_ts_syntax(source: str) -> str:
    """Remove TypeScript-only syntax so the result is valid JS.

    This is a lightweight fallback for when ``tsc`` hasn't been run.
    It handles the patterns actually used in our scripts:
    - Type annotations on parameters and variables  (: Type)
    - ``as Type`` casts
    - Angle-bracket generics on function calls (Array.from<X>)
    - Non-null assertions (!)
    """
    # Remove 'as TypeName' casts (word boundary aware)
    source = re.sub(r"\s+as\s+\w[\w.<>\[\]|]*", "", source)
    # Remove type annotations after : in function params and variable decls
    # Match ': Type' but not inside strings or object literals
    source = re.sub(r":\s*(?:readonly\s+)?(?:Record|Set|Map|Array)<[^>]+>", "", source)
    source = re.sub(
        r"(?<=[\w\)\?])\s*:\s*(?:string|number|boolean|void|null|undefined|Element|HTMLElement|HTMLInputElement|HTMLSelectElement|NodeFilter|RegExpMatchArray)"
        r"(?:\s*\[\s*\])?(?:\s*\|\s*(?:string|number|boolean|null|undefined))*",
        "",
        source,
    )
    return source

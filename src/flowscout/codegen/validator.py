"""Validation helpers for generated code artifacts."""

from __future__ import annotations

import ast
import json
import py_compile
import re
import shutil
import subprocess  # nosec B404 - used without shell for local compiler invocation
import tempfile
from pathlib import Path
from typing import Callable, Iterable


class CodegenValidationError(ValueError):
    """Raised when generated code validation fails."""


def validate_python_sources(*, paths: Iterable[str | Path]) -> None:
    """Validate generated Python files by compiling them with ``py_compile``."""
    candidate_paths = _normalize_paths(paths=paths)
    errors: list[str] = []
    for path in candidate_paths:
        try:
            py_compile.compile(file=str(path), doraise=True)
        except py_compile.PyCompileError as exc:  # pragma: no cover - defensive
            errors.append(f"{path}: {exc.msg}")

    if errors:
        raise CodegenValidationError(
            "Generated Python code failed to compile:\n" + "\n".join(errors),
        )


def validate_python_imports(
    *,
    test_file: str | Path,
    package_root: str | Path,
    package_prefix: str = "pages",
) -> None:
    """Validate that generated test imports resolve to on-disk modules."""
    test_path = Path(test_file).resolve()
    root = Path(package_root).resolve()
    module = ast.parse(test_path.read_text())
    missing_modules: list[str] = []

    for node in ast.walk(module):
        if not isinstance(node, ast.ImportFrom):
            continue
        if not node.module:
            continue
        if node.module != package_prefix and not node.module.startswith(
            f"{package_prefix}.",
        ):
            continue

        module_rel_path = Path(*node.module.split("."))
        module_file = root / module_rel_path.with_suffix(".py")
        package_file = root / module_rel_path / "__init__.py"
        if module_file.exists() or package_file.exists():
            continue
        missing_modules.append(node.module)

    if missing_modules:
        unique_missing = sorted(set(missing_modules))
        raise CodegenValidationError(
            "Generated test imports do not resolve: " + ", ".join(unique_missing),
        )


def validate_python_playwright_api(*, paths: Iterable[str | Path]) -> None:
    """Validate Python Playwright API usage patterns in generated sources."""
    forbidden_patterns = (
        (r"\.toBeVisible\(", "to_be_visible"),
        (r"\.toHaveURL\(", "to_have_url"),
        (r"\.toHaveTitle\(", "to_have_title"),
        (r"\.waitForLoadState\(", "wait_for_load_state"),
        (r"\.isChecked\(", "is_checked"),
    )
    _validate_forbidden_patterns(
        paths=paths,
        forbidden_patterns=forbidden_patterns,
        language="python",
    )


def validate_typescript_playwright_api(*, paths: Iterable[str | Path]) -> None:
    """Validate TypeScript Playwright API usage patterns in generated sources."""
    forbidden_patterns = (
        (r"\.to_be_visible\(", "toBeVisible"),
        (r"\.to_have_url\(", "toHaveURL"),
        (r"\.to_have_title\(", "toHaveTitle"),
        (r"\.wait_for_load_state\(", "waitForLoadState"),
        (r"\.is_checked\(", "isChecked"),
    )
    _validate_forbidden_patterns(
        paths=paths,
        forbidden_patterns=forbidden_patterns,
        language="typescript",
    )


def validate_typescript_sources(
    *,
    paths: Iterable[str | Path],
    cwd: str | Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> None:
    """Validate generated TypeScript with ``tsc --noEmit``."""
    candidate_paths = _normalize_paths(paths=paths)
    tsc_binary = shutil.which("tsc")
    if tsc_binary is None:
        raise CodegenValidationError(
            "TypeScript validation requires `tsc` but it was not found in PATH.",
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        stub_path = temp_dir / "playwright-test.d.ts"
        stub_path.write_text(_playwright_test_stub())

        tsconfig_path = temp_dir / "tsconfig.json"
        tsconfig_payload = {
            "compilerOptions": {
                "target": "ES2020",
                "module": "CommonJS",
                "moduleResolution": "Node",
                "strict": True,
                "skipLibCheck": True,
                "noEmit": True,
            },
            "files": [str(path) for path in candidate_paths] + [str(stub_path)],
        }
        tsconfig_path.write_text(json.dumps(tsconfig_payload, indent=2))

        command = [
            tsc_binary,
            "-p",
            str(tsconfig_path),
            "--noEmit",
            "--pretty",
            "false",
        ]
        command_runner = runner or subprocess.run
        completed = command_runner(  # nosec B603 - fixed binary, no shell
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            check=False,
            text=True,
        )
        if completed.returncode != 0:
            output = completed.stderr.strip() or completed.stdout.strip()
            raise CodegenValidationError(
                "Generated TypeScript failed `tsc --noEmit` validation:\n"
                f"{output or 'Unknown TypeScript compiler error.'}",
            )


def _normalize_paths(*, paths: Iterable[str | Path]) -> list[Path]:
    """Normalize and validate file paths."""
    normalized = [Path(path).resolve() for path in paths]
    missing = [path for path in normalized if not path.exists()]
    if missing:
        raise CodegenValidationError(
            "Validation paths do not exist: "
            + ", ".join(str(path) for path in missing),
        )
    return normalized


def _validate_forbidden_patterns(
    *,
    paths: Iterable[str | Path],
    forbidden_patterns: tuple[tuple[str, str], ...],
    language: str,
) -> None:
    """Validate that no forbidden API spellings appear in source files."""
    candidate_paths = _normalize_paths(paths=paths)
    issues: list[str] = []
    for path in candidate_paths:
        text = path.read_text()
        for pattern, expected in forbidden_patterns:
            if re.search(pattern, text):
                issues.append(
                    f"{path}: found `{pattern}`; expected Playwright `{expected}`",
                )
    if issues:
        raise CodegenValidationError(
            f"Generated {language} code uses invalid Playwright API forms:\n"
            + "\n".join(issues),
        )


def _playwright_test_stub() -> str:
    """Return a minimal ``@playwright/test`` declaration for type-checking."""
    return """
declare module '@playwright/test' {
  export interface Locator {
    click(): Promise<void>;
    fill(value: string): Promise<void>;
    press(key: string): Promise<void>;
    first(): Locator;
    nth(index: number): Locator;
    isChecked(): Promise<boolean>;
  }

  export interface Keyboard {
    press(key: string): Promise<void>;
  }

  export interface Page {
    goto(url: string): Promise<void>;
    waitForLoadState(state?: string): Promise<void>;
    locator(selector: string): Locator;
    fill(selector: string, value: string): Promise<void>;
    press(selector: string, key: string): Promise<void>;
    click(selector: string): Promise<void>;
    getByRole(
      role: string,
      options?: { name?: string },
    ): Locator;
    keyboard: Keyboard;
  }

  export interface LocatorAssertions {
    toBeVisible(): Promise<void>;
  }

  export interface PageAssertions {
    toHaveTitle(title: string | RegExp): Promise<void>;
    toHaveURL(url: string | RegExp): Promise<void>;
  }

  export function expect(target: Locator): LocatorAssertions;
  export function expect(target: Page): PageAssertions;

  export interface TestFn {
    (
      title: string,
      fn: (args: { page: Page }) => Promise<void>,
    ): void;
    describe(title: string, fn: () => void): void;
  }

  export const test: TestFn;
}
""".strip()

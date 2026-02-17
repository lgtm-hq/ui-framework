"""Writes rendered POM files to disk."""

from __future__ import annotations

from pathlib import Path

from flowscout.codegen.adapters.base import POMAdapter
from flowscout.codegen.pom_model import POMClass, POMSuite


def write_pom_suite(
    suite: POMSuite,
    adapter: POMAdapter,
    output_dir: str,
) -> list[str]:
    """Write all POM files for a suite. Returns list of generated file paths."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []

    # Base page
    base_path = out / adapter.base_page_filename()
    base_path.write_text(adapter.render_base_page(suite.base_page))
    generated.append(str(base_path))

    # Shared components
    if suite.components:
        components_dir = out / "components"
        components_dir.mkdir(parents=True, exist_ok=True)
        for component in suite.components:
            filename = adapter.class_to_filename(component.class_name)
            path = components_dir / filename
            path.write_text(adapter.render_component(component))
            generated.append(str(path))

    # Page objects
    for page in suite.pages:
        filename = adapter.class_to_filename(page.class_name)
        path = out / filename
        path.write_text(adapter.render_page(page))
        generated.append(str(path))

    return generated


def render_previews(
    page_classes: dict[str, POMClass],
    python_adapter: POMAdapter,
    ts_adapter: POMAdapter,
) -> dict[str, dict[str, str]]:
    """Render in-memory previews for HTML report embedding.

    Args:
        page_classes: page_type_id -> POMClass mapping.
        python_adapter: Adapter for Python rendering.
        ts_adapter: Adapter for TypeScript rendering.

    Returns:
        Mapping of page_type_id -> {class_name, python, typescript}.
    """
    previews: dict[str, dict[str, str]] = {}
    for page_type_id, pom_class in page_classes.items():
        previews[page_type_id] = {
            "class_name": pom_class.class_name,
            "python": python_adapter.render_page(pom_class),
            "typescript": ts_adapter.render_page(pom_class),
        }
    return previews

"""Content expectation verification by page archetype."""

from __future__ import annotations

from pydantic import BaseModel, Field

from flowscout.modeling.archetype import PageAnalysis, PageArchetype


class ContentExpectation(BaseModel):
    """A single content expectation for a page."""

    description: str
    check_type: str
    selector_hint: str = ""
    met: bool = False
    actual_value: str = ""


class ExpectationResult(BaseModel):
    """Result of checking content expectations against a page."""

    page_archetype: PageArchetype
    expectations: list[ContentExpectation] = Field(default_factory=list)
    pass_count: int = 0
    total_count: int = 0
    summary: str = ""


# Archetype → list of expectation definitions
_ARCHETYPE_EXPECTATIONS: dict[PageArchetype, list[dict[str, str]]] = {
    PageArchetype.DETAIL: [
        {
            "description": "Page has a primary heading (h1 or h2)",
            "check_type": "heading_present",
            "selector_hint": "h1, h2",
        },
        {
            "description": "Page has substantial text content (>200 chars)",
            "check_type": "text_content_present",
            "selector_hint": "p, .description",
        },
        {
            "description": "Page has at least one image",
            "check_type": "image_present",
            "selector_hint": "img",
        },
    ],
    PageArchetype.LISTING: [
        {
            "description": "Page has multiple repeated items (>= 2)",
            "check_type": "repeated_items_present",
            "selector_hint": "",
        },
        {
            "description": "Items have consistent structure",
            "check_type": "consistent_structure",
            "selector_hint": "",
        },
    ],
    PageArchetype.SEARCH_RESULTS: [
        {
            "description": "Search results are present",
            "check_type": "results_present",
            "selector_hint": "",
        },
        {
            "description": "Search input is visible",
            "check_type": "search_input_present",
            "selector_hint": "input[type='search']",
        },
    ],
    PageArchetype.FORM: [
        {
            "description": "Form has input fields",
            "check_type": "form_inputs_present",
            "selector_hint": "input, textarea, select",
        },
        {
            "description": "Form has a heading or label",
            "check_type": "heading_present",
            "selector_hint": "h1, h2, legend",
        },
    ],
}


class ExpectationChecker:
    """Verifies content expectations using PageAnalysis data."""

    def check(self, analysis: PageAnalysis) -> ExpectationResult:
        """Check content expectations for the page's archetype.

        Uses data already in PageAnalysis — no additional browser calls.
        """
        archetype = analysis.archetype
        expectation_defs = _ARCHETYPE_EXPECTATIONS.get(archetype, [])

        expectations: list[ContentExpectation] = []
        for defn in expectation_defs:
            exp = ContentExpectation(
                description=defn["description"],
                check_type=defn["check_type"],
                selector_hint=defn.get("selector_hint", ""),
            )
            exp.met, exp.actual_value = self._evaluate(exp.check_type, analysis)
            expectations.append(exp)

        pass_count = sum(1 for e in expectations if e.met)
        total_count = len(expectations)
        summary = (
            f"{pass_count}/{total_count} expectations met for {archetype.value}"
            if total_count > 0
            else f"No expectations defined for {archetype.value}"
        )

        return ExpectationResult(
            page_archetype=archetype,
            expectations=expectations,
            pass_count=pass_count,
            total_count=total_count,
            summary=summary,
        )

    def _evaluate(self, check_type: str, analysis: PageAnalysis) -> tuple[bool, str]:
        """Evaluate a single check against the analysis data."""
        density = analysis.content_density

        if check_type == "heading_present":
            met = density.heading_count > 0
            return met, f"{density.heading_count} headings"

        if check_type == "text_content_present":
            met = density.total_text_length > 200
            return met, f"{density.total_text_length} chars"

        if check_type == "image_present":
            met = density.image_count > 0
            return met, f"{density.image_count} images"

        if check_type == "repeated_items_present":
            max_count = max(
                (rs.item_count for rs in analysis.repeated_structures), default=0
            )
            met = max_count >= 2
            return met, f"{max_count} items in largest group"

        if check_type == "consistent_structure":
            # All repeated groups share a tag signature
            sigs = {rs.tag_signature for rs in analysis.repeated_structures}
            met = len(analysis.repeated_structures) > 0
            return met, f"{len(sigs)} unique structures"

        if check_type == "results_present":
            max_count = max(
                (rs.item_count for rs in analysis.repeated_structures), default=0
            )
            met = max_count >= 1
            return met, f"{max_count} results"

        if check_type == "search_input_present":
            met = analysis.has_search
            return met, "search input found" if met else "no search input"

        if check_type == "form_inputs_present":
            met = density.form_input_count > 0
            return met, f"{density.form_input_count} inputs"

        return False, "unknown check"

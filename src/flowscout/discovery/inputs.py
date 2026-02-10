"""Heuristic input data generation for form fields."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flowscout.discovery.context import ContextStore
    from flowscout.discovery.elements import InteractiveElement

# Pattern key → {scenario → value}
# Keys are matched against field name, aria-label, placeholder (lowercased)
FIELD_PATTERNS: dict[str, dict[str, str]] = {
    # Email
    "email": {"valid": "testuser@example.com", "invalid": "not-an-email"},
    "e-mail": {"valid": "testuser@example.com", "invalid": "not-an-email"},
    # Password
    "password": {"valid": "SecureP@ss123!", "invalid": "x"},
    "passwd": {"valid": "SecureP@ss123!", "invalid": "x"},
    # Name
    "full_name": {"valid": "Jane Doe", "invalid": ""},
    "fullname": {"valid": "Jane Doe", "invalid": ""},
    "first_name": {"valid": "Jane", "invalid": ""},
    "firstname": {"valid": "Jane", "invalid": ""},
    "last_name": {"valid": "Doe", "invalid": ""},
    "lastname": {"valid": "Doe", "invalid": ""},
    "name": {"valid": "Jane Doe", "invalid": ""},
    "username": {"valid": "janedoe42", "invalid": ""},
    "user": {"valid": "janedoe42", "invalid": ""},
    # Contact
    "phone": {"valid": "+12025551234", "invalid": "abc"},
    "telephone": {"valid": "+12025551234", "invalid": "abc"},
    "tel": {"valid": "+12025551234", "invalid": "abc"},
    "mobile": {"valid": "+12025551234", "invalid": "abc"},
    # Address
    "address": {"valid": "123 Main St", "invalid": ""},
    "street": {"valid": "123 Main St", "invalid": ""},
    "city": {"valid": "Springfield", "invalid": ""},
    "state": {"valid": "IL", "invalid": ""},
    "zip": {"valid": "62701", "invalid": "abc"},
    "zipcode": {"valid": "62701", "invalid": "abc"},
    "postal": {"valid": "62701", "invalid": "abc"},
    "country": {"valid": "US", "invalid": ""},
    # URL
    "url": {"valid": "https://example.com", "invalid": "not-a-url"},
    "website": {"valid": "https://example.com", "invalid": "not-a-url"},
    "homepage": {"valid": "https://example.com", "invalid": "not-a-url"},
    # Numeric
    "age": {"valid": "30", "invalid": "-1"},
    "quantity": {"valid": "1", "invalid": "-999"},
    "amount": {"valid": "100.00", "invalid": "abc"},
    "price": {"valid": "29.99", "invalid": "abc"},
    "number": {"valid": "42", "invalid": "abc"},
    # Date
    "date": {"valid": "2025-01-15", "invalid": "not-a-date"},
    "birthday": {"valid": "1990-06-15", "invalid": "not-a-date"},
    "dob": {"valid": "1990-06-15", "invalid": "not-a-date"},
    # Search
    "search": {"valid": "test query", "invalid": ""},
    "query": {"valid": "test query", "invalid": ""},
    "q": {"valid": "test query", "invalid": ""},
    # Text/comment
    "message": {"valid": "This is a test message.", "invalid": ""},
    "comment": {"valid": "This is a test comment.", "invalid": ""},
    "description": {"valid": "Test description text.", "invalid": ""},
    "bio": {"valid": "A brief biography.", "invalid": ""},
    "note": {"valid": "A test note.", "invalid": ""},
    "subject": {"valid": "Test Subject", "invalid": ""},
    "title": {"valid": "Test Title", "invalid": ""},
}

# HTML5 input type → pattern key
TYPE_TO_PATTERN: dict[str, str] = {
    "email": "email",
    "tel": "phone",
    "number": "number",
    "url": "url",
    "date": "date",
    "datetime-local": "date",
    "password": "password",
    "search": "search",
}


def generate_input_value(
    element: InteractiveElement,
    scenario: str = "valid",
    *,
    input_profile: str = "safe",
    context_store: ContextStore | None = None,
) -> str:
    """Backward-compatible wrapper returning only the generated value."""
    value, _ = generate_input_value_with_source(
        element,
        scenario=scenario,
        input_profile=input_profile,
        context_store=context_store,
    )
    return value


def generate_input_value_with_source(
    element: InteractiveElement,
    scenario: str = "valid",
    *,
    input_profile: str = "safe",
    context_store: ContextStore | None = None,
) -> tuple[str, str]:
    """Generate a value for an input field based on heuristics.

    Resolution order:
    0. Context store (for search fields in smart mode)
    1. HTML5 input type (email, tel, number, url, date, search, password)
    2. Field name/id pattern matching
    3. Placeholder text analysis
    4. ARIA label analysis
    5. Fallback based on input type
    """
    # 0. Smart mode: use context store for search fields
    if (
        input_profile == "contextual"
        and context_store is not None
        and scenario == "valid"
        and _is_search_field(element)
    ):
        query = context_store.get_search_query()
        if query:
            return query, "context_store_search_entity"

    # 1. Check HTML5 type
    if element.input_type and element.input_type in TYPE_TO_PATTERN:
        pattern_key = TYPE_TO_PATTERN[element.input_type]
        if pattern_key in FIELD_PATTERNS:
            return (
                FIELD_PATTERNS[pattern_key].get(
                    scenario, FIELD_PATTERNS[pattern_key]["valid"]
                ),
                f"input_type:{pattern_key}",
            )

    # 2. Match field identifiers against known patterns
    identifiers = " ".join(
        filter(
            None,
            [element.name, element.aria_label, element.placeholder, element.label],
        ),
    ).lower()

    # Try exact key matches first, then substring matches
    for pattern_key, values in _ordered_field_patterns():
        if _pattern_in_identifiers(pattern_key=pattern_key, identifiers=identifiers):
            return (
                values.get(scenario, values["valid"]),
                f"field_pattern:{pattern_key}",
            )

    # 3. Fallback
    if scenario == "valid":
        if input_profile == "safe":
            return "test input", "fallback:safe"
        return "test input value", "fallback:contextual"
    return "", "fallback:invalid_empty"


def _is_search_field(element: InteractiveElement) -> bool:
    """Check if an element is a search-related input field."""
    if element.input_type == "search":
        return True
    identifiers = " ".join(
        filter(
            None,
            [element.name, element.aria_label, element.placeholder, element.label],
        ),
    ).lower()
    return any(kw in identifiers for kw in ("search", "query", " q "))


def _pattern_in_identifiers(*, pattern_key: str, identifiers: str) -> bool:
    """Match pattern keys against identifiers using token boundaries."""
    normalized_identifiers = re.sub(r"[^a-z0-9]+", " ", identifiers).strip()
    normalized_pattern = re.sub(r"[^a-z0-9]+", " ", pattern_key).strip()
    if not normalized_identifiers or not normalized_pattern:
        return False
    escaped = re.escape(normalized_pattern)
    regex = re.compile(rf"\b{escaped}\b")
    return bool(regex.search(normalized_identifiers))


def _ordered_field_patterns() -> list[tuple[str, dict[str, str]]]:
    """Return field patterns with domain-critical credentials matched first."""
    preferred = ("username", "user", "email", "password", "passwd")
    rows: list[tuple[str, dict[str, str]]] = []
    seen: set[str] = set()

    for key in preferred:
        if key in FIELD_PATTERNS:
            rows.append((key, FIELD_PATTERNS[key]))
            seen.add(key)

    for key, values in FIELD_PATTERNS.items():
        if key in seen:
            continue
        rows.append((key, values))
    return rows

"""Heuristic-based outcome detection for action results."""

from __future__ import annotations

from flowscout.discovery.actions import OutcomeType

# CSS selectors that indicate error states
ERROR_SELECTORS = [
    ".error",
    ".alert-error",
    ".alert-danger",
    ".validation-error",
    ".form-error",
    ".field-error",
    ".invalid-feedback",
    "[aria-invalid='true']",
]

# CSS selectors that indicate success states
SUCCESS_SELECTORS = [
    ".success",
    ".alert-success",
    ".notification-success",
]

# JavaScript to scan for visible error messages
FIND_ERRORS_JS = """
(selectors) => {
    const errors = [];
    for (const sel of selectors) {
        const elements = document.querySelectorAll(sel);
        for (const el of elements) {
            if (el.offsetParent !== null || getComputedStyle(el).position === 'fixed') {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    const text = el.textContent.trim();
                    if (text) errors.push(text);
                }
            }
        }
    }
    return errors;
}
"""


class OutcomeDetector:
    """Classifies action outcomes using heuristics."""

    def __init__(
        self,
        *,
        error_selectors: list[str] | None = None,
        success_selectors: list[str] | None = None,
    ) -> None:
        self.error_selectors = error_selectors or ERROR_SELECTORS
        self.success_selectors = success_selectors or SUCCESS_SELECTORS

    def classify(
        self,
        *,
        url_before: str,
        url_after: str,
        dom_hash_before: str,
        dom_hash_after: str,
        error_messages: list[str],
        console_errors: list[str],
        network_errors: list[dict[str, str]],
    ) -> OutcomeType:
        """Classify the outcome of an action based on observable signals."""
        # 1. URL changed → navigation
        if url_before != url_after:
            return OutcomeType.NAVIGATION

        # 2. Network errors (4xx, 5xx)
        for resp in network_errors:
            status = int(resp.get("status", 200))
            if status >= 400:
                return OutcomeType.NETWORK_ERROR

        # 3. Console errors
        if console_errors:
            return OutcomeType.CONSOLE_ERROR

        # 4. Validation errors in DOM
        if error_messages:
            return OutcomeType.VALIDATION_ERROR

        # 5. DOM structure changed
        if dom_hash_before != dom_hash_after:
            return OutcomeType.DOM_CHANGE

        # 6. No observable change
        return OutcomeType.NO_CHANGE

    async def find_error_messages(self, page: object) -> list[str]:
        """Scan the current page for visible error messages."""
        try:
            errors = await page.evaluate(FIND_ERRORS_JS, self.error_selectors)  # type: ignore[union-attr]
            return [e for e in errors if e]
        except Exception:
            return []

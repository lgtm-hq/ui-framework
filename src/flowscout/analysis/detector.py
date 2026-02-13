"""Heuristic-based outcome detection for action results."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from flowscout.core.state import PageBlockReason
from flowscout.discovery.actions import OutcomeType

logger = logging.getLogger(__name__)

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


PAGE_BLOCK_SCAN_JS = """
() => {
    const title = document.title || '';
    const bodyText = document.body?.innerText || '';
    const consentSelectors = [
        '.onetrust-banner-sdk',
        '#onetrust-banner-sdk',
        '#CybotCookiebotDialog',
        '.cookie-banner',
        '[id*="cookie-consent"]',
        '[class*="cookie-consent"]',
        '[id*="consent"]',
        '[class*="consent"]',
        '[aria-label*="cookie"]',
    ];

    return {
        title,
        bodyText: bodyText.slice(0, 20000),
        hasRecaptcha: Boolean(
            document.querySelector(
                ".g-recaptcha, iframe[src*='recaptcha'], script[src*='recaptcha']"
            )
        ),
        hasHCaptcha: Boolean(
            document.querySelector(
                ".h-captcha, iframe[src*='hcaptcha'], script[src*='hcaptcha']"
            )
        ),
        hasTurnstile: Boolean(
            document.querySelector(
                ".cf-turnstile, iframe[src*='challenges.cloudflare.com'],"
                + " script[src*='turnstile'], script[src*='challenges.cloudflare.com']"
            )
        ),
        hasConsentWall: consentSelectors.some((selector) =>
            Boolean(document.querySelector(selector))
        ),
    };
}
"""


@dataclass(frozen=True)
class PageBlockDetection:
    """Result of blocked-page detection for the current page."""

    is_blocked: bool
    reason: PageBlockReason = PageBlockReason.NONE
    detail: str = ""


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

    async def find_error_messages(self, page: Any) -> list[str]:
        """Scan the current page for visible error messages."""
        try:
            errors = await page.evaluate(FIND_ERRORS_JS, self.error_selectors)
            return [e for e in errors if e]
        except (AttributeError, RuntimeError, OSError):
            logger.debug("Error scanning for error messages", exc_info=True)
            return []


async def detect_page_block(
    *,
    page: Any,
    status_code: int | None = None,
) -> PageBlockDetection:
    """Detect access blocks/CAPTCHAs using status code + page content signals."""
    if status_code in {401, 403}:
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.ACCESS_DENIED,
            detail=f"HTTP {status_code} response from page navigation",
        )

    snapshot = await _scan_page_block_signals(page=page)
    title = str(snapshot.get("title", "")).strip()
    body_text = str(snapshot.get("bodyText", "")).strip()
    lowered_text = f"{title}\n{body_text}".lower()

    if (
        bool(snapshot.get("hasRecaptcha"))
        or bool(snapshot.get("hasHCaptcha"))
        or bool(snapshot.get("hasTurnstile"))
        or _contains_any(
            lowered_text,
            (
                "captcha",
                "verify you are human",
                "i am human",
                "human verification",
            ),
        )
    ):
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.CAPTCHA,
            detail="CAPTCHA challenge detected in page content",
        )

    if _contains_any(
        lowered_text,
        (
            "access denied",
            "forbidden",
            "not authorized",
            "unauthorized",
            "permission denied",
            "403",
        ),
    ):
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.ACCESS_DENIED,
            detail="Access denied/forbidden text detected in page title or body",
        )

    if bool(snapshot.get("hasConsentWall")) or _contains_any(
        lowered_text,
        (
            "cookie consent",
            "manage cookies",
            "accept all cookies",
            "reject all cookies",
            "privacy preferences",
            "your privacy choices",
        ),
    ):
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.CONSENT_WALL,
            detail="Cookie consent wall detected in page content",
        )

    if _contains_any(
        lowered_text,
        (
            "just a moment",
            "checking your browser",
            "attention required",
            "security check",
            "cloudflare",
            "ddos protection",
        ),
    ):
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.WAF_CHALLENGE,
            detail="WAF/challenge page markers detected",
        )

    if status_code in {429, 503}:
        return PageBlockDetection(
            is_blocked=True,
            reason=PageBlockReason.BLOCKED_UNKNOWN,
            detail=f"Potential blocked page (HTTP {status_code})",
        )

    return PageBlockDetection(is_blocked=False)


async def _scan_page_block_signals(*, page: Any) -> dict[str, Any]:
    """Collect key signals for blocked-page detection."""
    try:
        payload = await page.evaluate(PAGE_BLOCK_SCAN_JS)
    except (AttributeError, RuntimeError, OSError):
        logger.debug("Could not evaluate blocked-page signals", exc_info=True)
        return {}

    return payload if isinstance(payload, dict) else {}


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True when any normalized pattern exists in text."""
    lowered = str(text or "").lower()
    return any(pattern in lowered for pattern in patterns)

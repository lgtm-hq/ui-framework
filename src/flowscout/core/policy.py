"""Action safety policy evaluation for exploration runs."""

from __future__ import annotations

from pydantic import BaseModel, Field

from flowscout.discovery.actions import Action, ActionType

_DEFAULT_BLOCKED_KEYWORDS = (
    "delete",
    "remove",
    "destroy",
    "checkout",
    "purchase",
    "buy",
    "pay",
    "payment",
    "place order",
    "confirm order",
    "submit order",
    "create account",
    "sign up",
    "register",
)


class ActionPolicyConfig(BaseModel):
    """Runtime policy for non-destructive exploration behavior."""

    enforce_non_destructive: bool = True
    block_form_submissions: bool = True
    block_high_impact_actions: bool = True
    blocked_keywords: list[str] = Field(
        default_factory=lambda: list(_DEFAULT_BLOCKED_KEYWORDS),
    )
    allow_label_patterns: list[str] = Field(default_factory=list)
    allow_target_selectors: list[str] = Field(default_factory=list)


def get_action_policy_block_reason(
    action: Action,
    policy: ActionPolicyConfig,
) -> str | None:
    """Return the reason an action is blocked by policy, or ``None`` if allowed."""
    if not policy.enforce_non_destructive:
        return None

    surfaces = _collect_action_surfaces(action=action)
    if _is_allowlisted(action=action, policy=policy, surfaces=surfaces):
        return None

    if action.action_type == ActionType.SUBMIT_FORM and policy.block_form_submissions:
        return "form submissions are blocked by non-destructive policy"

    if not policy.block_high_impact_actions:
        return None

    for keyword in policy.blocked_keywords:
        normalized_keyword = _normalize_text(keyword)
        if not normalized_keyword:
            continue

        for surface in surfaces:
            if normalized_keyword in surface:
                return f"matched risky keyword '{keyword}'"

    return None


def _collect_action_surfaces(action: Action) -> list[str]:
    """Collect normalized text surfaces used for policy matching."""
    values: list[str | None] = [
        action.label,
        action.target_selector,
        action.metadata.get("href"),
        action.metadata.get("form_selector"),
        action.metadata.get("url"),
        action.metadata.get("requires_open"),
    ]

    if action.intent:
        values.append(action.intent.target_description)
        values.append(action.intent.expected_effect)

    surfaces: list[str] = []
    for value in values:
        normalized = _normalize_text(value)
        if normalized:
            surfaces.append(normalized)
    return surfaces


def _is_allowlisted(
    action: Action,
    policy: ActionPolicyConfig,
    surfaces: list[str],
) -> bool:
    """Check whether an action should bypass destructive checks."""
    normalized_selector = _normalize_text(action.target_selector)
    allowed_selectors = {_normalize_text(v) for v in policy.allow_target_selectors}
    if normalized_selector and normalized_selector in allowed_selectors:
        return True

    allow_patterns = [_normalize_text(v) for v in policy.allow_label_patterns]
    allow_patterns = [pattern for pattern in allow_patterns if pattern]

    if not allow_patterns:
        return False

    for pattern in allow_patterns:
        for surface in surfaces:
            if pattern in surface:
                return True
    return False


def _normalize_text(value: str | None) -> str:
    """Normalize values for case-insensitive substring matching."""
    if not value:
        return ""
    return " ".join(value.casefold().split())

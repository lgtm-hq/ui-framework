"""Tests for non-destructive action policy behavior."""

from flowscout.core.policy import ActionPolicyConfig, get_action_policy_block_reason
from flowscout.discovery.actions import Action, ActionType


def _make_action(
    *,
    action_type: ActionType,
    label: str,
    selector: str = "button#action",
    metadata: dict[str, str] | None = None,
) -> Action:
    return Action(
        action_id="action-1",
        action_type=action_type,
        target_selector=selector,
        label=label,
        metadata=metadata or {},
    )


def test_blocks_submit_form_actions_by_default() -> None:
    policy = ActionPolicyConfig()
    action = _make_action(
        action_type=ActionType.SUBMIT_FORM,
        label="Submit form: #checkout",
    )

    reason = get_action_policy_block_reason(action=action, policy=policy)

    assert reason is not None
    assert "form submissions" in reason


def test_allows_submit_form_actions_when_enabled() -> None:
    policy = ActionPolicyConfig(block_form_submissions=False)
    action = _make_action(
        action_type=ActionType.SUBMIT_FORM,
        label="Submit form: #contact",
    )

    reason = get_action_policy_block_reason(action=action, policy=policy)

    assert reason is None


def test_blocks_high_impact_click_by_keyword() -> None:
    policy = ActionPolicyConfig()
    action = _make_action(
        action_type=ActionType.CLICK,
        label="Click: Delete account",
    )

    reason = get_action_policy_block_reason(action=action, policy=policy)

    assert reason is not None
    assert "delete" in reason


def test_allowlist_selector_overrides_keyword_block() -> None:
    policy = ActionPolicyConfig(
        allow_target_selectors=["button#delete-account"],
    )
    action = _make_action(
        action_type=ActionType.CLICK,
        label="Click: Delete account",
        selector="button#delete-account",
    )

    reason = get_action_policy_block_reason(action=action, policy=policy)

    assert reason is None


def test_allowlist_pattern_overrides_keyword_block() -> None:
    policy = ActionPolicyConfig(
        allow_label_patterns=["delete account"],
    )
    action = _make_action(
        action_type=ActionType.CLICK,
        label="Click: Delete account",
    )

    reason = get_action_policy_block_reason(action=action, policy=policy)

    assert reason is None

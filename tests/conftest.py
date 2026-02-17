"""Shared test fixtures and factory functions."""

from __future__ import annotations

import hashlib
import uuid
from typing import Any

import pytest

from flowscout.analysis.graph import ExplorationResult, Flow
from flowscout.core.archetypes import CatalogEntry, PageArchetype, PageCatalog, ZoneType
from flowscout.core.state import PageState
from flowscout.discovery.actions import Action, ActionResult, ActionType, OutcomeType
from flowscout.discovery.elements import InteractiveElement

TEST_URL = "https://example.com"


def make_catalog(
    archetype: PageArchetype = PageArchetype.LISTING,
    entries: list[CatalogEntry] | None = None,
    url_pattern: str = "",
) -> PageCatalog:
    """Create a PageCatalog with sensible defaults."""
    if entries is None:
        entries = [
            CatalogEntry(
                selector="a[href='/home']",
                tag="a",
                label="Home",
                zone_type=ZoneType.NAVIGATION,
                element_type="link",
                semantic_name="home",
            ),
            CatalogEntry(
                selector="input[type='search']",
                tag="input",
                label="Search",
                zone_type=ZoneType.SEARCH,
                element_type="input_search",
                input_type="search",
                semantic_name="search",
            ),
            CatalogEntry(
                selector=".movie-card",
                tag="div",
                label="Movie 1",
                zone_type=ZoneType.MAIN_CONTENT,
                element_type="other",
                semantic_name="movie_1",
            ),
        ]
    return PageCatalog(archetype=archetype, url_pattern=url_pattern, entries=entries)


def make_state(
    *,
    state_id: str | None = None,
    url: str = TEST_URL,
    title: str = "Test Page",
    depth: int = 0,
) -> PageState:
    """Create a PageState with sensible defaults."""
    sid = state_id or f"state-{uuid.uuid4().hex[:8]}"
    fp = hashlib.sha256(sid.encode()).hexdigest()
    return PageState(
        state_id=sid,
        url=url,
        title=title,
        fingerprint=fp,
        depth=depth,
        dom_structure_hash=f"dom-{sid}",
        visible_text_hash=f"text-{sid}",
        form_state_hash=f"form-{sid}",
    )


def make_action(
    *,
    action_id: str | None = None,
    action_type: ActionType = ActionType.CLICK,
    label: str = "Click button",
    selector: str = "button#submit",
    value: str | None = None,
    metadata: dict[str, str] | None = None,
) -> Action:
    """Create an Action with sensible defaults."""
    aid = action_id or f"action-{uuid.uuid4().hex[:8]}"
    return Action(
        action_id=aid,
        action_type=action_type,
        target_selector=selector,
        label=label,
        value=value,
        metadata=metadata or {},
    )


def make_action_result(
    *,
    action_id: str = "a0",
    source_state_id: str = "s0",
    target_state_id: str = "s1",
    outcome: OutcomeType = OutcomeType.NAVIGATION,
    duration_ms: float = 100.0,
    url_before: str = TEST_URL,
    url_after: str = f"{TEST_URL}/next",
) -> ActionResult:
    """Create an ActionResult with sensible defaults."""
    return ActionResult(
        action_id=action_id,
        source_state_id=source_state_id,
        target_state_id=target_state_id,
        outcome=outcome,
        duration_ms=duration_ms,
        url_before=url_before,
        url_after=url_after,
    )


def make_exploration_result(
    *,
    start_url: str = TEST_URL,
    num_states: int = 2,
    num_flows: int = 1,
    duration_seconds: float = 60.0,
) -> ExplorationResult:
    """Create an ExplorationResult with sensible defaults."""
    states = {}
    for i in range(num_states):
        sid = f"state-{i}"
        states[sid] = make_state(
            state_id=sid,
            url=f"{start_url}/page{i}" if i > 0 else start_url,
            title=f"Page {i}",
            depth=i,
        )

    actions = {
        "act-0": make_action(
            action_id="act-0",
            label="Click link",
            selector="a#link-0",
        ),
    }

    src = "state-0"
    tgt = f"state-{min(1, num_states - 1)}"
    results = [
        make_action_result(
            action_id="act-0",
            source_state_id=src,
            target_state_id=tgt,
            url_before=start_url,
            url_after=f"{start_url}/page1",
        ),
    ]

    flows = [
        Flow(
            flow_id=f"flow-{i}",
            name=f"Flow {i}",
            description=f"Test flow {i}",
            state_ids=list(states.keys()),
            action_ids=list(actions.keys()),
            outcomes=[OutcomeType.NAVIGATION],
            depth=1,
        )
        for i in range(num_flows)
    ]

    return ExplorationResult(
        config={"start_url": start_url},
        started_at="2025-01-01T00:00:00Z",
        finished_at="2025-01-01T00:01:00Z",
        duration_seconds=duration_seconds,
        states=states,
        actions=actions,
        results=results,
        flows=flows,
        stats={"total_states": num_states},
    )


def make_element(
    *,
    element_id: str | None = None,
    selector: str = "button#submit",
    element_type: str = "button",
    label: str = "Submit",
    **kwargs: object,
) -> InteractiveElement:
    """Create an InteractiveElement with sensible defaults."""
    defaults: dict[str, object] = {
        "element_id": element_id or f"elem-{uuid.uuid4().hex[:8]}",
        "selector": selector,
        "element_type": element_type,
        "label": label,
        "tag": "button",
        "priority": 25,
        "group": "default",
        "metadata": {},
    }
    defaults.update(kwargs)
    return InteractiveElement.model_validate(defaults)


@pytest.fixture
def sample_element_data() -> dict[str, Any]:
    """Sample raw element data as returned by the discovery JS."""
    return {
        "selector": 'a[href="/themes/"]',
        "tag": "a",
        "input_type": None,
        "role": None,
        "aria_label": None,
        "aria_expanded": None,
        "href": "/themes/",
        "name": None,
        "placeholder": None,
        "value": None,
        "required": False,
        "disabled": False,
        "visible": True,
        "label": "Themes",
        "options": [],
        "parent_form": None,
        "bbox": {"x": 100, "y": 20, "width": 60, "height": 30},
        "data_attrs": {},
    }


@pytest.fixture
def sample_form_element_data() -> dict[str, Any]:
    """Sample form input element data."""
    return {
        "selector": 'input[name="email"]',
        "tag": "input",
        "input_type": "email",
        "role": None,
        "aria_label": "Email address",
        "aria_expanded": None,
        "href": None,
        "name": "email",
        "placeholder": "Enter your email",
        "value": "",
        "required": True,
        "disabled": False,
        "visible": True,
        "label": "Email address",
        "options": [],
        "parent_form": "#login-form",
        "bbox": {"x": 100, "y": 100, "width": 200, "height": 40},
        "data_attrs": {},
    }

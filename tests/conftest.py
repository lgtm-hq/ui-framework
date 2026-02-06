"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_element_data() -> dict:
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
def sample_form_element_data() -> dict:
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

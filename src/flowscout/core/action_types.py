"""Shared action and outcome enums used across layers."""

from __future__ import annotations

from enum import StrEnum, auto


class ActionType(StrEnum):
    CLICK = auto()
    FILL = auto()
    SELECT_OPTION = auto()
    CHECK = auto()
    UNCHECK = auto()
    SUBMIT_FORM = auto()
    PRESS_KEY = auto()
    HOVER = auto()
    NAVIGATE = auto()


class OutcomeType(StrEnum):
    NAVIGATION = auto()
    DOM_CHANGE = auto()
    VISUAL_CHANGE = auto()
    NO_CHANGE = auto()
    VALIDATION_ERROR = auto()
    NETWORK_ERROR = auto()
    CONSOLE_ERROR = auto()
    TIMEOUT = auto()
    EXCEPTION = auto()

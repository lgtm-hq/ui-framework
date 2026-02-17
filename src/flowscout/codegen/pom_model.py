"""Framework-agnostic intermediate POM representation."""

from __future__ import annotations

from enum import StrEnum, auto

from pydantic import BaseModel, Field

from flowscout.modeling.archetype import PageArchetype, ZoneType


class PropertyKind(StrEnum):
    """What kind of page property this is."""

    LOCATOR = auto()
    COMPONENT = auto()


class MethodKind(StrEnum):
    """Classification of generated methods."""

    NAVIGATE = auto()
    SEARCH = auto()
    SELECT_ITEM = auto()
    FILL = auto()
    CLICK = auto()
    ASSERT_VISIBLE = auto()
    OPEN = auto()
    CLOSE = auto()
    SELECT_OPTION = auto()
    SWITCH_TAB = auto()
    NEXT_PAGE = auto()
    PREVIOUS_PAGE = auto()
    TOGGLE = auto()
    IS_CHECKED = auto()
    FILL_AND_SUBMIT = auto()


class POMProperty(BaseModel):
    """A single property in a POM class."""

    name: str
    selector: str
    zone: ZoneType = ZoneType.MAIN_CONTENT
    zone_label: str = ""
    kind: PropertyKind = PropertyKind.LOCATOR
    component_class_name: str = ""
    element_type: str = ""


class POMMethod(BaseModel):
    """A generated method in a POM class."""

    kind: MethodKind
    name: str
    parameters: list[tuple[str, str]] = Field(default_factory=list)
    target_property: str = ""
    selector: str = ""


class POMClass(BaseModel):
    """A single POM class (page or component)."""

    class_name: str
    parent_class: str = ""
    archetype: PageArchetype = PageArchetype.UNKNOWN
    url_pattern: str = ""
    base_url: str = ""
    properties: list[POMProperty] = Field(default_factory=list)
    methods: list[POMMethod] = Field(default_factory=list)
    is_component: bool = False
    component_name: str = ""
    component_zone: ZoneType = ZoneType.MAIN_CONTENT


class POMSuite(BaseModel):
    """Complete set of POM classes for a site."""

    base_page: POMClass = Field(default_factory=lambda: POMClass(class_name="BasePage"))
    components: list[POMClass] = Field(default_factory=list)
    pages: list[POMClass] = Field(default_factory=list)

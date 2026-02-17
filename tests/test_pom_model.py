"""Tests for the intermediate POM model."""

from __future__ import annotations

from flowscout.codegen.pom_model import (
    MethodKind,
    POMClass,
    POMMethod,
    POMProperty,
    POMSuite,
    PropertyKind,
)
from flowscout.modeling.archetype import PageArchetype, ZoneType


class TestPOMProperty:
    def test_defaults(self) -> None:
        prop = POMProperty(name="home", selector="a[href='/']")
        assert prop.kind == PropertyKind.LOCATOR
        assert prop.zone == ZoneType.MAIN_CONTENT
        assert prop.component_class_name == ""

    def test_component_kind(self) -> None:
        prop = POMProperty(
            name="nav",
            selector="",
            kind=PropertyKind.COMPONENT,
            component_class_name="NavigationComponent",
        )
        assert prop.kind == PropertyKind.COMPONENT


class TestPOMMethod:
    def test_navigate(self) -> None:
        method = POMMethod(kind=MethodKind.NAVIGATE, name="navigate")
        assert method.kind == MethodKind.NAVIGATE
        assert method.parameters == []

    def test_with_parameters(self) -> None:
        method = POMMethod(
            kind=MethodKind.SEARCH,
            name="search",
            parameters=[("query", "str")],
        )
        assert len(method.parameters) == 1
        assert method.parameters[0] == ("query", "str")


class TestPOMClass:
    def test_defaults(self) -> None:
        pom = POMClass(class_name="HomePage")
        assert pom.parent_class == ""
        assert pom.archetype == PageArchetype.UNKNOWN
        assert pom.properties == []
        assert pom.methods == []
        assert pom.is_component is False

    def test_with_parent(self) -> None:
        pom = POMClass(class_name="MoviePage", parent_class="BasePage")
        assert pom.parent_class == "BasePage"

    def test_serialization_roundtrip(self) -> None:
        pom = POMClass(
            class_name="TestPage",
            archetype=PageArchetype.LISTING,
            properties=[POMProperty(name="link", selector="a")],
            methods=[POMMethod(kind=MethodKind.NAVIGATE, name="navigate")],
        )
        data = pom.model_dump()
        restored = POMClass.model_validate(data)
        assert restored.class_name == "TestPage"
        assert len(restored.properties) == 1
        assert len(restored.methods) == 1


class TestPOMSuite:
    def test_defaults(self) -> None:
        suite = POMSuite()
        assert suite.base_page.class_name == "BasePage"
        assert suite.components == []
        assert suite.pages == []

    def test_with_pages_and_components(self) -> None:
        suite = POMSuite(
            components=[POMClass(class_name="NavComponent", is_component=True)],
            pages=[POMClass(class_name="HomePage")],
        )
        assert len(suite.components) == 1
        assert len(suite.pages) == 1


class TestMethodKind:
    def test_expected_kinds_exist(self) -> None:
        expected = {
            "navigate",
            "search",
            "select_item",
            "fill",
            "click",
            "assert_visible",
            "open",
            "close",
            "select_option",
            "switch_tab",
            "next_page",
            "previous_page",
            "toggle",
            "is_checked",
            "fill_and_submit",
        }
        actual = {kind.value for kind in MethodKind}
        assert expected == actual

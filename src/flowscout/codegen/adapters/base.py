"""Abstract base for POM rendering adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from flowscout.codegen.pom_model import POMClass


class POMAdapter(ABC):
    """Renders POMClass models into language-specific source code."""

    @abstractmethod
    def render_base_page(self, pom_class: POMClass) -> str:
        """Render a BasePage class."""

    @abstractmethod
    def render_component(self, pom_class: POMClass) -> str:
        """Render a shared component class."""

    @abstractmethod
    def render_page(self, pom_class: POMClass) -> str:
        """Render a page object class."""

    @abstractmethod
    def file_extension(self) -> str:
        """Return the file extension (e.g. '.py', '.ts')."""

    @abstractmethod
    def base_page_filename(self) -> str:
        """Return the base page filename (e.g. 'base_page.py')."""

    @abstractmethod
    def class_to_filename(self, class_name: str) -> str:
        """Convert a class name to a filename."""


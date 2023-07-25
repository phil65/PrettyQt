"""Module containing stuff to help buidling docs.

This module builds on mknodes and contains some new nodes to help building documentation,
an ItemModelTable to easily display Qt ItemModels as Markdown Tables
as well as a model + widget to preview a generated mknodes tree.

"""

from __future__ import annotations

from .itemmodeltable import DependencyTable, ItemModelTable
from .markdownmodel import MarkdownModel
from .markdownwidget import MarkdownWidget
from .prettyqtclasspage import PrettyQtClassPage
from .prettyqtdiagram import PrettyQtDiagram
from .propertytable import PropertyTable
from .widgetscreenshot import WidgetScreenShot


__all__ = [
    "ItemModelTable",
    "DependencyTable",
    "MarkdownModel",
    "MarkdownWidget",
    "PrettyQtClassPage",
    "PrettyQtDiagram",
    "PropertyTable",
    "WidgetScreenShot",
]

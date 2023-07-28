"""Module containing stuff to help buidling docs.

This module builds on mknodes and contains some new nodes to help building documentation,
an MkItemModelTable to easily display Qt ItemModels as Markdown Tables
as well as a model + widget to preview a generated mknodes tree.

"""

from __future__ import annotations

from .markdownmodel import MarkdownModel
from .markdownwidget import MarkdownWidget
from .mkitemmodeltable import MkDependencyTable, MkItemModelTable
from .mkprettyqtclasspage import MkPrettyQtClassPage
from .mkprettyqtdiagram import MkPrettyQtDiagram
from .mkpropertytable import MkPropertyTable
from .mkwidgetscreenshot import MkWidgetScreenShot


__all__ = [
    "MkItemModelTable",
    "MkDependencyTable",
    "MarkdownModel",
    "MarkdownWidget",
    "MkPrettyQtClassPage",
    "MkPrettyQtDiagram",
    "MkPropertyTable",
    "MkWidgetScreenShot",
]

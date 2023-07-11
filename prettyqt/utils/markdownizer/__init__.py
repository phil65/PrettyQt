from __future__ import annotations


import logging

from prettyqt.utils.markdownizer.basesection import BaseSection, Text, Code
from prettyqt.utils.markdownizer.image import Image, BinaryImage
from prettyqt.utils.markdownizer.admonition import Admonition
from prettyqt.utils.markdownizer.docs import Docs
from prettyqt.utils.markdownizer.literatenav import LiterateNav
from prettyqt.utils.markdownizer.docstrings import DocStrings
from prettyqt.utils.markdownizer.table import Table
from prettyqt.utils.markdownizer.mermaiddiagram import MermaidDiagram
from prettyqt.utils.markdownizer.document import Document

__all__ = [
    "BaseSection",
    "Docs",
    "LiterateNav",
    "DocStrings",
    "Text",
    "Code",
    "Image",
    "BinaryImage",
    "Document",
    "Admonition",
    "MermaidDiagram",
    "Table",
]


logger = logging.getLogger(__name__)

BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"


def get_qt_help_link(klass):
    mod = klass.__module__.replace("PySide6.", "").replace("PyQt6.", "")
    url = f"{BASE_URL}{mod}/{klass.__qualname__.replace('.', '/')}.html"
    return f"[{klass.__name__}]({url})"


def link_for_class(klass: type) -> str:
    if klass is set:
        return "set"
    if klass.__module__.startswith(("PyQt", "PySide")):
        return get_qt_help_link(klass)
    return f"[{klass.__qualname__}]({klass.__qualname__}.md)"


def label_for_class(klass: type) -> str:
    if klass.__module__.startswith(("PyQt", "PySide")):
        return f"{klass.__module__.split('.')[-1]}.{klass.__name__}"
    elif klass.__module__.startswith(("prettyqt.")):
        parts = klass.__module__.split(".")
        return f"{parts[1]}.{klass.__name__}"
    return klass.__qualname__


class ClassDocument(Document):
    def __init__(self, klass: type, parts: tuple[str, ...] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.klass = klass
        self.parts = parts or ()
        self._build()

    def _build(self):
        self.append(DocStrings(f'{".".join(self.parts)}.{self.klass.__name__}'))
        if table := Table.get_ancestor_table_for_klass(self.klass):
            self.append(table)
        self.append(MermaidDiagram.for_classes([self.klass]))
        # self.append(MermaidDiagram.for_subclasses([self.klass]))


if __name__ == "__main__":
    from prettyqt import core
    from prettyqt.utils import helpers

    doc = Document([], True, True)
    doc += Admonition("info", "etst")
    doc += Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += Table.get_prop_tables_for_klass(core.StringListModel)[0]
    doc += DocStrings(helpers, header="DocStrings")
    doc += Table.get_dependency_table("prettyqt")
    doc += MermaidDiagram.for_classes([Table], header="Mermaid diagram")

    print(doc.to_markdown())
    # print(text)

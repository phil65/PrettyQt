from __future__ import annotations


import logging
from importlib import metadata

from prettyqt.utils.markdownizer.basesection import BaseSection, Text, Code
from prettyqt.utils.markdownizer.image import Image, BinaryImage
from prettyqt.utils.markdownizer.admonition import Admonition
from prettyqt.utils.markdownizer.docs import Docs
from prettyqt.utils.markdownizer.literatenav import LiterateNav
from prettyqt.utils.markdownizer.docstrings import DocStrings
from prettyqt.utils.markdownizer.list import List
from prettyqt.utils.markdownizer.table import Table
from prettyqt.utils.markdownizer.mermaiddiagram import MermaidDiagram
from prettyqt.utils.markdownizer.document import Document, ClassDocument, ModuleDocument
from prettyqt.utils.markdownizer.prettyqtmarkdown import (
    WidgetScreenShot,
    PrettyQtClassDocument,
)

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
    "List",
    "ClassDocument",
    "ModuleDocument",
    "PrettyQtClassDocument",
    "WidgetScreenShot",
]


logger = logging.getLogger(__name__)

BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
BUILTIN_URL = "https://docs.python.org/3/library/functions.html#{klass}"


def link_for_class(klass: type) -> str:
    if klass.__module__ == "builtins":
        return f"[{klass.__name__}]({BUILTIN_URL.format(klass=klass)})"
    elif klass.__module__.startswith(("PyQt", "PySide")):
        mod = klass.__module__.replace("PySide6.", "").replace("PyQt6.", "")
        url = f"{BASE_URL}{mod}/{klass.__qualname__.replace('.', '/')}.html"
        return f"[{klass.__name__}]({url})"
    elif klass.__module__.startswith("prettyqt"):
        return f"[{klass.__qualname__}]({klass.__qualname__}.md)"
    try:
        dist = metadata.distribution(klass.__module__.split(".")[0])
    except metadata.PackageNotFoundError:
        return f"[{klass.__qualname__}]({klass.__qualname__}.md)"
    else:
        if url := dist.metadata["Home-Page"]:
            return f"[{klass.__qualname__}]({url})"
        return f"[{klass.__qualname__}]({klass.__qualname__}.md)"


def label_for_class(klass: type) -> str:
    if klass.__module__.startswith(("PyQt", "PySide")):
        return f"{klass.__module__.split('.')[-1]}.{klass.__name__}"
    elif klass.__module__.startswith(("prettyqt.")):
        parts = klass.__module__.split(".")
        return f"{parts[1]}.{klass.__name__}"
    return klass.__qualname__


def to_html_list(ls: list[str]):
    if not ls:
        return ""
    item_str = "".join(f"<li>{i}</li>" for i in ls)
    return f"<ul>{item_str}</ul>"


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
    from fsspec import AbstractFileSystem

    print(link_for_class(AbstractFileSystem))

    # print(doc.to_markdown())
    # print(text)

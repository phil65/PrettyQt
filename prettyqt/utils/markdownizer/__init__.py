from __future__ import annotations


import logging
import re
from importlib import metadata
import sys

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
BUILTIN_URL = "https://docs.python.org/3/library/{mod}.html#{name}"


def escape_markdown(text: str, version: int = 1, entity_type: str | None = None) -> str:
    """Helper function to escape telegram markup symbols.

    Args:
        text: The text.
        version: Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type: For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in
            ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """
    match version:
        case 1 | "1":
            escape_chars = r"_*`["
        case 2 | "2":
            if entity_type in ["pre", "code"]:
                escape_chars = r"\`"
            elif entity_type == "text_link":
                escape_chars = r"\)"
            else:
                escape_chars = r"_*[]()~`>#+-=|{}.!"
        case _:
            raise ValueError("Markdown version must be either 1 or 2!")

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# import pathlib
# from mkdocstrings import inventory

# path = pathlib.Path(__file__, "../qt6.inv")
# with path.open("rb") as file:
#     inv = inventory.Inventory.parse_sphinx(file)

#     logger.warning(inv.values())


def linked(identifier: str, title: str | None = None) -> str:
    return f"[{identifier if title is None else title}]({identifier}.md)"


def styled(
    text: str,
    size: int | None = None,
    bold: bool = False,
    recursive: bool = False,
    code: bool = False,
) -> str:
    if size:
        text = f"<font size='{size}'>{text}</font>"
    if bold:
        text = f"**{text}**"
    if recursive:
        text = f"*{text}*"
    if code:
        text = f"`{text}`"
    return text


def link_for_class(kls: type, **kwargs) -> str:
    if kls.__module__ == "builtins":
        url = BUILTIN_URL.format(mod="functions", name=kls.__name__)
        link = linked(url, title=kls.__name__)
    elif kls.__module__ in sys.stdlib_module_names:
        mod = kls.__module__
        url = BUILTIN_URL.format(mod=mod, name=f"{mod}.{kls.__name__}")
        link = linked(url, title=kls.__name__)
    elif kls.__module__.startswith(("PyQt", "PySide")):
        mod = kls.__module__.replace("PySide6.", "").replace("PyQt6.", "")
        url = f"{BASE_URL}{mod}/{kls.__qualname__.replace('.', '/')}.html"
        link = linked(url, title=kls.__name__)
    elif kls.__module__.startswith("prettyqt"):
        link = linked(kls.__qualname__)
    try:
        dist = metadata.distribution(kls.__module__.split(".")[0])
    except metadata.PackageNotFoundError:
        link = linked(kls.__qualname__)
    else:
        if url := dist.metadata["Home-Page"]:
            link = linked(url, title=kls.__qualname__)
        else:
            link = linked(kls.__qualname__)
    return styled(link, **kwargs)


def label_for_class(klass: type) -> str:
    if klass.__module__.startswith(("PyQt", "PySide")):
        return f"{klass.__module__.split('.')[-1]}.{klass.__name__}"
    elif klass.__module__.startswith("prettyqt."):
        parts = klass.__module__.split(".")
        return f"{parts[1]}.{klass.__name__}"
    return klass.__qualname__


def to_html_list(
    ls: list[str], shorten_after: int | None = None, make_link: bool = False
):
    if not ls:
        return ""
    item_str = "".join(
        f"<li>{linked(i)}</li>" if make_link else f"<li>{i}</li>"
        for i in ls[:shorten_after]
    )
    if shorten_after and len(ls) > shorten_after:
        item_str += "<li>...</li>"
    return f"<ul>{item_str}</ul>"


if __name__ == "__main__":
    from prettyqt import core
    from prettyqt.utils import helpers

    doc = Document([], True, True)
    doc += Admonition("info", "etst")
    doc += Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += Table.get_property_table(core.StringListModel)
    doc += DocStrings(helpers, header="DocStrings")
    doc += Table.get_dependency_table("prettyqt")
    doc += MermaidDiagram.for_classes([Table], header="Mermaid diagram")
    from fsspec import AbstractFileSystem

    print(link_for_class(AbstractFileSystem))

    # print(doc.to_markdown())
    # print(text)

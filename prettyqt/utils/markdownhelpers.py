from __future__ import annotations

import logging
import typing

from typing import Literal

from prettyqt import core


T = typing.TypeVar("T", bound=type)


logger = logging.getLogger(__name__)

AdmonitionTypeStr = Literal[
    "node",
    "abstract",
    "info",
    "tip",
    "success",
    "question",
    "warning",
    "failure",
    "danger",
    "bug",
    "example",
    "quote",
]


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


def get_class_table(klasses: list[type[core.QObject]]) -> str:
    lines = ["|Name|Child classes|Inherits|Description|", "|--|--|--|--|"]
    for kls in klasses:
        subclasses = kls.__subclasses__()
        parents = kls.__bases__
        subclass_str = ", ".join(link_for_class(subclass) for subclass in subclasses)
        parent_str = ", ".join(link_for_class(parent) for parent in parents)
        desc = kls.__doc__.split("\n")[0] if isinstance(kls.__doc__, str) else ""
        line = f"|{link_for_class(kls)}|{subclass_str}|{parent_str}|{desc}|"
        lines.append(line)
    return "\n\n" + "\n".join(lines) + "\n\n"

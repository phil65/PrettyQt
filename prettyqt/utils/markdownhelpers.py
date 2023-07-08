from __future__ import annotations

import logging
import typing

from typing import Literal

from prettyqt import constants, core


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


def class_name(cls):
    """Return a string representing the class."""
    # NOTE: can be changed to str(class) for more complete class info
    return cls.__name__


def classes_tree(klasses):
    module_classes = set()
    inheritances = []

    def inspect_class(klass):
        if class_name(klass) not in module_classes:
            # if klass.__module__.startswith(base_module):
            module_classes.add(class_name(klass))
            for base in klass.__bases__:
                inheritances.append((class_name(base), class_name(klass)))
                inspect_class(base)

    for klass in klasses:
        inspect_class(klass)
    return module_classes, inheritances


def classes_tree_to_mermaid(klasses, inheritances):
    return "graph TD;\n" + "\n".join(
        list(klasses) + [f"{a} --> {b}" for a, b in inheritances]
    )


def to_mermaid_tree(index: core.ModelIndex, role=constants.DISPLAY_ROLE):
    indexes, inheritances = index_tree([index], role=role)
    text = index_tree_to_mermaid(indexes, inheritances)
    lines = ["\n\n## Index diagram\n\n``` mermaid\n", text, "\n```\n"]
    return "".join(lines)


def index_tree(indexes, role):
    module_classes = set()
    inheritances = []

    def inspect_index(index, role):
        if index.data(role) not in module_classes:
            # if klass.__module__.startswith(base_module):
            module_classes.add(index.data(role))
            # for child_index in index.model().get_child_indexes(index):
            for child_index in index.model().iter_tree(index, depth=1, fetch_more=True):
                inheritances.append((child_index.data(role), index.data(role)))
                inspect_index(child_index, role)

    for index in indexes:
        inspect_index(index, role)
    return module_classes, inheritances


def index_tree_to_mermaid(klasses, inheritances):
    return "graph TD;\n" + "\n".join(
        list(klasses) + [f"{a} --> {b}" for a, b in inheritances]
    )


def get_prop_table(props, user_prop_name: str | None = None) -> str:
    lines = ["|Qt Property|Type|User property|", "|-----------|----|-----------|"]
    for prop in props:
        sections: list[str] = [
            f"`{prop.get_name()}`",
            f"**{(prop.get_meta_type().get_name() or '').rstrip('*')}**",
            "x" if prop.get_name() == user_prop_name else "",
        ]
        lines.append(f"|{'|'.join(sections)}|")
    return "\n".join(lines)


def get_qt_help_link(klass):
    mod = klass.__module__.replace("PySide6.", "").replace("PyQt6.", "")
    url = f"{BASE_URL}{mod}/{klass.__name__}.html"
    return f"[{klass.__name__}]({url})"


def get_prop_tables_for_klass(klass: type[core.QObject]) -> str:
    metaobject = core.MetaObject(klass.staticMetaObject)
    user_prop_name = (
        user_prop.get_name()
        if (user_prop := metaobject.get_user_property()) is not None
        else None
    )
    props_without_super = metaobject.get_properties(include_super=False)
    prop_names_without_super = [p.get_name() for p in props_without_super]
    props_with_super = metaobject.get_properties(include_super=True)
    super_props = [
        p for p in props_with_super if p.get_name() not in prop_names_without_super
    ]
    if not props_with_super:
        return ""
    lines = []
    if props_without_super:
        lines.append("\n## Class Properties\n")
        lines.append(get_prop_table(props_without_super, user_prop_name))
    if super_props:
        lines.append("\n## Inherited properties\n")
        lines.append(get_prop_table(super_props, user_prop_name))
    return "\n\n" + "\n".join(lines) + "\n\n"


def get_admonition(
    typ: AdmonitionTypeStr,
    message: str,
    title: str | None = None,
    collapsible: bool = False,
) -> str:
    block_start = "???" if collapsible else "!!!"
    title = repr(title) if title else ""
    return f"{block_start} {typ} {title}\n     {message}\n\n"


def get_mermaid_for_klass(klass: type) -> str:
    classes, inheritances = classes_tree([klass])
    lines = [
        "\n## ₼ Class diagram\n\n``` mermaid\n",
        classes_tree_to_mermaid(classes, inheritances),
        "```\n",
    ]
    return "\n".join(lines)


def link_for_class(klass: type) -> str:
    if klass is set:
        return "set"
    if klass.__module__.startswith(("PyQt", "PySide")):
        return get_qt_help_link(klass)
    return f"[{klass.__qualname__}]({klass.__qualname__}.md)"


def get_ancestor_table_for_klass(klass: type[core.QObject]) -> str:
    subclasses = klass.__subclasses__()
    if not subclasses:
        return ""
    lines = ["|Class|Module|", "|--------|-----------|"]
    lines.extend(
        f"|{link_for_class(subklass)}|{subklass.__module__}|" for subklass in subclasses
    )
    return "\n\n## Child classes\n\n" + "\n".join(lines) + "\n\n"


def get_image(path: str, caption: str = "") -> str:
    text = f"""
<figure markdown>
  ![Image title](images/{path})
  <figcaption>{caption}</figcaption>
</figure>"""
    return text


def get_class_table(klasses: list[type[core.QObject]]) -> str:
    lines = ["|Name|Module|Child classes|Inherits|", "|--|--|--|--|"]
    for kls in klasses:
        subclasses = kls.__subclasses__()
        parents = kls.__bases__
        subclass_str = ", ".join(link_for_class(subclass) for subclass in subclasses)
        parent_str = ", ".join(link_for_class(parent) for parent in parents)
        line = f"|{link_for_class(kls)}|{kls.__module__}|{subclass_str}|{parent_str}|"
        lines.append(line)
    return "\n\n" + "\n".join(lines) + "\n\n"


def model_to_markdown(
    model: core.AbstractItemModelMixin, use_checkstate_role: bool = True, **kwargs
) -> str:
    data, h_header, v_header = model.get_table_data(**kwargs)
    if use_checkstate_role:
        kwargs["role"] = constants.CHECKSTATE_ROLE
        check_data, _, __ = model.get_table_data(**kwargs)
        for i, row in enumerate(data):
            for j, _column in enumerate(row):
                if check_data[i][j]:
                    data[i][j] = "x"

    lines = [f"|{'|'.join(h_header)}|", f"|{'--|--'.join('' for _ in h_header)}|"]
    for row in data:
        sections = [str(i) if i else "" for i in row]
        lines.append(f"|{'|'.join(sections)}|")
    return "\n".join(lines)

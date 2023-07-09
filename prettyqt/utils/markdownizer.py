from __future__ import annotations

import collections

from collections.abc import Callable, Mapping, Sequence
import dataclasses
import importlib
import logging
import os
import textwrap
import types
import typing
from typing import Literal

from prettyqt.utils import helpers, markdownhelpers


T = typing.TypeVar("T", bound=type)
GraphTypeStr = Literal["TODO"]


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

GraphTypeStr = Literal["TODO"]

BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"

# Link are created following the documentation here :
# https://mermaid.js.org/syntax/flowchart.html#links-between-nodes
LINK_SHAPES = {"normal": "---", "dotted": "-.-", "thick": "==="}

LINK_HEADS = {"none": "", "arrow": ">", "left-arrow": "<", "bullet": "o", "cross": "x"}

HEADER = """---
hide:
{options}
---

"""


@dataclasses.dataclass
class NodeShape:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end


# Shapes are created following the documentation here :
# https://mermaid.js.org/syntax/flowchart.html#node-shapes


NODE_SHAPES = {
    "normal": NodeShape("[", "]"),
    "round-edge": NodeShape("(", ")"),
    "stadium-shape": NodeShape("([", "])"),
    "subroutine-shape": NodeShape("[[", "]]"),
    "cylindrical": NodeShape("[(", ")]"),
    "circle": NodeShape("((", "))"),
    "label-shape": NodeShape(">", "]"),
    "rhombus": NodeShape("{", ")"),
    "hexagon": NodeShape("{{", ")}"),
    "parallelogram": NodeShape("[/", "/]"),
    "parallelogram-alt": NodeShape("[\\", "\\]"),
    "trapezoid": NodeShape("[/", "\\]"),
    "trapezoid-alt": NodeShape("[\\", "/]"),
    "double-circle": NodeShape("(((", ")))"),
}


class Node:
    def __init__(
        self,
        identifier: str,
        content: str = "",
        shape: str = "normal",
        sub_nodes: list = None,
    ):
        sub_nodes = sub_nodes or []
        self.id = helpers.to_snake(identifier)
        self.content = content if content else self.id
        self.shape = NODE_SHAPES[shape]
        self.sub_nodes = sub_nodes

        # TODO: verify that content match a working string pattern

    def add_sub_nodes(self, new_nodes: list[Node] = None):
        if new_nodes is None:
            new_nodes = []
        self.sub_nodes = self.sub_nodes + new_nodes

    def __repr__(self):
        return f"{self.id}['{self.content}'] Nb_children:{len(self.sub_nodes)}"

    def __str__(self):
        return "" + (
            "\n".join(
                [
                    f'subgraph {self.id} ["{self.content}"]',
                    "\n".join([str(node) for node in self.sub_nodes]),
                    "end",
                ]
            )
            if len(self.sub_nodes)
            else "".join([self.id, self.shape.start, f'"{self.content}"', self.shape.end])
        )


class Link:
    def __init__(
        self,
        origin: Node,
        end: Node,
        shape: str = "normal",
        head_left: str = "none",
        head_right: str = "arrow",
        message: str = "",
    ):
        self.origin = origin
        self.end = end
        self.head_left = LINK_HEADS[head_left]
        self.head_right = LINK_HEADS[head_right]
        self.shape = LINK_SHAPES[shape]
        self.message = message

    def __str__(self):
        elements = [
            f"{self.origin.id} ",
            self.head_left,
            self.shape,
            self.head_right,
            f"|{self.message}|" if self.message else "",
            f" {self.end.id}",
        ]
        return "".join(elements)


class MarkdownDocument:
    def __init__(self, items=None, hide_toc: bool = False, hide_nav: bool = False):
        self.items = items or []
        self.options = collections.defaultdict(list)
        if hide_toc:
            self.options["hide"].append("toc")
        if hide_nav:
            self.options["hide"].append("nav")

    def __add__(self, other):
        self.items.append(other)
        return self

    def __iter__(self):
        return iter(self.items)

    def to_markdown(self) -> str:
        header = self.get_header()
        return header + "\n".join(i.to_markdown() for i in self.items)

    def get_header(self) -> str:
        if not self.options:
            return ""
        text = "\n".join(
            [f"  - {i}" for k in self.options.keys() for i in self.options[k]]
        )
        return HEADER.format(options=text)

    def append(self, other):
        self.items.append(other)


class MarkdownText:
    def __init__(self, text: str = ""):
        self.text = text

    def to_markdown(self) -> str:
        return self.text


class MarkdownCode(MarkdownText):
    def __init__(self, language: str, text: str = ""):
        super().__init__(text)
        self.language = language

    def to_markdown(self) -> str:
        return f"``` {self.language}\n{self.text}\n```"


class MarkdownImage:
    def __init__(self, path: str, caption: str, title: str = ""):
        super().__init__()
        self.title = title
        self.caption = caption
        self.path = path

    def to_markdown(self) -> str:
        lines = ["<figure markdown>", f"![{self.title}]({self.path})"]
        if self.caption:
            lines.append(f"  <figcaption>{self.caption}</figcaption>")
        lines.append("</figure>")
        return "\n".join(lines)


class Admonition(MarkdownText):
    def __init__(
        self,
        typ: AdmonitionTypeStr,
        text: str,
        title: str | None = None,
        collapsible: bool = False,
    ):
        super().__init__(text=text)
        self.typ = typ
        self.title = title
        self.collapsible = collapsible

    def to_markdown(self) -> str:
        block_start = "???" if self.collapsible else "!!!"
        title = repr(self.title) if self.title else ""
        text = textwrap.indent(self.text, "    ")
        return f"{block_start} {self.typ} {title}\n{text}\n\n"


class MermaidDiagram(MarkdownCode):
    TYPE_MAP = dict(
        flow_left_right="graph LR",
        sequence="sequenceDiagram",
        state="stateDiagram-v2",
        flow_top_down="graph TD",
    )
    ORIENTATION = dict(
        default="",
        left_right="LR",
        top_down="TD",
        right_left="RL",
        down_top="DT",
    )

    def __init__(
        self,
        graph_type: GraphTypeStr,
        items,
        connections,
        orientation: str = "",
        attributes: dict[str, str] | None = None,
    ):
        super().__init__(language="mermaid")
        self.graph_type = graph_type
        self.orientation = orientation
        self.items = set(items)
        self.connections = set(connections)
        self.attributes = attributes or {}

    @classmethod
    def for_classes(cls, klasses):
        items, connections = helpers.get_connections(
            klasses, child_getter=lambda x: x.__bases__, id_getter=lambda x: x.__name__
        )
        return cls(graph_type="flow_top_down", items=items, connections=connections)

    def to_markdown(self) -> str:
        self.text = f"{self.graph_type} {self.orientation};\n" + "\n".join(
            list(self.items) + [f"{a} --> {b}" for a, b in self.connections]
        )
        return super().to_markdown()


class Table(MarkdownText):
    def __init__(
        self,
        data: Sequence[str] | dict[str, list] | None = None,
        headers: Sequence[Sequence[str]] | None = None,
        column_modifiers: dict[str, Callable] | None = None,
    ):
        column_modifiers = column_modifiers or {}
        match data:
            case Mapping():
                self.data = data
            case (str(), *_):
                self.data = {headers[i]: col for i, col in enumerate(self.data)}
        for k, v in column_modifiers.items():
            self.data[k] = [v(i) for i in self.data[k]]

    @classmethod
    def get_class_table(cls, klasses: list[type]) -> str:
        lines = ["|Name|Module|Child classes|Inherits|", "|--|--|--|--|"]
        for kls in klasses:
            subclasses = kls.__subclasses__()
            parents = kls.__bases__
            subclass_str = ", ".join(
                markdownhelpers.link_for_class(subclass) for subclass in subclasses
            )
            parent_str = ", ".join(
                markdownhelpers.link_for_class(parent) for parent in parents
            )
            link = markdownhelpers.link_for_class(kls)
            line = f"|{link}|{kls.__module__}|{subclass_str}|{parent_str}|"
            lines.append(line)
        return "\n\n" + "\n".join(lines) + "\n\n"

    def to_markdown(self) -> str:
        headers = list(self.data.keys())
        lines = [f"|{'|'.join(headers)}|", f"|{'--|--'.join('' for _ in headers)}|"]
        lines.extend(f"|{'|'.join(row)}|" for row in self.iter_rows())
        return "\n".join(lines)

    def iter_rows(self):
        return (
            [str(self.data[k][j]) for k in self.data.keys()]
            for j, _ in enumerate(self.data)
        )


class DocStringSection(MarkdownText):
    def __init__(self, obj: types.ModuleType | str | os.PathLike | type, **kwargs):
        """Docstring section.

        Possible keyword arguments:

        allow_inspection (bool): Whether to allow inspecting modules when visiting
                                  them is not possible. Default: True.
        show_bases (bool): Show the base classes of a class. Default: True.
        show_source (bool): Show the source code of this object. Default: True.
        preload_modules (list[str] | None): Pre-load modules

        The modules must be listed as an array of strings. Default: None.

        Headings options:

        heading_level (int): The initial heading level to use. Default: 2.
        show_root_heading (bool): Show the heading of the object at the root of the
                                  documentation tree (i.e. the object referenced by
                                  the identifier after :::). Default: False.
        show_root_toc_entry (bool): If the root heading is not shown, at least
                                    add a ToC entry for it. Default: True.
        show_root_full_path (bool): Show the full Python path for the root
                                    object heading. Default: True.
        show_root_members_full_path (bool): Show the full Python path of the
                                            root members. Default: False.
        show_object_full_path (bool): Show the full Python path of every object.
                                      Default: False.
        show_category_heading (bool): When grouped by categories, show a heading
                                      for each category. Default: False.
        show_symbol_type_heading (bool): Show the symbol type in headings (e.g. mod,
                                         class, func and attr). Default: False.
        show_symbol_type_toc (bool): Show the symbol type in the Table of
                                     Contents (e.g. mod, class, func and attr).
                                     Default: False.
        Members options:

        members (list[str] | False | None): An explicit list of members to render.
                                            Default: None.
        members_order (str): The members ordering to use.
                             Options: alphabetical - order by the members names,
                             source - order members as they appear in the
                             source file. Default: "alphabetical".
        filters (list[str] | None): A list of filters applied to filter objects
                                    based on their name. A filter starting with !
                                    will exclude matching objects instead of
                                    including them. The members option takes
                                    precedence over filters (filters will still be
                                    applied recursively to lower members in the
                                    hierarchy). Default: ["!^_[^_]"].
        group_by_category (bool): Group the object's children by categories:
                                  attributes, classes, functions, and modules.
                                  Default: True.
        show_submodules (bool): When rendering a module, show its submodules
                                recursively. Default: False.
        Docstrings options:

        docstring_style (str): The docstring style to use: google, numpy, sphinx,
                               or None. Default: "google".
        docstring_options (dict): The options for the docstring parser. See
                                  parsers under griffe.docstrings.
        docstring_section_style (str): The style used to render docstring sections.
                                       Options: table, list, spacy. Default: "table".
        merge_init_into_class (bool): Whether to merge the __init__ method into
                                      the class' signature and docstring.
                                      Default: False.
        show_if_no_docstring (bool): Show the object heading even if it has no
                                     docstring or children with docstrings.
                                     Default: False.
        show_docstring_attributes (bool): Whether to display the "Attributes"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_description (bool): Whether to display the textual block
                                           (including admonitions) in the object's
                                           docstring. Default: True.
        show_docstring_examples (bool): Whether to display the "Examples"
                                        section in the object's docstring.
                                        Default: True.
        show_docstring_other_parameters (bool): Whether to display the
                                                "Other Parameters" section in the
                                                object's docstring. Default: True.
        show_docstring_parameters (bool): Whether to display the "Parameters"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_raises (bool): Whether to display the "Raises"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_receives (bool): Whether to display the "Receives"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_returns (bool): Whether to display the "Returns"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_warns (bool): Whether to display the "Warns"
                                          section in the object's docstring.
                                          Default: True.
        show_docstring_yields (bool): Whether to display the "Yields"
                                          section in the object's docstring.
                                          Default: True.
        Signatures/annotations options:

        annotations_path (str): The verbosity for annotations path: brief
                                (recommended), or source (as written in the source).
                                Default: "brief".
        line_length (int): Maximum line length when formatting code/signatures.
                           Default: 60.
        show_signature (bool): Show methods and functions signatures. Default: True.
        show_signature_annotations (bool): Show the type annotations in methods
                                           and functions signatures. Default: False.
        signature_crossrefs (bool): Whether to render cross-references for type
                                    annotations in signatures. Default: False.
        separate_signature (bool): Whether to put the whole signature in a code
                                  block below the heading. If Black is installed,
                                  the signature is also formatted using it.
                                  Default: False.
        """
        match obj:
            case types.ModuleType():
                self.module_path = obj.__name__
            case type():
                self.module_path = f"{obj.__module__}.{obj.__qualname__}"
            case str():
                self.module_path = obj
            case os.PathLike():
                mod = importlib.import_module(os.fspath(obj))
                self.module_path = mod.__name__
        self.options = kwargs

    def to_markdown(self) -> str:
        md = f"::: {self.module_path}\n"
        if self.options:
            lines = [f"    {k} : {v}" for k, v in self.options]
            md = md + "\n" + "\n".join(lines)
        return f"\n{md}\n"


if __name__ == "__main__":
    doc = MarkdownDocument([], True, True)
    graph = MermaidDiagram.for_classes([Table])
    doc.append(graph)
    doc += Admonition("info", "etst")

    table = Table(data=dict(a=[1, 2], b=["c", "D"]))
    doc.append(table)
    docstring = DocStringSection(helpers)
    doc.append(docstring)
    print(doc.to_markdown())

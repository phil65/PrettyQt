from __future__ import annotations

import collections

from collections.abc import Callable, Mapping, Sequence
import dataclasses
import importlib
import inspect

import logging
import os
import pathlib
import re
import textwrap
import types
import typing
from typing import Literal

from prettyqt import core
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


class Docs:
    def __init__(self, module_name: str, exclude_modules: list[str] | None = None):
        self.module_name = module_name
        self.root_path = pathlib.Path(f"./{module_name}")
        self._exclude = exclude_modules or []

    def write(self, document):
        pass

    def yield_files(self, glob: str = "*/*.py"):
        for path in sorted(self.root_path.rglob(glob)):
            if (
                all(i not in path.parts for i in self._exclude)
                and not any(i.startswith("__") for i in path.parent.parts)
                and not path.is_dir()
            ):
                yield path.relative_to(self.root_path)

    def yield_klasses_for_module(
        self, mod: types.ModuleType, recursive: bool = False, _seen=None
    ):
        if recursive:
            seen = _seen or set()
            for _submod_name, submod in inspect.getmembers(mod, inspect.ismodule):
                if submod.__name__.startswith(self.module_name) and submod not in seen:
                    seen.add(submod)
                    yield from self.yield_klasses_for_module(
                        submod, recursive=True, _seen=seen
                    )
        for i in inspect.getmembers(mod, inspect.isclass):
            if i[1].__module__.startswith(self.module_name):
                yield i[1]

    def yield_classes_for_glob(
        self, glob="*/*.py", recursive: bool = False, avoid_duplicates: bool = True
    ):
        seen = set()
        for path in self.yield_files(glob):
            module_path = path.with_suffix("")
            parts = tuple(module_path.parts)
            module_path = f"{self.module_name}." + ".".join(parts)
            try:
                module = importlib.import_module(module_path)
            except (ImportError, AttributeError):
                continue
            else:
                for klass in self.yield_klasses_for_module(module, recursive=recursive):
                    if (klass, path) not in seen or not avoid_duplicates:
                        seen.add((klass, path))
                        yield klass, path


class MarkdownDocument:
    def __init__(
        self,
        items: list | None = None,
        hide_toc: bool = False,
        hide_nav: bool = False,
        hide_path: bool = False,
        path: str | os.PathLike = "",
    ):
        self.items = items or []
        self.path = path
        self.options = collections.defaultdict(list)
        if hide_toc:
            self.options["hide"].append("toc")
        if hide_nav:
            self.options["hide"].append("nav")
        if hide_path:
            self.options["hide"].append("path")

    def __add__(self, other):
        self.append(other)
        return self

    def __iter__(self):
        return iter(self.items)

    def write(self, path: str | os.PathLike, edit_path: str | os.PathLike | None = None):
        import mkdocs_gen_files

        with mkdocs_gen_files.open(path, "w") as fd:
            fd.write(self.to_markdown())
            logger.info(f"Written MarkDown file to {path}")
        if edit_path:
            mkdocs_gen_files.set_edit_path(path, edit_path)
            logger.info(f"Setting edit path to {edit_path}")

    def to_markdown(self) -> str:
        header = self.get_header()
        return header + "\n\n".join(i.to_markdown() for i in self.items)

    def get_header(self) -> str:
        if not self.options:
            return ""
        text = "\n".join(
            [f"  - {i}" for k in self.options.keys() for i in self.options[k]]
        )
        return HEADER.format(options=text)

    def append(self, other: str | BaseMarkdownSection):
        if isinstance(other, str):
            other = MarkdownText(other)
        self.items.append(other)


class MarkdownClassDocument(MarkdownDocument):
    def __init__(self, klass: type, parts: tuple[str, ...] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.klass = klass
        self.parts = parts or ()
        self._build()

    def _build(self):
        self.append(DocStringSection(f'{".".join(self.parts)}.{self.klass.__name__}'))
        if table := Table.get_ancestor_table_for_klass(self.klass):
            self.append(table)
        self.append(MermaidDiagram.for_classes([self.klass]))
        # self.append(MermaidDiagram.for_subclasses([self.klass]))


class BaseMarkdownSection:
    def __init__(self, header: str = ""):
        self.header = header

    def __str__(self):
        return self.to_markdown()

    def to_markdown(self):
        text = self._to_markdown() + "\n"
        if self.header:
            return f"## {self.header}\n\n{text}"
        return text


# class TabWidget(Admonition):
#     def __init__(
#         self,
#         items=None,
#     ):
#         super().__init__(header=header)
#         self.items = items or []
#         self.title = title

#     def _to_markdown(self) -> str:
#         lines = [f'!!! Example "{self.title}"']

#         for item in self.items:
#             header = f"=== {header!r}"
#             text = textwrap.indent(item.to_markdown(), "        ")


class MarkdownText(BaseMarkdownSection):
    def __init__(self, text: str | BaseMarkdownSection = "", header: str = ""):
        super().__init__(header=header)
        self.text = text

    def _to_markdown(self) -> str:
        return self.text if isinstance(self.text, str) else self.text.to_markdown()


class MarkdownCode(MarkdownText):
    def __init__(
        self, language: str, text: str | BaseMarkdownSection = "", header: str = ""
    ):
        super().__init__(text, header)
        self.language = language

    def _to_markdown(self) -> str:
        return f"``` {self.language}\n{self.text}\n```"


class MarkdownImage(BaseMarkdownSection):
    def __init__(
        self, path: str, caption: str, title: str = "Image title", header: str = ""
    ):
        super().__init__(header=header)
        self.title = title
        self.caption = caption
        self.path = path

    def _to_markdown(self) -> str:
        lines = ["<figure markdown>", f"  ![{self.title}]({self.path})"]
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

    def _to_markdown(self) -> str:
        block_start = "???" if self.collapsible else "!!!"
        title = repr(self.title) if self.title else ""
        text = textwrap.indent(self.text, "    ")
        return f"{block_start} {self.typ} {title}\n{text}\n\n"


class BinaryImage(MarkdownImage):
    def __init__(
        self,
        data: bytes,
        path: str,
        caption: str = "",
        title: str = "Image title",
        header: str = "",
    ):
        super().__init__(path=path, header=header, caption=caption, title=title)
        self.data = data

    def _to_markdown(self) -> str:
        import pathlib

        import mkdocs_gen_files

        path = pathlib.Path(self.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with mkdocs_gen_files.open(self.path, "wb") as file:
            file.write(self.data)
        logger.info(f"Written image to {self.path}")
        return super()._to_markdown()


class MermaidDiagram(MarkdownCode):
    TYPE_MAP = dict(
        flow="graph",
        sequence="sequenceDiagram",
        state="stateDiagram-v2",
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
        header: str = "",
    ):
        super().__init__(language="mermaid", header=header)
        self.graph_type = (
            graph_type if graph_type not in self.TYPE_MAP else self.TYPE_MAP[graph_type]
        )
        self.orientation = (
            orientation
            if orientation not in self.ORIENTATION
            else self.ORIENTATION[orientation]
        )
        self.items = set(items)
        self.connections = set(connections)
        self.attributes = attributes or {}

    @classmethod
    def for_classes(cls, klasses, header: str = ""):
        items, connections = helpers.get_connections(
            klasses, child_getter=lambda x: x.__bases__
        )
        items = [label_for_class(i) for i in items]
        connections = [(label_for_class(i), label_for_class(j)) for i, j in connections]
        return cls(
            graph_type="flow",
            orientation="TD",
            items=items,
            connections=connections,
            header=header,
        )

    @classmethod
    def for_subclasses(cls, klasses, header: str = ""):
        items, connections = helpers.get_connections(
            klasses,
            child_getter=lambda x: x.__subclasses__(),
            id_getter=lambda x: x.__name__,
        )
        return cls(
            graph_type="flow",
            orientation="RL",
            items=items,
            connections=connections,
            header=header,
        )

    def _to_markdown(self) -> str:
        items = list(self.items) + [f"{a} --> {b}" for a, b in self.connections]
        item_str = textwrap.indent("\n".join(items), "  ")
        text = f"{self.graph_type} {self.orientation}\n{item_str}"
        return f"```mermaid\n{text}\n```"


class Table(MarkdownText):
    def __init__(
        self,
        data: Sequence[Sequence[str]] | Sequence[dict] | dict[str, list] | None = None,
        columns: Sequence[str] | None = None,
        column_modifiers: dict[str, Callable[[str], str]] | None = None,
        header: str = "",
    ):
        super().__init__(header=header)
        column_modifiers = column_modifiers or {}
        match data:
            case Mapping():
                self.data = {str(k): [str(i) for i in v] for k, v in data.items()}
            case ((str(), *_), *_):
                h = columns or [str(i) for i in range(len(data))]
                self.data = {h[i]: col for i, col in enumerate(data)}
            case (dict(), *_):
                self.data = v = {k: [dic[k] for dic in data] for k in data[0]}
        for k, v in column_modifiers.items():
            self.data[k] = [v(i) for i in self.data[k]]

    @classmethod
    def get_property_table(
        cls, props, user_prop_name: str | None = None, header: str = ""
    ) -> Table:
        lines = []
        headers = ["Qt Property", "Type", "User property"]
        for prop in props:
            sections: list[str] = [
                f"`{prop.get_name()}`",
                f"**{(prop.get_meta_type().get_name() or '').rstrip('*')}**",
                "x" if prop.get_name() == user_prop_name else "",
            ]
            lines.append(sections)
        return cls(columns=headers, data=list(zip(*lines)), header=header)

    @classmethod
    def get_prop_tables_for_klass(cls, klass: type[core.QObject]) -> list[Table]:
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
            return []
        lines = []
        if props_without_super:
            item = cls.get_property_table(
                props_without_super, user_prop_name, header="Class Properties"
            )
            lines.append(item)
        if super_props:
            item = cls.get_property_table(
                super_props, user_prop_name, header="Inherited Properties"
            )
            lines.append(item)
        return lines

    @classmethod
    def get_classes_table(
        cls,
        klasses: list[type],
        filter_fn: Callable | None = None,
    ) -> Table:
        """Create a table containing information about a list of classes.

        Includes columns for child and parent classes including links.
        """
        ls = []
        if filter_fn is None:
            filter_fn = lambda _: True
        for kls in klasses:
            subclasses = [subkls for subkls in kls.__subclasses__() if filter_fn(subkls)]
            parents = kls.__bases__
            subclass_str = ", ".join(link_for_class(sub) for sub in subclasses)
            parent_str = ", ".join(link_for_class(parent) for parent in parents)
            desc = [
                kls.__doc__.split("\n")[0] if kls.__doc__ else "" for kls in subclasses
            ]
            data = dict(
                Name=link_for_class(kls),
                # Module=kls.__module__,
                Children=subclass_str,
                Inherits=parent_str,
                Description=desc,
            )
            ls.append(data)
        return cls(ls)

    @classmethod
    def get_dependency_table(cls, distribution):
        from prettyqt import itemmodels

        model = itemmodels.ImportlibTreeModel("prettyqt")
        list(model.iter_tree(depth=2))
        proxy = itemmodels.ColumnOrderProxyModel(
            order=["Name", "Constraints", "Extra", "Summary", "Homepage"],
            source_model=model,
        )
        return cls.from_itemmodel(proxy)

    @classmethod
    def get_ancestor_table_for_klass(cls, klass: type[core.QObject]) -> Table | None:
        subclasses = klass.__subclasses__()
        if not subclasses:
            return None
        # STRIP_CODE = r"```[^\S\r\n]*[a-z]*\n.*?\n```"
        # docs = [re.sub(STRIP_CODE, '', k.__module__, 0, re.DOTALL) for k in subclasses]
        desc = [kls.__doc__.split("\n")[0] if kls.__doc__ else "" for kls in subclasses]
        data = dict(
            Class=[link_for_class(kls) for kls in subclasses],
            Module=[kls.__module__ for kls in subclasses],
            Description=desc,
        )
        return cls(data=data, header="Child classes")

    @classmethod
    def from_itemmodel(
        cls,
        model: core.AbstractItemModelMixin,
        use_checkstate_role: bool = True,
        **kwargs,
    ) -> Table:
        from prettyqt import constants

        data, h_header, _ = model.get_table_data(**kwargs)
        if use_checkstate_role:
            kwargs["role"] = constants.CHECKSTATE_ROLE
            check_data, _, __ = model.get_table_data(**kwargs)
            for i, row in enumerate(data):
                for j, _column in enumerate(row):
                    if check_data[i][j]:
                        data[i][j] = "x"
        data = list(zip(*data))
        return cls(data, columns=h_header)

    def _to_markdown(self) -> str:
        # print(self.data)
        headers = [str(i) for i in self.data.keys()]
        lines = [f"|{'|'.join(headers)}|", f"|{'--|--'.join('' for _ in headers)}|"]
        lines.extend(f"|{'|'.join(row)}|" for row in self._iter_rows())
        return "\n".join(lines)

    def _iter_rows(self):
        length = min(len(i) for i in self.data.values())
        for j, _ in enumerate(range(length)):
            yield [self.data[k][j] or "" for k in self.data.keys()]


class DocStringSection(MarkdownText):
    def __init__(
        self, obj: types.ModuleType | str | os.PathLike | type, header: str = "", **kwargs
    ):
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
        super().__init__(header=header)
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

    def _to_markdown(self) -> str:
        md = f"::: {self.module_path}\n"
        if self.options:
            lines = [f"    {k} : {v}" for k, v in self.options]
            md = md + "\n" + "\n".join(lines)
        return f"{md}\n"


class LiterateNav(BaseMarkdownSection):
    def __init__(
        self,
        mapping: dict[str | tuple[str, ...], str] | None = None,
        indentation: int | str = "",
    ):
        import mkdocs_gen_files

        super().__init__()
        self.nav = mkdocs_gen_files.Nav()
        if mapping:
            for k, v in mapping.items():
                self.nav[k] = v

    def write(self, path: str = "SUMMARY.md"):
        import mkdocs_gen_files

        logger.info(f"Written SUMMARY to {path}")
        with mkdocs_gen_files.open(path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())


if __name__ == "__main__":
    doc = MarkdownDocument([], True, True)
    doc += Admonition("info", "etst")
    doc += Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += Table.get_prop_tables_for_klass(core.StringListModel)[0]
    doc += DocStringSection(helpers, header="DocStrings")
    doc += Table.get_dependency_table("prettyqt")
    doc += MermaidDiagram.for_classes([Table], header="Mermaid diagram")

    print(doc.to_markdown())
    logger.info(markdownhelpers.get_mermaid_for_klass(Table))
    # print(text)

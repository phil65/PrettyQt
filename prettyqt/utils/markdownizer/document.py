from __future__ import annotations

import collections
import logging
import os
import pathlib
import types

import mkdocs_gen_files

from prettyqt.utils import classhelpers, markdownizer


logger = logging.getLogger(__name__)

HEADER = "---\n{options}\n---\n\n"


class Document:
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
        self.header_options = collections.defaultdict(list)
        if hide_toc:
            self.header_options["hide"].append("toc")
        if hide_nav:
            self.header_options["hide"].append("nav")
        if hide_path:
            self.header_options["hide"].append("path")

    def __add__(self, other):
        self.append(other)
        return self

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return self.to_markdown()

    def write(self, edit_path: str | os.PathLike | None = None):
        with mkdocs_gen_files.open(self.path, "w") as fd:
            fd.write(self.to_markdown())
            logger.info(f"Written MarkDown file to {self.path}")
        if edit_path:
            mkdocs_gen_files.set_edit_path(self.path, edit_path)
            logger.info(f"Setting edit path to {edit_path}")

    def to_markdown(self) -> str:
        header = self.get_header()
        content_str = "\n\n".join(i.to_markdown() for i in self.items)
        return header + content_str if header else content_str

    def get_header(self) -> str:
        lines = []
        keys = self.header_options.keys()
        if not keys:
            return ""
        for option in keys:
            lines.append(f"{option}:")
            lines.extend(f"  - {area}" for area in self.header_options[option])
        return HEADER.format(options="\n".join(lines))

    def append(self, other: str | markdownizer.BaseSection):
        if isinstance(other, str):
            other = markdownizer.Text(other)
        self.items.append(other)


class ClassDocument(Document):
    def __init__(
        self,
        klass: type,
        module_path: tuple[str, ...] | str | None = None,
        path: str | os.PathLike = "",
        **kwargs,
    ):
        """Document showing info about a class.

        Arguments:
            klass: class to show info for
            module_path: If given, overrides module returned by class.__module__
                         This can be useful if you want to link to an aliased class
                         (for example a class imported to __init__.py)
            path: some path for the file.
            kwargs: keyword arguments passed to base class
        """
        path = pathlib.Path(path).with_name(f"{klass.__name__}.md")
        super().__init__(path=path, **kwargs)
        self.klass = klass
        match module_path:
            case None:
                self.parts = klass.__module__.split(".")
            case _:
                self.parts = classhelpers.to_module_parts(module_path)
        self._build()
        self.write()

    def _build(self):
        module_path = ".".join(self.parts)
        self.append(
            markdownizer.DocStrings(
                f"{module_path}.{self.klass.__name__}", header="DocStrings"
            ),
        )
        if table := markdownizer.Table.get_ancestor_table_for_klass(self.klass):
            self.append(table)
        self.append(
            markdownizer.MermaidDiagram.for_classes(
                [self.klass], header="Inheritance diagram"
            ),
        )
        # self.append(markdownizer.MermaidDiagram.for_subclasses([self.klass]))


class ModuleDocument(Document):
    """Document showing info about a module.

    Arguments:
        module: ModuleType or path to model to show info for.
        module: Some path for the file.
        docstrings: Whether to show docstrings for given module.
        show_class_table: ModuleType or path to model to show info for.
    """

    def __init__(
        self,
        module: tuple[str, ...] | str | types.ModuleType,
        path: str | os.PathLike = "",
        *,
        docstrings: bool = False,
        show_class_table: bool = True,
        **kwargs,
    ):
        path = pathlib.Path(path).with_name("index.md")
        super().__init__(path=path, **kwargs)
        self.parts = classhelpers.to_module_parts(module)
        self.module = classhelpers.to_module(self.parts)
        self.docstrings = docstrings
        self.show_class_table = show_class_table
        self._build()
        self.write()

    def _build(self):
        if doc := self.module.__doc__:
            self.append(doc)
        if self.docstrings:
            self.append(markdownizer.DocStrings(f'{".".join(self.parts)}'))
        if self.show_class_table:
            klasses = list(
                classhelpers.iter_classes_for_module(
                    self.parts, module_filter=self.parts[0]
                )
            )
            self.append(markdownizer.Table.get_classes_table(klasses))


if __name__ == "__main__":
    doc = Document()
    print(doc.to_markdown())
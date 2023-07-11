from __future__ import annotations

import collections
import logging
import os
import types

import mkdocs_gen_files

from prettyqt.utils import classhelpers, markdownizer


logger = logging.getLogger(__name__)

HEADER = """---
hide:
{options}
---

"""


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

    def append(self, other: str | markdownizer.BaseSection):
        if isinstance(other, str):
            other = markdownizer.Text(other)
        self.items.append(other)


class ClassDocument(Document):
    def __init__(
        self, klass: type, module_path: tuple[str, ...] | str | None = None, **kwargs
    ):
        """Document showing info about a class.

        Arguments:
            klass: class to show info for
            module_path: If given, overrides module returned by class.__module__
            kwargs: keyword arguments passed to base class
        """
        super().__init__(**kwargs)
        self.klass = klass
        match module_path:
            case str():
                self.parts = module_path.split(".")
            case (str(), *_):
                self.parts = module_path
            case None:
                self.parts = klass.__module__.split(".")
            case _:
                raise TypeError(module_path)
        self._build()

    def _build(self):
        module_path = ".".join(self.parts)
        self.append(markdownizer.DocStrings(f"{module_path}.{self.klass.__name__}"))
        if table := markdownizer.Table.get_ancestor_table_for_klass(self.klass):
            self.append(table)
        self.append(markdownizer.MermaidDiagram.for_classes([self.klass]))
        # self.append(markdownizer.MermaidDiagram.for_subclasses([self.klass]))


class ModuleDocument(Document):
    """Document showing info about a module.

    Arguments:
        module: ModuleType or path to model to show info for.
        docstrings: Whether to show docstrings for given module.
        show_class_table: ModuleType or path to model to show info for.
    """

    def __init__(
        self,
        module: tuple[str, ...] | str | types.ModuleType,
        docstrings: bool = False,
        show_class_table: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        match module:
            case (str(), *_):
                self.parts = module
            case str():
                self.parts = module.split(".")
            case types.ModuleType():
                self.parts = module.__name__
            case _:
                raise TypeError(module)
        self.docstrings = docstrings
        self.show_class_table = show_class_table
        self._build()

    def _build(self):
        if self.docstrings:
            self.append(markdownizer.DocStrings(f'{".".join(self.parts)}'))
        if self.show_class_table:
            klasses = classhelpers.get_module_classes(self.parts)
            self.append(markdownizer.Table.get_classes_table(klasses))


if __name__ == "__main__":
    doc = ModuleDocument(collections)
    print(doc.to_markdown())

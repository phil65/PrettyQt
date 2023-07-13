from __future__ import annotations

from collections.abc import Callable
import importlib
import inspect
import logging
import os
import pathlib

import mkdocs_gen_files

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Nav(markdownizer.BaseSection):
    def __init__(
        self,
        section: str | os.PathLike,
        mapping: dict[str | tuple[str, ...], str] | None = None,
        indentation: int | str = "",
        module_name: str = "",
    ):
        super().__init__()
        self.section = section
        self.path = pathlib.Path(section) / "SUMMARY.md"
        self.nav = mkdocs_gen_files.Nav()
        self.module_name = module_name
        self._mapping = {}
        self.navs = []
        if mapping:
            for k, v in mapping.items():
                self.nav[k] = v
                self._mapping[k] = v

    def __setitem__(self, item: tuple | str, value: str | os.PathLike):
        if isinstance(item, str):
            item = tuple(item.split("."))
        self.nav[item] = pathlib.Path(value).as_posix()
        self._mapping[item] = value

    def __getitem__(self, item):
        return self._mapping[item]

    def write_navs(self):
        for nav in self.navs:
            nav.write()

    def write(self):
        self.write_navs()
        logger.info(f"Written SUMMARY to {self.path}")
        with mkdocs_gen_files.open(self.path, "w") as nav_file:
            nav_file.writelines(self.iter_rows())

    def iter_rows(self):
        return self.nav.build_literate_nav()

    def to_markdown(self):
        return "\n".join(self.iter_rows())

    def add_document(self, nav_path: str | tuple, file_path: os.PathLike | str, **kwargs):
        self.__setitem__(nav_path, file_path)
        return markdownizer.Document(**kwargs)

    def get_overview_document(self, predicate: Callable | None = None):
        page = markdownizer.Document(
            hide_toc=True, path=pathlib.Path(self.section, "index.md")
        )
        # page += self.get_dependency_table()
        page += self.get_module_overview(predicate=predicate)
        return page

    def get_module_overview(
        self, module: str | None = None, predicate: Callable | None = None
    ):
        mod = importlib.import_module(module or self.module_name)
        rows = [
            (
                submod_name,
                (
                    submod.__doc__.split("\n")[0]
                    if submod.__doc__
                    else "*No docstrings defined.*"
                ),
                (
                    markdownizer.to_html_list(submod.__all__, make_link=True)
                    if hasattr(submod, "__all__")
                    else ""
                ),
            )
            for submod_name, submod in inspect.getmembers(mod, inspect.ismodule)
            if (predicate is None or predicate(submod)) and "__" not in submod.__name__
        ]
        rows = list(zip(*rows))
        return markdownizer.Table(rows, columns=["Name", "Information", "Members"])

    def add_class_page(self, klass, path, **kwargs):
        parts = pathlib.Path(path).parts[:-1]
        page = markdownizer.PrettyQtClassDocument(
            klass=klass,
            module_path=f'{self.module_name}.{".".join(parts)}',
            path=pathlib.Path(self.section, path),
            **kwargs,
        )
        self[(*parts, klass.__name__)] = path.with_name(f"{klass.__name__}.md")
        return page

    def add_module_page(self, module, path, **kwargs):
        complete_mod_path = f"{self.module_name}.{module}"
        parts = pathlib.Path(path).parts[:-1]
        page = markdownizer.ModuleDocument(
            hide_toc=True,
            module=complete_mod_path,
            path=pathlib.Path(self.section, path),
            **kwargs,
        )
        self[parts] = path.with_name("index.md")
        return page


if __name__ == "__main__":
    nav = Nav(path="prettyqt")
    doc = nav.add_document(("a", "ab"), "Path/to/something")
    print(nav)

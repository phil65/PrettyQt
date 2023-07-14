from __future__ import annotations

from collections.abc import Callable
import logging
import os
import pathlib

import mkdocs_gen_files

from prettyqt.utils import get_repr, markdownizer


logger = logging.getLogger(__name__)


class Nav(markdownizer.BaseSection):
    def __init__(
        self,
        section: str | os.PathLike,
        module_name: str = "",
        filename: str = "SUMMARY.md",
    ):
        super().__init__()
        self.section = section
        self.filename = filename
        self.path = pathlib.Path(section) / self.filename
        self.nav = mkdocs_gen_files.Nav()
        self.module_name = module_name
        self.indentation = 0
        self._mapping = {}
        self.navs = []
        self.pages = []

    def __repr__(self):
        return get_repr(
            self,
            section=self.section,
            module_name=self.module_name,
            filename=self.filename,
        )

    def __setitem__(self, item: tuple | str, value: str | os.PathLike):
        if isinstance(item, str):
            item = tuple(item.split("."))
        self.nav[item] = pathlib.Path(value).as_posix()
        self._mapping[item] = value

    def __getitem__(self, item):
        return self._mapping[item]

    @property
    def children(self):
        return self.pages + self.navs

    @children.setter
    def children(self, items):
        self.navs = [i for i in items if isinstance(i, Nav)]
        self.pages = [i for i in items if not isinstance(i, Nav)]

    def create_nav(self, section: str | os.PathLike) -> markdownizer.Nav:
        nav = markdownizer.Nav(section=section, module_name=self.module_name)
        # self.nav[(section,)]
        self.navs.append(nav)
        return nav

    def write_navs(self):
        for nav in self.navs:
            nav.write()

    def virtual_files(self):
        return {self.path: self.to_markdown()}

    def to_markdown(self):
        return "".join(self.nav.build_literate_nav())

    def add_document(self, nav_path: str | tuple, file_path: os.PathLike | str, **kwargs):
        self.__setitem__(nav_path, file_path)
        page = markdownizer.Document(**kwargs)
        self.pages.append(page)
        return page

    def add_overview_page(self, predicate: Callable | None = None):
        page = markdownizer.Document(
            hide_toc=True, path=pathlib.Path(self.section, "index.md")
        )
        # page += self.get_dependency_table()
        page += markdownizer.Table.get_module_overview(
            self.module_name, predicate=predicate
        )
        return page

    def add_class_page(self, klass, path, **kwargs):
        path = pathlib.Path(path)
        parts = path.parts[:-1]
        page = markdownizer.PrettyQtClassDocument(
            klass=klass,
            module_path=f'{self.module_name}.{".".join(parts)}',
            path=pathlib.Path(self.section, path),
            **kwargs,
        )
        self[(*parts, klass.__name__)] = path.with_name(f"{klass.__name__}.md")
        self.pages.append(page)
        return page

    def add_module_page(self, module, path, **kwargs):
        path = pathlib.Path(path)
        complete_mod_path = f"{self.module_name}.{module}"
        parts = path.parts[:-1]
        page = markdownizer.ModuleDocument(
            hide_toc=True,
            module=complete_mod_path,
            path=pathlib.Path(self.section, path),
            **kwargs,
        )
        self[parts] = path.with_name("index.md")
        self.pages.append(page)
        return page

    def get_dependency_table(self) -> markdownizer.Table:
        return markdownizer.DependencyTable(self.module_name)

    def add_dependency_page(self, path: str | os.PathLike, **kwargs):
        path = pathlib.Path(path)
        page = markdownizer.Document(path=pathlib.Path(self.section, path), **kwargs)
        page += self.get_dependency_table()
        self.pages.append(page)
        parts = path.parts[:-1]
        self[parts] = path.with_name("dependencies.md")
        return page


if __name__ == "__main__":
    nav = Nav(section="prettyqt")
    doc = nav.add_document(("a", "ab"), "Path/to/something")
    print(nav)

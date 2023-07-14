from __future__ import annotations

from collections.abc import Callable
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

    def __setitem__(self, item: tuple | str, value: str | os.PathLike):
        if isinstance(item, str):
            item = tuple(item.split("."))
        self.nav[item] = pathlib.Path(value).as_posix()
        self._mapping[item] = value

    def __getitem__(self, item):
        return self._mapping[item]

    @property
    def children(self):
        return self.navs + self.pages

    # @children.setter
    # def children(self, pages):
    #     self.pages = pages

    def create_nav(self, section: str | os.PathLike) -> markdownizer.Nav:
        nav = markdownizer.Nav(section=section, module_name=self.module_name)
        # self.nav[(section,)]
        self.navs.append(nav)
        return nav

    def write_navs(self):
        for nav in self.navs:
            nav.write()

    def write(self):
        self.write_navs()
        logger.info(f"Written SUMMARY to {self.path}")
        with mkdocs_gen_files.open(self.path, "w") as nav_file:
            nav_file.writelines(self.iter_rows())

    def virtual_files(self):
        return {self.path: self.to_markdown()}

    def iter_rows(self):
        return self.nav.build_literate_nav()

    def to_markdown(self):
        return "\n".join(self.iter_rows())

    def add_document(self, nav_path: str | tuple, file_path: os.PathLike | str, **kwargs):
        self.__setitem__(nav_path, file_path)
        page = markdownizer.Document(**kwargs)
        self.pages[nav_path] = page
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
        parts = pathlib.Path(path).parts[:-1]
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
        complete_mod_path = f"{self.module_name}.{module}"
        parts = pathlib.Path(path).parts[:-1]
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
        page = markdownizer.Document(path=pathlib.Path(self.section, path), **kwargs)
        page += self.get_dependency_table()
        self.pages.append(page)
        parts = pathlib.Path(path).parts[:-1]
        self[parts] = path.with_name("dependencies.md")
        page.write()
        return page


if __name__ == "__main__":
    nav = Nav(path="prettyqt")
    doc = nav.add_document(("a", "ab"), "Path/to/something")
    print(nav)

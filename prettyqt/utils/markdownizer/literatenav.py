from __future__ import annotations

import logging
import os
import pathlib

import mkdocs_gen_files

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class Nav(markdownizer.BaseSection):
    def __init__(
        self,
        path: str | os.PathLike,
        mapping: dict[str | tuple[str, ...], str] | None = None,
        indentation: int | str = "",
    ):
        super().__init__()
        self.path = pathlib.Path(path) / "SUMMARY.md"
        self.nav = mkdocs_gen_files.Nav()
        self.module_name = "prettyqt"
        self._mapping = {}
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

    def write(self):
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

    def add_class_page(self, klass, path, **kwargs):
        parts = pathlib.Path(path).parts[:-1]
        page = markdownizer.PrettyQtClassDocument(
            klass=klass,
            module_path=f'{self.module_name}.{".".join(parts)}',
            path=path,
            **kwargs,
        )
        self[(*parts, klass.__name__)] = path.with_name(f"{klass.__name__}.md")
        return page

    def add_module_page(self, module, path, **kwargs):
        parts = pathlib.Path(path).parts[:-1]
        page = markdownizer.ModuleDocument(
            hide_toc=True,
            module=module,
            path=path,
            **kwargs,
        )
        self[parts] = path.with_name("index.md")
        return page


if __name__ == "__main__":
    nav = Nav(path="prettyqt")
    doc = nav.add_document(("a", "ab"), "Path/to/something")
    print(nav)

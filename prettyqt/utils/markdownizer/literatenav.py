from __future__ import annotations

import logging
import os
import pathlib

import mkdocs_gen_files

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class LiterateNav(markdownizer.BaseSection):
    def __init__(
        self,
        path: str | os.PathLike,
        mapping: dict[str | tuple[str, ...], str] | None = None,
        indentation: int | str = "",
    ):
        super().__init__()
        self.path = pathlib.Path(path) / "SUMMARY.md"
        self.nav = mkdocs_gen_files.Nav()
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


if __name__ == "__main__":
    nav = LiterateNav(path="prettyqt")
    doc = nav.add_document(("a", "ab"), "Path/to/something")
    print(nav)

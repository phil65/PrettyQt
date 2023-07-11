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
        self._mapping = dict()
        if mapping:
            for k, v in mapping.items():
                self.nav[k] = v
                self._mapping[k] = v

    def __setitem__(self, item, value):
        self.nav[item] = value
        self._mapping[item] = value

    def __getitem__(self, item):
        return self._mapping[item]

    def write(self):
        logger.info(f"Written SUMMARY to {self.path}")
        with mkdocs_gen_files.open(self.path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())


if __name__ == "__main__":
    doc = LiterateNav(module_name="prettyqt")
    print(list(doc.yield_files()))

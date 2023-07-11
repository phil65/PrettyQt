from __future__ import annotations

import collections
import logging
import os

import mkdocs_gen_files

from prettyqt.utils import markdownizer


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

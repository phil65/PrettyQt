from __future__ import annotations

import logging

import mkdocs_gen_files

from prettyqt.utils import markdownizer


logger = logging.getLogger(__name__)


class LiterateNav(markdownizer.BaseSection):
    def __init__(
        self,
        mapping: dict[str | tuple[str, ...], str] | None = None,
        indentation: int | str = "",
    ):
        super().__init__()
        self.nav = mkdocs_gen_files.Nav()
        if mapping:
            for k, v in mapping.items():
                self.nav[k] = v

    def write(self, path: str = "SUMMARY.md"):
        logger.info(f"Written SUMMARY to {path}")
        with mkdocs_gen_files.open(path, "w") as nav_file:
            nav_file.writelines(self.nav.build_literate_nav())


if __name__ == "__main__":
    doc = LiterateNav(module_name="prettyqt")
    print(list(doc.yield_files()))

from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING

from prettyqt import gui, widgets


if TYPE_CHECKING:
    from collections.abc import Iterable

    from prettyqt.utils import datatypes


class TextBrowser(widgets.TextEditMixin, widgets.QTextBrowser):
    """Rich text browser with hypertext navigation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenExternalLinks(True)

    # def dragEnterEvent(self, event):
    #     u = event.mimeData().urls()
    #     for url in u:
    #         file_path = os.path.abspath(url.toLocalFile())

    #         ext = file_path.split(".")[-1]
    #         if ext in ["txt", "md", "markdown"]:
    #             event.accept()
    #         else:
    #             event.ignore()

    # def dropEvent(self, event):
    #     event.accept()
    #     self.show_markdown_file(self.filePath)

    def set_markdown_file(self, file_path: datatypes.PathType):
        file_path = pathlib.Path(file_path)
        with file_path.open() as f:
            file_content = f.read()
        self.setMarkdown(file_content)

    def set_markdown(self, text: str):
        self.setMarkdown(text)

    def get_search_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.searchPaths()]

    def set_search_paths(self, paths: Iterable[datatypes.PathType]):
        self.setSearchPaths([os.fspath(p) for p in paths])

    def get_source_type(self) -> gui.textdocument.ResourceTypeStr:
        return gui.textdocument.RESOURCE_TYPES.inverse[self.sourceType()]


if __name__ == "__main__":
    app = widgets.app()
    reader = TextBrowser()
    reader.show()
    app.exec()

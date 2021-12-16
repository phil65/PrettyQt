from __future__ import annotations

import os
import pathlib

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


QtWidgets.QTextBrowser.__bases__ = (widgets.TextEdit,)


class TextBrowser(QtWidgets.QTextBrowser):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenExternalLinks(True)

    def serialize_fields(self):
        return dict(
            open_external_links=self.openExternalLinks(),
            open_links=self.openLinks(),
            search_paths=self.get_search_paths(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setOpenExternalLinks(state["open_external_links"])
        self.setOpenLinks(state["open_links"])
        self.set_search_paths(state["search_paths"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

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

    def set_markdown_file(self, file_path: types.PathType):
        file_path = pathlib.Path(file_path)
        with file_path.open() as f:
            file_content = f.read()
        self.set_markdown(file_content)

    def set_markdown(self, source: str):
        self.setMarkdown(source)

    def set_rst_file(self, file_path: types.PathType):
        file_path = pathlib.Path(file_path)
        with file_path.open() as f:
            file_content = f.read()
        self.set_rst(file_content)

    def set_rst(self, source: str):
        import docutils.core

        html = docutils.core.publish_string(source, writer_name="html")
        self.setHtml(str(html))

    def get_search_paths(self) -> list[pathlib.Path]:
        return [pathlib.Path(p) for p in self.searchPaths()]

    def set_search_paths(self, paths: list[types.PathType]):
        self.setSearchPaths([os.fspath(p) for p in paths])


if __name__ == "__main__":
    app = widgets.app()
    reader = TextBrowser()
    reader.show()
    app.main_loop()

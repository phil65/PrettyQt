# -*- coding: utf-8 -*-
"""
"""

from typing import Union
import pathlib

try:
    from PyQt5 import QtWinExtras  # type: ignore
except ImportError:
    from PySide2 import QtWinExtras

from prettyqt import gui
from prettyqt.utils import bidict


TYPES = bidict(
    destination=QtWinExtras.QWinJumpListItem.Destination,
    link=QtWinExtras.QWinJumpListItem.Link,
    separator=QtWinExtras.QWinJumpListItem.Separator,
)


class WinJumpListItem(QtWinExtras.QWinJumpListItem):
    def __init__(self, typ: str) -> None:
        if typ in TYPES:
            typ = TYPES[typ]
        super().__init__(typ)

    def set_title(self, title: str) -> None:
        self.setTitle(title)

    def set_icon(self, icon: gui.icon.IconType) -> None:
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def set_file_path(self, path: Union[str, pathlib.Path]) -> None:
        self.setFilePath(str(path))

    def get_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.filePath())

    def set_working_directory(self, path: Union[str, pathlib.Path]) -> None:
        self.setWorkingDirectory(str(path))

    def get_working_directory(self) -> pathlib.Path:
        return pathlib.Path(self.workingDirectory())

    def set_type(self, typ: str) -> None:
        self.setType(TYPES[typ])

    def get_type(self) -> str:
        return TYPES.inv[self.type()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    pass
    app.exec_()

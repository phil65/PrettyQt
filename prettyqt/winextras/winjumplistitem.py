from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import iconprovider
from prettyqt.qt import QtWinExtras
from prettyqt.utils import bidict, types


TYPES = bidict(
    destination=QtWinExtras.QWinJumpListItem.Destination,
    link=QtWinExtras.QWinJumpListItem.Link,
    separator=QtWinExtras.QWinJumpListItem.Separator,
)

TypeStr = Literal["destination", "link", "separator"]


class WinJumpListItem(QtWinExtras.QWinJumpListItem):
    def __init__(self, typ: QtWinExtras.QWinJumpListItem.Type | TypeStr) -> None:
        if isinstance(typ, QtWinExtras.QWinJumpListItem.Type):
            param = typ
        else:
            param = TYPES[typ]
        super().__init__(param)

    def set_title(self, title: str) -> None:
        self.setTitle(title)

    def set_icon(self, icon: types.IconType) -> None:
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_file_path(self, path: types.PathType) -> None:
        self.setFilePath(os.fspath(path))

    def get_file_path(self) -> pathlib.Path:
        return pathlib.Path(self.filePath())

    def set_working_directory(self, path: types.PathType) -> None:
        self.setWorkingDirectory(os.fspath(path))

    def get_working_directory(self) -> pathlib.Path:
        return pathlib.Path(self.workingDirectory())

    def set_type(self, typ: TypeStr) -> None:
        self.setType(TYPES[typ])

    def get_type(self) -> TypeStr:
        return TYPES.inverse[self.type()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    pass
    app.main_loop()

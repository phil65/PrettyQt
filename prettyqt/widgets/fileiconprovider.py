from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict, types


mod = QtWidgets.QFileIconProvider

ICON_TYPE = bidict(
    computer=mod.IconType.Computer,
    desktop=mod.IconType.Desktop,
    trashcan=mod.IconType.Trashcan,
    network=mod.IconType.Network,
    drive=mod.IconType.Drive,
    folder=mod.IconType.Folder,
    file=mod.IconType.File,
)

IconTypeStr = Literal[
    "computer", "desktop", "trashcan", "network", "drive", "folder", "file"
]

OPTIONS = bidict(
    dont_use_custom_dir_icons=mod.Option.DontUseCustomDirectoryIcons,
)

OptionStr = Literal["dont_use_custom_dir_icons"]


class FileIconProvider(QtWidgets.QFileIconProvider):
    def get_icon(self, typ: IconTypeStr | QtCore.QFileInfo | types.PathType) -> gui.Icon:
        if isinstance(typ, (os.PathLike, QtCore.QFileInfo)):
            param = core.FileInfo(typ)
        else:
            param = ICON_TYPE[typ]
        return gui.Icon(self.icon(param))


if __name__ == "__main__":
    import pathlib

    from prettyqt import widgets

    app = widgets.app()
    path = pathlib.Path.home()
    provider = FileIconProvider()
    provider.get_icon(path)

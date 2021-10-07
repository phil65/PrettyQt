from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict


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
    def get_icon(self, typ: IconTypeStr | QtCore.QFileInfo) -> gui.Icon:
        if not isinstance(typ, QtCore.QFileInfo):
            param = ICON_TYPE[typ]
        else:
            param = typ
        return gui.Icon(self.icon(param))

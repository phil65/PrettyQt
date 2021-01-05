from __future__ import annotations

from typing import Literal, Union

from prettyqt import gui
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict


ICON_TYPE = bidict(
    computer=QtWidgets.QFileIconProvider.Computer,
    desktop=QtWidgets.QFileIconProvider.Desktop,
    trashcan=QtWidgets.QFileIconProvider.Trashcan,
    network=QtWidgets.QFileIconProvider.Network,
    drive=QtWidgets.QFileIconProvider.Drive,
    folder=QtWidgets.QFileIconProvider.Folder,
    file=QtWidgets.QFileIconProvider.File,
)

IconTypeStr = Literal[
    "computer", "desktop", "trashcan", "network", "drive", "folder", "file"
]

OPTIONS = bidict(
    dont_use_custom_dir_icons=QtWidgets.QFileIconProvider.DontUseCustomDirectoryIcons,
)

OptionStr = Literal["dont_use_custom_dir_icons"]


class FileIconProvider(QtWidgets.QFileIconProvider):
    def get_icon(self, typ: Union[IconTypeStr, QtCore.QFileInfo]) -> gui.Icon:
        if not isinstance(typ, QtCore.QFileInfo):
            param = ICON_TYPE[typ]
        else:
            param = typ
        return gui.Icon(self.icon(param))

from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import bidict, datatypes


mod = QtGui.QAbstractFileIconProvider

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


class AbstractFileIconProviderMixin:
    def get_type(self, file: QtCore.QFileInfo | datatypes.PathType) -> str:
        if isinstance(file, os.PathLike):
            file = core.FileInfo(file)
        return self.type(file)


class AbstractFileIconProvider(
    AbstractFileIconProviderMixin, QtGui.QAbstractFileIconProvider
):
    pass

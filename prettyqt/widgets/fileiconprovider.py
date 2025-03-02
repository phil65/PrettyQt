from __future__ import annotations

import os
from typing import TYPE_CHECKING

from prettyqt import core, gui
from prettyqt.qt import QtWidgets


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class FileIconProvider(gui.AbstractFileIconProviderMixin, QtWidgets.QFileIconProvider):
    """File icons for the QFileSystemModel class."""

    def get_icon(
        self,
        typ: gui.abstractfileiconprovider.IconTypeStr
        | core.QFileInfo
        | datatypes.PathType,
    ) -> gui.QIcon:
        if isinstance(typ, os.PathLike | core.QFileInfo):
            param = core.FileInfo(typ)
        else:
            param = gui.abstractfileiconprovider.ICON_TYPE[typ]
        return self.icon(param)

    def use_custom_directory_icons(self, state: bool = True):
        opt = self.Option(0) if state else self.Option.DontUseCustomDirectoryIcons
        self.setOptions(opt)

    def uses_custom_directory_icons(self) -> bool:
        return self.options() == self.Option(0)


if __name__ == "__main__":
    import pathlib

    from prettyqt import widgets

    app = widgets.app()
    path = pathlib.Path.home()
    provider = FileIconProvider()
    provider.get_icon(path)

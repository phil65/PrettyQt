from __future__ import annotations

import os

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import types


class FileIconProvider(gui.AbstractFileIconProviderMixin, QtWidgets.QFileIconProvider):
    def get_icon(
        self,
        typ: gui.abstractfileiconprovider.IconTypeStr | QtCore.QFileInfo | types.PathType,
    ) -> QtGui.QIcon:
        if isinstance(typ, (os.PathLike, QtCore.QFileInfo)):
            param = core.FileInfo(typ)
        else:
            param = gui.abstractfileiconprovider.ICON_TYPE[typ]
        return self.icon(param)


if __name__ == "__main__":
    import pathlib

    from prettyqt import widgets

    app = widgets.app()
    path = pathlib.Path.home()
    provider = FileIconProvider()
    provider.get_icon(path)

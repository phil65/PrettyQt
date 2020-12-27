import pathlib
from typing import Union

from prettyqt import core
from prettyqt.qt import QtCore, QtGui


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: Union[str, pathlib.Path, QtCore.QUrl]) -> bool:
        return cls.openUrl(core.Url.from_user_input(str(location)))

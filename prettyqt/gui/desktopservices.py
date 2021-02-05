from __future__ import annotations

import os

from prettyqt import core
from prettyqt.qt import QtCore, QtGui


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: str | os.PathLike | QtCore.QUrl) -> bool:
        if not isinstance(location, QtCore.QUrl):
            location = core.Url.from_user_input(os.fspath(location))
        return cls.openUrl(location)

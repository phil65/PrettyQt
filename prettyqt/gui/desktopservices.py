from __future__ import annotations

import os

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import types


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: types.PathType | types.UrlType) -> bool:
        if not isinstance(location, QtCore.QUrl):
            location = core.Url.from_user_input(os.fspath(location))
        return cls.openUrl(location)

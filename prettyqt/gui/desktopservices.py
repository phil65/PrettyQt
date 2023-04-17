from __future__ import annotations

import os

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import datatypes


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: datatypes.PathType | datatypes.UrlType) -> bool:
        if not isinstance(location, QtCore.QUrl):
            location = core.Url.from_user_input(os.fspath(location))
        return cls.openUrl(location)

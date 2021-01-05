from __future__ import annotations

import os
from typing import Union

from prettyqt import core
from prettyqt.qt import QtCore, QtGui


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: Union[str, os.PathLike, QtCore.QUrl]) -> bool:
        if not isinstance(location, QtCore.QUrl):
            location = core.Url.from_user_input(os.fspath(location))
        return cls.openUrl(location)

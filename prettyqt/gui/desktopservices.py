# -*- coding: utf-8 -*-

from typing import Union
import pathlib

from qtpy import QtGui, QtCore

from prettyqt import core


class DesktopServices(QtGui.QDesktopServices):
    @classmethod
    def open_url(cls, location: Union[str, pathlib.Path, QtCore.QUrl]) -> bool:
        return cls.openUrl(core.Url.from_user_input(str(location)))

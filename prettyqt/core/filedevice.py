# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


QtCore.QFileDevice.__bases__ = (core.IODevice,)


class FileDevice(QtCore.QFileDevice):
    pass

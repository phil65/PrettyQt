# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


QtCore.QFile.__bases__ = (core.FileDevice,)


class File(QtCore.QFile):
    def __repr__(self):
        return f"File('{self.fileName()}')"

    def __str__(self):
        return self.fileName()

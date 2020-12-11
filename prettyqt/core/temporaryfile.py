from qtpy import QtCore

from prettyqt import core


QtCore.QTemporaryFile.__bases__ = (core.File,)


class TemporaryFile(QtCore.QTemporaryFile):
    pass

from qtpy import QtCore

from prettyqt import core


QtCore.QFile.__bases__ = (core.FileDevice,)


class File(QtCore.QFile):
    pass

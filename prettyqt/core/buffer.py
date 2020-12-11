from qtpy import QtCore

from prettyqt import core


QtCore.QBuffer.__bases__ = (core.IODevice,)


class Buffer(QtCore.QBuffer):
    pass

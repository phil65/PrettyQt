from qtpy import QtCore

from prettyqt import core


QtCore.QSaveFile.__bases__ = (core.FileDevice,)


class SaveFile(QtCore.QSaveFile):
    pass

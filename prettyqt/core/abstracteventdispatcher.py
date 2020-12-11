from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractEventDispatcher.__bases__ = (core.Object,)


class AbstractEventDispatcher(QtCore.QAbstractEventDispatcher):
    pass

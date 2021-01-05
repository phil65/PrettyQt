from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QAbstractListModel.__bases__ = (core.AbstractItemModel,)


class AbstractListModel(QtCore.QAbstractListModel):
    pass

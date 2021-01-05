from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QAbstractTableModel.__bases__ = (core.AbstractItemModel,)


class AbstractTableModel(QtCore.QAbstractTableModel):
    pass

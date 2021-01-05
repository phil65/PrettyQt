from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


QtWidgets.QAbstractItemDelegate.__bases__ = (core.Object,)


class AbstractItemDelegate(QtWidgets.QAbstractItemDelegate):
    pass

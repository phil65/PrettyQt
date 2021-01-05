from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QItemDelegate.__bases__ = (widgets.AbstractItemDelegate,)


class ItemDelegate(QtWidgets.QItemDelegate):
    pass

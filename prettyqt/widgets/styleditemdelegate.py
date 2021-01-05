from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyledItemDelegate.__bases__ = (widgets.AbstractItemDelegate,)


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    pass

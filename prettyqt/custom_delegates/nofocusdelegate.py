from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


# Remove dotted border on cell focus.  https://stackoverflow.com/a/55252650/3620725
class NoFocusDelegate(widgets.StyledItemDelegate):
    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        if option.state & widgets.Style.StateFlag.State_HasFocus:
            option.state = option.state ^ widgets.Style.StateFlag.State_HasFocus
        super().paint(painter, option, index)

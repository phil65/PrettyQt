from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


DecorationRole2 = QtCore.Qt.UserRole + 1000


class IconDelegate(widgets.StyledItemDelegate):
    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Override to paint an icon based on given Pixmap / Color / Icon.

        Pixmap / Color / Icon must be set to 'QtCore.Qt.UserRole + 1000'

        Args:
            painter (QtGui.QPainter): painter to paint the icon
            option (QtWidgets.QStyleOptionViewItem): state of the item to be displayed
            index (QtCore.QModelIndex): index which gets decorated
        """
        super().paint(painter, option, index)
        value = index.data(DecorationRole2)
        if not value:
            return
        margin = 10
        mode = gui.Icon.Normal

        if not (option.state & widgets.Style.State_Enabled):
            mode = gui.Icon.Disabled
        elif option.state & widgets.Style.State_Selected:
            mode = gui.Icon.Selected

        if isinstance(value, QtGui.QPixmap):
            icon = QtGui.QIcon(value)
            option.decorationSize = value.size() / value.devicePixelRatio()

        elif isinstance(value, QtGui.QColor):
            pixmap = QtGui.QPixmap(option.decorationSize)
            pixmap.fill(value)
            icon = QtGui.QIcon(pixmap)

        elif isinstance(value, QtGui.QImage):
            icon = QtGui.QIcon(QtGui.QPixmap.fromImage(value))
            option.decorationSize = value.size() / value.devicePixelRatio()

        elif isinstance(value, QtGui.QIcon):
            is_on = option.state & widgets.Style.State_Open
            state = gui.Icon.On if is_on else gui.Icon.Off
            actual_size = option.icon.actualSize(option.decorationSize, mode, state)
            option.decorationSize = option.decorationSize & actual_size
        r = core.Rect(core.Point(), option.decorationSize)
        r.moveCenter(option.rect.center())
        r.setRight(option.rect.right() - margin)
        state = gui.Icon.On if option.state & widgets.Style.State_Open else gui.Icon.Off
        alignment = constants.ALIGN_RIGHT | constants.ALIGN_V_CENTER
        icon.paint(painter, r, alignment, mode, state)

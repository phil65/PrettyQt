from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import constants, core, gui, widgets


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
        if value:
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
                state = (
                    gui.Icon.On
                    if option.state & widgets.Style.State_Open
                    else gui.Icon.Off
                )
                actualSize = option.icon.actualSize(option.decorationSize, mode, state)
                option.decorationSize = core.Size(
                    min(option.decorationSize.width(), actualSize.width()),
                    min(option.decorationSize.height(), actualSize.height()),
                )

            r = core.Rect(core.Point(), option.decorationSize)
            r.moveCenter(option.rect.center())
            r.setRight(option.rect.right() - margin)
            state = (
                gui.Icon.On if option.state & widgets.Style.State_Open else gui.Icon.Off
            )
            icon.paint(
                painter, r, constants.ALIGN_RIGHT | constants.ALIGN_V_CENTER, mode, state
            )

from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


class IconDelegate(widgets.StyledItemDelegate):
    ID = "icon"

    def __init__(self, role: constants.ItemDataRole = constants.USER_ROLE, **kwargs):
        self._role = role
        self.margin = 10
        super().__init__(**kwargs)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        """Override to paint an icon based on given Pixmap / Color / Icon.

        Pixmap / Color / Icon must be set to '_role'

        Args:
            painter (QtGui.QPainter): painter to paint the icon
            option (QtWidgets.QStyleOptionViewItem): state of the item to be displayed
            index (QtCore.QModelIndex): index which gets decorated
        """
        super().paint(painter, option, index)
        value = index.data(self._role)
        if not value:
            return
        mode = gui.Icon.Mode.Normal

        if not option.state & widgets.Style.StateFlag.State_Enabled:
            mode = gui.Icon.Mode.Disabled
        elif option.state & widgets.Style.StateFlag.State_Selected:
            mode = gui.Icon.Mode.Selected
        match value:
            case QtGui.QPixmap():
                icon = QtGui.QIcon(value)
                option.decorationSize = int(value.size() / value.devicePixelRatio())

            case QtGui.QColor():
                pixmap = QtGui.QPixmap(option.decorationSize)
                pixmap.fill(value)
                icon = QtGui.QIcon(pixmap)

            case QtGui.QImage():
                icon = QtGui.QIcon(QtGui.QPixmap.fromImage(value))
                option.decorationSize = int(value.size() / value.devicePixelRatio())

            case QtGui.QIcon():
                icon = value
                is_on = option.state & widgets.Style.StateFlag.State_Open
                state = gui.Icon.State.On if is_on else gui.Icon.State.Off
                actual_size = option.icon.actualSize(option.decorationSize, mode, state)
                option.decorationSize.boundedTo(actual_size)
            case _:
                raise ValueError(value)
        r = core.Rect(core.Point(), option.decorationSize)
        r.moveCenter(option.rect.center())
        r.setRight(option.rect.right() - self.margin)
        state = (
            gui.Icon.State.On
            if option.state & widgets.Style.StateFlag.State_Open
            else gui.Icon.State.Off
        )
        alignment = constants.ALIGN_RIGHT | constants.ALIGN_V_CENTER
        icon.paint(painter, r, alignment, mode, state)


if __name__ == "__main__":
    from prettyqt import iconprovider

    app = widgets.app()
    model = gui.StandardItemModel()
    model.add("test")
    app = widgets.app()
    w = widgets.ListView()
    w.set_delegate(IconDelegate())
    w.set_model(model)
    item = gui.StandardItem("Item")
    item.set_data(iconprovider.get_icon("mdi.folder"), "user")
    model += item
    w.show()
    app.exec()

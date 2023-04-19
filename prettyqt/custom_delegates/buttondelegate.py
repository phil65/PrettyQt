from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets


class ButtonDelegate(widgets.StyledItemDelegate):
    def __init__(
        self,
        parent: QtWidgets.QAbstractItemView,
        role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
    ):
        super().__init__(parent)
        parent.setMouseTracking(True)
        self.btn = widgets.PushButton(parent=parent)
        self.method_role = role
        self.btn.hide()
        self.is_one_cell_edit_mode = False
        self.current_edited_index = QtCore.QModelIndex()
        parent.entered.connect(self.cellEntered)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def createEditor(self, parent, option, index):
        if index.data(self.method_role) is None:
            return
        btn = widgets.PushButton(parent)
        btn.setText(index.data())
        btn_callback = index.data(self.method_role)
        if not btn_callback:
            btn.set_disabled()
        else:
            btn.clicked.connect(btn_callback)
        return btn

    def setEditorData(self, editor, index):
        pass
        # editor.setProperty("test", "aa")
        # editor.setText(index.data())

    def setModelData(self, editor, model, index):
        pass
        # model.setData(index, editor.property("test"))

    def cellEntered(self, index):
        self.parent().closePersistentEditor(self.current_edited_index)
        self.parent().openPersistentEditor(index)
        self.is_one_cell_edit_mode = True
        self.current_edited_index = index

    def paint(self, painter, option, index):
        if index.data(self.method_role) is None:
            super().paint(painter, option, index)
            return
        self.btn.setGeometry(option.rect)
        self.btn.setText(index.data())
        if option.state & widgets.Style.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, option.palette.highlight())
        if option.state & widgets.Style.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        pixmap = self.btn.grab()
        painter.drawPixmap(option.rect, pixmap)
        # return super().paint(painter, option, index)

    # mouseOver = option.state in [73985, 73729, 8192]
    # if option.state & widgets.Style.StateFlag.State_MouseOver:
    #     painter.fillRect(option.rect, gui.Brush(gui.Color("yellow")))

    # def editorEvent(self, event, model, option, index):
    #     if event.type() == QtCore.QEvent.Type.MouseButtonRelease:
    #         logger.info("Clicked on Item", index.row())
    #         return True
    #     elif event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
    #         logger.info("Double-Clicked on Item", index.row())
    #         return True
    #     else:
    #         return super().editorEvent(event, model, option, index)

    # @core.Slot()
    # def currentIndexChanged(self):
    #     self.commitData.emit(self.sender())

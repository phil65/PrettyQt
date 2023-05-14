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
        parent.entered.connect(self.cell_entered)

    #     parent.viewport().installEventFilter(self)

    # def eventFilter(self, source, event) -> bool:
    #     if event.type() == event.Type.MouseMove:
    #         return True
    #     return super().eventFilter(source, event)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def createEditor(self, parent, option, index):
        btn_callback = index.data(self.method_role)
        if btn_callback is None:
            return
        btn = widgets.PushButton(parent=parent)
        btn.setText(index.data())
        btn.clicked.connect(btn_callback)
        return btn

    def setEditorData(self, editor, index):
        pass
        # editor.setProperty("test", "aa")
        # editor.setText(index.data())

    def setModelData(self, editor, model, index):
        pass
        # model.setData(index, editor.property("test"))

    def cell_entered(self, index):
        # index = self.parent().indexFromItem(item)
        if self.parent().isPersistentEditorOpen(index):
            self.parent().closePersistentEditor(self.current_edited_index)
        if self.parent().itemDelegateForIndex(index) is self:
            # if index.data(self.method_role) is not None:
            self.parent().openPersistentEditor(index)
            self.parent().setCurrentIndex(index)
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


if __name__ == "__main__":
    app = widgets.app()
    table_widget = widgets.TableWidget(15, 4)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(
        table_widget.EditTrigger.DoubleClicked  # type: ignore
        | table_widget.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behavior("rows")
    # table_widget.set_selection_mode(None)
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    for i in range(10):
        item_1 = widgets.TableWidgetItem(str(i))
        item_2 = widgets.TableWidgetItem()
        item_2.setData(constants.DISPLAY_ROLE, str(i))
        item_2.setData(constants.USER_ROLE, lambda: print("test"))
        table_widget[i, 0] = item_1
        table_widget[i, 1] = item_2

    delegate = ButtonDelegate(parent=table_widget)
    table_widget.set_delegate(delegate, column=1)

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()

from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class ButtonDelegate(widgets.StyledItemDelegate):
    """Delegate to show a button inside a table cell."""

    ID = "button"

    def __init__(
        self,
        parent: widgets.QAbstractItemView,
        role: constants.ItemDataRole = constants.USER_ROLE,
    ):
        super().__init__(parent)
        parent.setMouseTracking(True)
        self.btn = widgets.PushButton(parent=parent)
        self.method_role = role
        self.btn.hide()
        self.current_edited_index = core.ModelIndex()
        parent.entered.connect(self.cell_entered)

    #     parent.viewport().installEventFilter(self)

    # def eventFilter(self, source, event) -> bool:
    #     if event.type() == event.Type.MouseMove:
    #         return True
    #     return super().eventFilter(source, event)

    def updateEditorGeometry(
        self,
        editor: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        editor.setGeometry(option.rect)

    def createEditor(
        self,
        parent: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        btn_callback = index.data(self.method_role)
        if btn_callback is None:
            return None
        return widgets.PushButton(parent=parent, text=index.data(), clicked=btn_callback)

    def setEditorData(self, editor: widgets.QWidget, index: core.ModelIndex):
        pass
        # editor.setProperty("test", "aa")
        # editor.setText(index.data())

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        pass
        # model.setData(index, editor.property("test"))

    def cell_entered(self, index: core.ModelIndex):
        # index = self.parent().indexFromItem(item)
        parent: widgets.QAbstractItemView = self.parent()  # type: ignore
        if parent.isPersistentEditorOpen(index):
            parent.closePersistentEditor(self.current_edited_index)
        if parent.itemDelegateForIndex(index) is self:
            # if index.data(self.method_role) is not None:
            parent.openPersistentEditor(index)
            parent.setCurrentIndex(index)
        self.current_edited_index = index

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
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
    #     if event.type() == core.QEvent.Type.MouseButtonRelease:
    #         logger.info("Clicked on Item", index.row())
    #         return True
    #     elif event.type() == core.QEvent.Type.MouseButtonDblClick:
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

    table_widget.set_delegate("button", column=1)

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.exec()

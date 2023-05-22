from __future__ import annotations


from prettyqt import constants, widgets
from prettyqt.qt import QtCore, QtWidgets


class WidgetDelegate(widgets.StyledItemDelegate):
    def __init__(
        self,
        data_role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        parent: QtWidgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self.data_role = data_role
        self.editors = {}

    def paint(self, painter, option, index):
        value = index.data(self.data_role)
        if not isinstance(value, QtWidgets.QWidget):
            super().paint(painter, option, index)
            return
        value = self.editor_for_index(index)
        value.setGeometry(option.rect)
        if option.state & widgets.Style.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, option.palette.highlight())
        if option.state & widgets.Style.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        pixmap = value.grab()
        painter.drawPixmap(option.rect, pixmap)
        # super().paint(painter, option, index)

    def editor_for_index(self, index):
        key = str((index.row(), index.column()))
        editor = index.data(self.data_role)
        while (index := index.parent()).isValid():
            key += str((index.row(), index.column()))
        if key not in self.editors:
            self.editors[key] = editor
            return editor
        else:
            return self.editors[key]

    def createEditor(self, parent, option, index):
        editor = index.data(self.data_role)
        if isinstance(editor, QtWidgets.QWidget):
            editor = self.editor_for_index(index).copy()
            editor.setParent(parent)
            editor.setAutoFillBackground(True)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        orig = self.editor_for_index(index)
        prop = orig.get_metaobject().get_user_property()
        value = prop.read(editor)
        prop.write(orig, value)

    def sizeHint(self, option, index):
        editor = self.editor_for_index(index)
        if editor:
            return editor.sizeHint()
        else:
            return super().sizeHint(option, index)

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        pass


if __name__ == "__main__":
    app = widgets.app()
    table_widget = widgets.TableWidget(2, 2)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(table_widget.EditTrigger.AllEditTriggers)
    table_widget.set_selection_behavior("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    types = dict(
        color=widgets.PlainTextEdit(),
        time=widgets.DateEdit(),
    )
    for i, (k, v) in enumerate(types.items()):
        item_1 = widgets.TableWidgetItem(k)
        item_2 = widgets.TableWidgetItem()
        item_2.setData(constants.DISPLAY_ROLE, v)
        item_2.setData(constants.USER_ROLE, v)
        table_widget[i, 0] = item_1
        table_widget[i, 1] = item_2

    delegate = WidgetDelegate(parent=table_widget)
    table_widget.set_delegate(delegate, column=1)

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()
    with app.debug_mode():
        app.main_loop()

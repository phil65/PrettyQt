from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


class WidgetDelegate(widgets.StyledItemDelegate):
    def __init__(
        self,
        role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        parent: QtWidgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self._widget_role = role
        # self._editors = {}

    def paint(self, painter, option, index):
        value = self._editor_for_index(index)
        if not isinstance(value, QtWidgets.QWidget):
            super().paint(painter, option, index)
            return
        value.setGeometry(option.rect)
        if option.state & widgets.Style.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, option.palette.highlight())
        if option.state & widgets.Style.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        pixmap = value.grab()
        painter.drawPixmap(option.rect, pixmap)
        # super().paint(painter, option, index)

    def _editor_for_index(self, index):
        # using index.data() does not work with PyQt6, it casts widgets to QObjects
        model = index.model()
        editor = model.data(index, self._widget_role)
        return editor
        # key = str((index.row(), index.column()))
        # while (index := index.parent()).isValid():
        #     key += str((index.row(), index.column()))
        # if key not in self._editors:
        #     self._editors[key] = editor
        #     return editor
        # else:
        #     return self._editors[key]

    def createEditor(self, parent, option, index):
        editor = self._editor_for_index(index)
        if isinstance(editor, QtWidgets.QWidget):
            editor = editor.copy()
            editor.setParent(parent)
            editor.setAutoFillBackground(True)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        orig = self._editor_for_index(index)
        if isinstance(orig, QtWidgets.QWidget):
            prop = core.MetaObject(orig.metaObject()).get_user_property()
            value = prop.read(editor)
            prop.write(orig, value)

    def sizeHint(self, option, index):
        editor = self._editor_for_index(index)
        if isinstance(editor, QtWidgets.QWidget):
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

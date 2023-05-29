from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets


class WidgetDelegate(widgets.StyledItemDelegate):
    ID = "widget"

    def __init__(
        self,
        role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        parent: QtWidgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self._widget_role = role
        self._editors = {}
        self._cache_editors = True

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
        if not self._cache_editors:
            return editor
        # two reasons for caching:  1) possibly performance. 2) keeping a reference
        # perhaps it would be nicer to just cache the currently chosen editor, not sure.
        key = str((index.row(), index.column()))
        while (index := index.parent()).isValid():
            key += str((index.row(), index.column()))
        if key not in self._editors:
            self._editors[key] = editor
            return editor
        else:
            return self._editors[key]

    def createEditor(self, parent, option, index):
        editor = self._editor_for_index(index)
        if isinstance(editor, QtWidgets.QWidget):
            metaobj = core.MetaObject(editor.metaObject())
            editor = metaobj.copy(editor)
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
    import logging

    app = widgets.app()
    table_widget = widgets.TableView()
    pb = widgets.PushButton("test", clicked=lambda: logging.info("x"))

    class Model(core.AbstractTableModel):
        def rowCount(self, index=None):
            return 5

        def columnCount(self, index=None):
            return 5

        def data(self, index, role=None):
            match role, index.column():
                case constants.DISPLAY_ROLE | constants.USER_ROLE, 0:
                    # return pb
                    return widgets.PushButton("test", clicked=lambda: logging.info("x"))

                case constants.DISPLAY_ROLE | constants.USER_ROLE, 1:
                    return pb

        def flags(self, index):
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )

    table_widget.set_delegate("widget")
    model = Model()
    table_widget.set_model(model)
    table_widget.set_edit_triggers("all")
    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()
    with app.debug_mode():
        app.main_loop()

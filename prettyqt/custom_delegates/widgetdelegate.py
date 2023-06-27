from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class WidgetDelegate(widgets.StyledItemDelegate):
    ID = "widget"

    def __init__(
        self,
        role: constants.ItemDataRole = constants.USER_ROLE,
        parent: widgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self._widget_role = role
        self._editors = {}
        self._cache_editors = True

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        value = self._editor_for_index(index)
        if not isinstance(value, widgets.QWidget):
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

    def _editor_for_index(self, index: core.ModelIndex) -> widgets.QWidget:
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
        if key in self._editors:
            return self._editors[key]
        self._editors[key] = editor
        return editor

    def createEditor(
        self,
        parent: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        editor = self._editor_for_index(index)
        if isinstance(editor, widgets.QWidget):
            metaobj = core.MetaObject(editor.metaObject())
            editor = metaobj.copy(editor)
            editor.setParent(parent)
            editor.setAutoFillBackground(True)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor: widgets.QWidget, index: core.ModelIndex):
        pass

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        orig = self._editor_for_index(index)
        if isinstance(orig, widgets.QWidget):
            metaobj = core.MetaObject(orig.metaObject())
            if user_prop := metaobj.get_user_property():
                value = user_prop.read(editor)
                user_prop.write(orig, value)

    def sizeHint(self, option: widgets.QStyleOptionViewItem, index: core.ModelIndex):
        editor = self._editor_for_index(index)
        if isinstance(editor, widgets.QWidget):
            return editor.sizeHint()
        else:
            return super().sizeHint(option, index)

    def updateEditorGeometry(
        self,
        editor: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        pass


if __name__ == "__main__":
    import logging

    app = widgets.app()
    table_widget = widgets.TableView()
    pb = widgets.PushButton("test", clicked=lambda: logging.info("x"))

    class Model(core.AbstractTableModel):
        def rowCount(self, index: core.ModelIndex | None = None):
            return 5

        def columnCount(self, index: core.ModelIndex | None = None):
            return 5

        def data(
            self,
            index: core.ModelIndex,
            role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        ):
            match role, index.column():
                case constants.DISPLAY_ROLE | constants.USER_ROLE, 0:
                    # return pb
                    return widgets.PushButton("test", clicked=lambda: logging.info("x"))

                case constants.DISPLAY_ROLE | constants.USER_ROLE, 1:
                    return pb

        def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
            return super().flags(index) | constants.IS_EDITABLE

    table_widget.set_delegate("widget")
    model = Model()
    table_widget.set_model(model)
    table_widget.set_edit_triggers("all")
    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()
    with app.debug_mode():
        app.exec()

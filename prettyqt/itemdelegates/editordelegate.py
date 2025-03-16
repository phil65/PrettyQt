from __future__ import annotations

import enum
import logging
from typing import Any

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class EditorDelegate(widgets.StyledItemDelegate):
    """Delegate which supports editing a large range of data types.

    Allows editing a large range of different types from Qt, builtin libraries as well
    as some Numpy types.

    The Delegate also has an extended displayText method to show a repr-like string for
    different data types.

    The following data types are supported:

    * bool
    * enum.Flag
    * enum.Enum
    * int
    * float
    * str
    * range
    * slice
    * list of ints
    * list of floats
    * list of strings
    * pathlib.Path
    * re.Pattern
    * datetime.date
    * datetime.time
    * datetime.datetime
    * QtCore.QRegularExpression
    * QtCore.QTime
    * QtCore.QDate
    * QtCore.QDateTime
    * QtCore.QPoint
    * QtCore.QPointF
    * QtCore.QRect
    * QtCore.QRectF
    * QtCore.QRection
    * QtCore.QKeyCombination
    * QtCore.QLocale
    * QtCore.QSize
    * QtCore.QSizeF
    * QtCore.QUrl
    * QtGui.QFont
    * QtGui.QKeySequence
    * QtGui.QPalette
    * QtGui.QColor
    * QtGui.QBrush
    * QtGui.QCursor
    * QtGui.QIcon
    * QtWidgets.QSizePolicy

    If numpy is installed, the following types are supported, too:

    * numpy.floating
    * numpy.integer
    * numpy.str_
    * numpy.datetime64
    * numpy.bool_

    """

    ID = "editor"

    def __init__(
        self,
        *args,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
        validator: (
            gui.QValidator | widgets.lineedit.ValidatorStr | datatypes.PatternType | None
        ) = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._role = role
        self._validator = validator

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        # if not self.is_supported_type(value):
        #     option = widgets.StyleOptionViewItem(option)
        #     option.state &= ~widgets.QStyle.StateFlag.State_Enabled
        from prettyqt import itemdelegates

        match value := self._data_for_index(index, self._role):
            case gui.QIcon():
                icon_delegate = itemdelegates.IconDelegate()
                icon_delegate.paint(painter, option, index)
                return
            case enum.Enum():  # PySide6 needs this when using Views
                option.text = value.name
                option.widget.style().drawControl(
                    widgets.QStyle.ControlElement.CE_ItemViewItem, option, painter
                )
            case _:
                super().paint(painter, option, index)

    def createEditor(
        self,
        parent: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        val = self._data_for_index(index, self._role)
        logger.info("creating editor for %r...", val)
        if isinstance(val, list):
            widget = datatypes.get_editor_for_value_list(val, parent)
        else:
            widget = datatypes.get_editor_for_value(val, parent)
        if widget is None:
            logger.warning("Could not find editor for %r (%s)", val, type(val))
            return None
        if self._validator and isinstance(
            widget, widgets.LineEdit | widgets.AbstractSpinBoxMixin
        ):
            widget.set_validator(self._validator, append=True)

        widget.setAutoFillBackground(True)
        widget.set_focus_policy("strong")
        return widget

    def setEditorData(self, editor: widgets.QWidget, index: core.ModelIndex):
        value = self._data_for_index(index, self._role)
        logger.info("setting data for %r to %r", editor, value)
        editor.set_value(value)

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        if (value := editor.get_value()) is not None:
            logger.info("setting data for %r to %r", model, value)
            model.setData(index, value, self._role)
            # self.closeEditor.emit(editor, self.EndEditHint.NoHint)
            self.commitData.emit(editor)

    def displayText(self, value: Any, locale: core.QLocale) -> str:
        return datatypes.to_string(value, locale)


if __name__ == "__main__":
    import pathlib
    import re

    app = widgets.app()
    table_widget = widgets.TableWidget(15, 2)
    table_widget.set_edit_triggers("all")
    table_widget.set_selection_behavior("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    types = dict(
        color=gui.QColor(30, 30, 30),
        time=core.QTime(1, 1, 1),
        date=core.QDate(1, 1, 1),
        datetime=core.QDateTime(1, 1, 1, 1, 1, 1),
        font=gui.QFont(),
        str="fdsf",
        int=8,
        float=8.2,
        path=pathlib.Path(),
        url=core.QUrl("http://www.google.de"),
        # regex=core.QRegularExpression("[a-z]"),
        regex=re.compile("[a-z]"),
        enum=constants.ItemDataRole.UserRole,
        bool=True,
        keysequence=gui.QKeySequence("Ctrl+A"),
    )
    for i, (k, v) in enumerate(types.items()):
        item_1 = widgets.TableWidgetItem(k)
        item_2 = widgets.TableWidgetItem()
        item_2.setData(constants.DISPLAY_ROLE, v)
        item_2.setData(constants.USER_ROLE, v)
        table_widget[i, 0] = item_1
        table_widget[i, 1] = item_2

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()
    with app.debug_mode():
        delegate = table_widget.set_delegate("editor", column=1)
        delegate.closeEditor.connect(print)
        app.exec()

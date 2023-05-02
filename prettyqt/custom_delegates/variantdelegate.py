from __future__ import annotations

import enum
import pathlib

import regex as re

from prettyqt import constants, custom_widgets, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


class VariantDelegate(widgets.ItemDelegate):
    def __init__(
        self,
        data_role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        parent: QtWidgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self.data_role = data_role

    def paint(self, painter, option, index):
        value = index.model().data(index, self.data_role)
        if not self.is_supported_type(value):
            option = widgets.StyleOptionViewItem(option)
            option.state &= ~QtWidgets.QStyle.StateFlag.State_Enabled
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        original_value = index.model().data(index, self.data_role)
        if not self.is_supported_type(original_value):
            return None

        match original_value:
            case bool():
                return widgets.CheckBox(parent=parent)
            case enum.Enum():
                return custom_widgets.EnumComboBox(
                    parent=parent, enum_class=original_value.__class__
                )
            case int():
                return widgets.SpinBox(parent=parent)
            case float():
                return widgets.DoubleSpinBox(parent=parent)
            case QtCore.QRegularExpression() | re.Pattern():
                editor = custom_widgets.RegexInput(show_error=False, parent=parent)
                return editor
            case QtGui.QColor():
                return custom_widgets.ColorComboBox(parent=parent)
            case QtCore.QTime():
                return widgets.TimeEdit(parent=parent)
            case QtGui.QFont():
                return widgets.FontComboBox(parent=parent)
            case QtCore.QDate():
                return widgets.DateEdit(parent=parent)
            case QtCore.QDateTime():
                return widgets.DateTimeEdit(parent=parent)
            case QtGui.QKeySequence():
                return widgets.KeySequenceEdit(parent=parent)
            case pathlib.Path():
                return custom_widgets.FileChooserButton(parent=parent)
            case str():
                editor = widgets.LineEdit(parent=parent)
                editor.setFrame(False)
                return editor
            case _:
                return None

    def setEditorData(self, editor, index):
        if not editor:
            return
        value = index.model().data(index, self.data_role)
        editor.set_value(value)

    def setModelData(self, editor, model, index):
        if (value := editor.get_value()) is not None:
            model.setData(index, value, self.data_role)
            model.setData(index, self.display_text(value), constants.DISPLAY_ROLE)

    @staticmethod
    def is_supported_type(value):
        return isinstance(
            value,
            bool
            | float
            | int
            | str
            | QtGui.QColor
            | QtGui.QFont
            | QtGui.QKeySequence
            | QtCore.QDate
            | QtCore.QDateTime
            | QtCore.QTime
            | re.Pattern
            | QtCore.QRegularExpression
            | pathlib.Path,
        )

    @staticmethod
    def display_text(val):
        match val:
            case str():
                return val
            case bool():
                return "✓" if val else "☐"
            case int() | float() | QtCore.QByteArray():
                return str(val)
            case QtGui.QColor():
                return f"({val.red()},{val.green()},{val.blue()},{val.alpha()})"
            case QtCore.QDate() | QtCore.QDateTime() | QtCore.QTime():
                return val.toString(QtCore.Qt.DateFormat.ISODate)
            case QtCore.QPoint():
                return f"({val.x()},{val.y()})"
            case QtCore.QRect():
                return f"({val.x()},{val.y()},{val.width()},{val.height()})"
            case QtCore.QSize():
                return f"({val.width()},{val.height()})"
            case list():
                return ",".join(map(repr, val))
            case re.Pattern():
                return val.pattern
            case QtCore.QRegularExpression():
                return val.pattern()
            case None:
                return "<Invalid>"
            case _:
                return f"<{val}>"


if __name__ == "__main__":
    app = widgets.app()
    table_widget = widgets.TableWidget(15, 2)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(
        table_widget.EditTrigger.DoubleClicked  # type: ignore
        | table_widget.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    types = dict(
        color=QtGui.QColor(30, 30, 30),
        time=QtCore.QTime(1, 1, 1),
        date=QtCore.QDate(1, 1, 1),
        datetime=QtCore.QDateTime(1, 1, 1, 1, 1, 1),
        font=QtGui.QFont(),
        str="fdsf",
        int=8,
        float=8.2,
        path=pathlib.Path(),
        url=QtCore.QUrl("http://www.google.de"),
        # regex=QtCore.QRegularExpression("[a-z]"),
        regex=re.compile("[a-z]"),
        enum=QtCore.Qt.ItemDataRole.UserRole,
        bool=True,
        keysequence=QtGui.QKeySequence("Ctrl+A"),
    )
    for i, (k, v) in enumerate(types.items()):
        item_1 = widgets.TableWidgetItem(k)
        item_2 = widgets.TableWidgetItem()
        item_2.setData(constants.DISPLAY_ROLE, v)
        item_2.setData(constants.USER_ROLE, v)
        table_widget[i, 0] = item_1
        table_widget[i, 1] = item_2

    delegate = VariantDelegate(parent=table_widget)
    table_widget.set_delegate(delegate, column=1)

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()

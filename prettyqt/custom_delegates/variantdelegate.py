from __future__ import annotations

import datetime
import enum
import pathlib

import regex as re

from prettyqt import constants, custom_delegates, custom_widgets, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


class VariantDelegate(widgets.StyledItemDelegate):
    def __init__(
        self,
        data_role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        parent: QtWidgets.QAbstractItemView | None = None,
    ):
        super().__init__(parent)
        self.data_role = data_role

    def paint(self, painter, option, index):
        value = self._data_for_index(index, self.data_role)
        if not self.is_supported_type(value):
            option = widgets.StyleOptionViewItem(option)
            option.state &= ~QtWidgets.QStyle.StateFlag.State_Enabled
        if isinstance(value, QtGui.QIcon):
            icon_delegate = custom_delegates.IconDelegate()
            icon_delegate.paint(painter, option, index)
            return
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        original_value = self._data_for_index(index, self.data_role)
        if not self.is_supported_type(original_value):
            return None
        match original_value:
            case bool():
                widget = widgets.CheckBox(parent=parent)
            case enum.Flag():
                widget = custom_widgets.EnumFlagWidget(parent=parent)
            case enum.Enum():
                widget = custom_widgets.EnumComboBox(parent=parent)
            case int():
                widget = widgets.SpinBox(parent=parent)
            case float():
                widget = widgets.DoubleSpinBox(parent=parent)
            case pathlib.Path():
                widget = custom_widgets.FileChooserButton(parent=parent)
            case str():
                widget = widgets.LineEdit(parent=parent)
                widget.setFrame(False)
            case QtCore.QRegularExpression() | re.Pattern():
                widget = custom_widgets.RegexInput(show_error=False, parent=parent)
            case QtCore.QTime():
                widget = widgets.TimeEdit(parent=parent)
            case QtCore.QDate():
                widget = widgets.DateEdit(parent=parent)
            case QtCore.QDateTime():
                widget = widgets.DateTimeEdit(parent=parent)
            case QtCore.QPoint():
                widget = custom_widgets.PointEdit(parent=parent)
            case QtCore.QSize():
                widget = custom_widgets.SizeEdit(parent=parent)
            case QtCore.QRect():
                widget = custom_widgets.RectEdit(parent=parent)
            case QtGui.QKeySequence():
                widget = widgets.KeySequenceEdit(parent=parent)
            case QtGui.QRegion():
                widget = custom_widgets.RegionEdit(parent=parent)
            case QtGui.QFont():
                widget = widgets.FontComboBox(parent=parent)
            case QtGui.QColor():
                widget = custom_widgets.ColorComboBox(parent=parent)
            case QtWidgets.QSizePolicy():
                widget = custom_widgets.SizePolicyEdit(parent=parent)
            # case QtCore.QRectF():  # todo
            #     widget = custom_widgets.RectEdit(parent=parent)
            case _:
                return None
        widget.setAutoFillBackground(True)
        return widget

    def setEditorData(self, editor, index):
        if not editor:
            return
        value = self._data_for_index(index, self.data_role)
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
            | enum.Flag
            | enum.Enum
            | int
            | float
            | str
            | re.Pattern
            | pathlib.Path
            | QtCore.QRegularExpression
            | QtCore.QDate
            | QtCore.QDateTime
            | QtCore.QTime
            | QtCore.QRect
            | QtCore.QPoint
            | QtCore.QSize
            | QtCore.QTime
            | QtGui.QPalette
            | QtGui.QIcon
            | QtGui.QColor
            | QtGui.QFont
            | QtGui.QKeySequence
            | QtWidgets.QSizePolicy,
        )

    @staticmethod
    def display_text(val):
        match val:
            case str():
                return val
            case bool():
                return "✓" if val else "☐"
            case enum.Flag():
                return val.name
            case enum.Enum():
                return val.name
            case int() | float() | QtCore.QByteArray():
                return str(val)
            case QtGui.QColor():
                return f"({val.red()},{val.green()},{val.blue()},{val.alpha()})"
            case QtGui.QFont():
                return val.family()
            case QtGui.QRegion():
                rect = val.boundingRect()
                return f"({rect.x()},{rect.y()},{rect.width()},{rect.height()})"
            case QtGui.QCursor():
                return constants.CURSOR_SHAPE.inverse[val.shape()]
            case QtGui.QKeySequence():
                return val.toString()
            case QtCore.QDate() | QtCore.QDateTime() | QtCore.QTime():
                return val.toString(QtCore.Qt.DateFormat.ISODate)
            case QtCore.QPoint():
                return f"({val.x()},{val.y()})"
            case QtCore.QRect():
                return f"({val.x()},{val.y()},{val.width()},{val.height()})"
            case QtCore.QSize():
                return f"({val.width()},{val.height()})"
            case QtCore.QLocale():
                return val.bcp47Name()
            case QtWidgets.QSizePolicy():
                return (
                    f"({widgets.sizepolicy.SIZE_POLICY.inverse[val.horizontalPolicy()]}, "
                    f"{widgets.sizepolicy.SIZE_POLICY.inverse[val.verticalPolicy()]}, "
                    f"{widgets.sizepolicy.CONTROL_TYPE.inverse[val.controlType()]})"
                )
            case list():
                return ",".join(map(repr, val))
            case re.Pattern():
                return val.pattern
            case datetime.date():
                return val.isoformat()
            case datetime.datetime():
                return val.isoformat(sep=" ")
            case QtCore.QRegularExpression():
                return val.pattern()
            case QtCore.QUrl():
                return val.toString()
            # case np.integer():
            #     return super().displayText(int(val), locale)
            # case np.floating():
            #     return super().displayText(float(val), locale)
            # case np.str_():
            #     return str(val)
            # case np.datetime64():
            #     return self.displayText(val.astype(datetime), locale)
            case None:
                return "<None>"
            case _:
                return f"<{val}>"

    def displayText(self, value, locale: QtCore.QLocale) -> str:
        return self.display_text(value)


if __name__ == "__main__":
    app = widgets.app()
    table_widget = widgets.TableWidget(15, 2)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(
        table_widget.EditTrigger.DoubleClicked | table_widget.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behavior("rows")
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
    with app.debug_mode():
        app.main_loop()

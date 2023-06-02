from __future__ import annotations

import datetime
import enum
import logging
import pathlib

import regex as re

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


logger = logging.getLogger(__name__)


class VariantDelegate(widgets.StyledItemDelegate):
    ID = "variant"

    def __init__(
        self,
        *args,
        data_role: QtCore.Qt.ItemDataRole = constants.USER_ROLE,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data_role = data_role

    def paint(self, painter, option, index):
        # if not self.is_supported_type(value):
        #     option = widgets.StyleOptionViewItem(option)
        #     option.state &= ~QtWidgets.QStyle.StateFlag.State_Enabled
        from prettyqt import custom_delegates

        match value := self._data_for_index(index, self.data_role):
            case QtGui.QIcon():
                icon_delegate = custom_delegates.IconDelegate()
                icon_delegate.paint(painter, option, index)
                return
            case enum.Enum():  # PySide6 needs this when using Views
                option.text = value.name
                option.widget.style().drawControl(
                    QtWidgets.QStyle.ControlElement.CE_ItemViewItem, option, painter
                )
            case _:
                super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        from prettyqt import custom_widgets

        original_value = self._data_for_index(index, self.data_role)
        logger.info(f"creating editor for {original_value!r}...")
        widget = None
        match original_value:
            case bool():
                widget = widgets.CheckBox()
            case enum.Flag():
                widget = custom_widgets.EnumFlagWidget()
                widget._set_enum_class(type(original_value))
            case enum.Enum():
                widget = custom_widgets.EnumComboBox()
                widget._set_enum_class(type(original_value))
            case int():
                widget = widgets.SpinBox()
            case float():
                widget = widgets.DoubleSpinBox()
            case pathlib.Path():
                widget = custom_widgets.FileChooserButton()
            case str():
                widget = widgets.LineEdit()
                widget.setFrame(False)
            case QtCore.QRegularExpression() | re.Pattern():
                widget = custom_widgets.RegexInput(show_error=False)
            case QtCore.QTime():
                widget = widgets.TimeEdit()
            case QtCore.QDate():
                widget = widgets.DateEdit()
            case QtCore.QDateTime():
                widget = widgets.DateTimeEdit()
            case QtCore.QPoint():
                widget = custom_widgets.PointEdit()
            case QtCore.QSize():
                widget = custom_widgets.SizeEdit()
            case QtCore.QRect():
                widget = custom_widgets.RectEdit()
            case QtGui.QKeySequence():
                widget = widgets.KeySequenceEdit()
            case QtGui.QRegion():
                widget = custom_widgets.RegionEdit()
            case QtGui.QFont():
                widget = widgets.FontComboBox()
            case QtGui.QColor():
                widget = custom_widgets.ColorComboBox()
            case QtWidgets.QSizePolicy():
                widget = custom_widgets.SizePolicyEdit()
            case QtCore.QUrl():
                widget = custom_widgets.UrlLineEdit()
            # case QtCore.QRectF():  # todo
            #     widget = custom_widgets.RectEdit(parent=parent)
        try:
            import numpy as np
        except ImportError:
            pass
        else:
            match original_value:
                case np.floating():
                    widget = custom_widgets.FloatLineEdit()

        if widget is None:
            logger.warning(f"Could not find editor for {original_value!r}")
            return None
        widget.setParent(parent)
        widget.setAutoFillBackground(True)
        return widget

    def setEditorData(self, editor, index):
        # if not editor:
        #     return
        value = self._data_for_index(index, self.data_role)
        logger.info(f"setting data for {editor!r} to {value!r}")
        editor.set_value(value)

    def setModelData(self, editor, model, index):
        if (value := editor.get_value()) is not None:
            logger.info(f"setting data for {model!r} to {value!r}")
            model.setData(index, value, self.data_role)
            model.setData(index, self.display_text(value), constants.DISPLAY_ROLE)
            self.commitData.emit(editor)
            # self.closeEditor.emit(editor, self.EndEditHint.NoHint)

    def displayText(self, value, locale: QtCore.QLocale) -> str:
        return self.display_text(value, locale)

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

    @classmethod
    def display_text(cls, val, locale=None):
        if locale is None:
            locale = core.Locale()
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
                return locale.toString(val)
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
        try:
            import numpy as np
        except ImportError:
            pass
        else:
            match val:
                case np.integer():
                    return cls.display_text(int(val), locale)
                case np.floating():
                    return cls.display_text(float(val), locale)
                case np.str_():
                    return str(val)
                case np.datetime64():
                    return cls.display_text(val.astype(datetime.datetime), locale)
        return repr(val)


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

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()
    with app.debug_mode():
        table_widget.set_delegate("variant", column=1)
        app.main_loop()

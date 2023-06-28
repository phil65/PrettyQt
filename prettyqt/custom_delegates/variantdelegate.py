from __future__ import annotations

from typing import Any
import enum
import logging

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class VariantDelegate(widgets.StyledItemDelegate):
    """Delegate which supports editing many data types."""

    ID = "variant"

    def __init__(
        self,
        *args,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
        validator: gui.QValidator
        | widgets.lineedit.ValidatorStr
        | datatypes.PatternType
        | None = None,
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
        from prettyqt import custom_delegates

        match value := self._data_for_index(index, self._role):
            case gui.QIcon():
                icon_delegate = custom_delegates.IconDelegate()
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
        logger.info(f"creating editor for {val!r}...")
        widget = datatypes.get_widget_for_value(val, parent)
        if widget is None:
            logger.warning(f"Could not find editor for {val!r} ({type(val)})")
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
        logger.info(f"setting data for {editor!r} to {value!r}")
        editor.set_value(value)

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        if (value := editor.get_value()) is not None:
            logger.info(f"setting data for {model!r} to {value!r}")
            model.setData(index, value, self._role)
            # self.closeEditor.emit(editor, self.EndEditHint.NoHint)
            self.commitData.emit(editor)

    def displayText(self, value: Any, locale: core.QLocale) -> str:
        return datatypes.to_string(value, locale)


if __name__ == "__main__":
    import re
    import pathlib

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
        delegate = table_widget.set_delegate("variant", column=1, set_edit_role=True)
        delegate.closeEditor.connect(print)
        app.exec()

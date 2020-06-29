# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict

WRAP_MODES = bidict(none=QtGui.QTextOption.NoWrap,
                    word=QtGui.QTextOption.WordWrap,
                    manual=QtGui.QTextOption.ManualWrap,
                    anywhere=QtGui.QTextOption.WrapAnywhere,
                    boundary_or_anywhere=QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

LINE_WRAP_MODES = bidict(none=QtWidgets.QPlainTextEdit.NoWrap,
                         widget_width=QtWidgets.QPlainTextEdit.WidgetWidth)

QtWidgets.QPlainTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class PlainTextEdit(QtWidgets.QPlainTextEdit):

    value_changed = core.Signal()

    def __init__(self, text="", parent=None, read_only=False):
        super().__init__(text, parent)
        self.validator = None
        self.textChanged.connect(self._on_value_change)
        self.set_read_only(read_only)

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    read_only=self.isReadOnly(),
                    font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.__init__()
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])
        self.setReadOnly(state["read_only"])

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    @contextlib.contextmanager
    def create_cursor(self):
        cursor = gui.TextCursor(self.document())
        yield cursor
        self.setTextCursor(cursor)

    @contextlib.contextmanager
    def current_cursor(self):
        cursor = gui.TextCursor(self.textCursor())
        yield cursor
        self.setTextCursor(cursor)

    def append_text(self, text: str):
        self.appendPlainText(text)

    def set_text(self, text: str):
        self.setPlainText(text)

    def text(self) -> str:
        return self.toPlainText()

    def select_text(self, start: int, end: int):
        with self.create_cursor() as c:
            c.select_text(start, end)

    def set_read_only(self, value: bool = True):
        """set test to read only

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = widgets.TextEdit.ExtraSelection()
            line_color = gui.Color("yellow").lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    @classmethod
    def get_result_widget(cls, *args, **kwargs):
        widget = cls(*args, **kwargs)
        widget.setReadOnly(True)
        widget.set_font("Consolas")
        return widget

    def set_wrap_mode(self, mode: str):
        """set word wrap mode

        Allowed values are "none", "word", "manual", "anywhere", "boundary_or_anywhere"

        Args:
            style: word wrap mode to use

        Raises:
            ValueError: wrap mode does not exist
        """
        if mode not in WRAP_MODES:
            raise ValueError(f"invalid wrap mode. Allowed values: {WRAP_MODES.keys()}")
        self.setWordWrapMode(WRAP_MODES[mode])

    def set_line_wrap_mode(self, mode: str):
        """set line wrap mode

        Allowed values are "none" and "widget width"

        Args:
            style: line wrap mode to use

        Raises:
            ValueError: line wrap mode does not exist
        """
        if mode not in LINE_WRAP_MODES:
            raise ValueError(f"invalid wrap mode. "
                             f"Allowed values: {LINE_WRAP_MODES.keys()}")
        self.setLineWrapMode(LINE_WRAP_MODES[mode])

    def _on_value_change(self):
        self.value_changed.emit()
        if self.validator is not None:
            self.set_validation_color()

    def set_validation_color(self, state: bool = True):
        color = "rgb(255, 175, 90)" if not self.is_valid() else "white"
        self.set_background_color(color)

    def set_validator(self, validator: gui.Validator):
        self.validator = validator
        self.set_validation_color()

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegExpValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def is_valid(self):
        if self.validator is None:
            return True
        return self.validator.is_valid_value(self.text())

    def set_value(self, value: str):
        self.setPlainText(value)

    def get_value(self):
        return self.text()


if __name__ == "__main__":
    from prettyqt import custom_validators
    val = custom_validators.RegularExpressionValidator()
    app = widgets.app()
    widget = PlainTextEdit("This is a test")
    widget.set_validator(val)
    with widget.current_cursor() as c:
        c.select_text(2, 4)
    widget.show()
    app.exec_()

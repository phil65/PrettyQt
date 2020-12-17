import contextlib
from typing import Literal, Optional

from qtpy import QtGui, QtWidgets

from prettyqt import constants, core, gui, syntaxhighlighters, widgets
from prettyqt.utils import InvalidParamError, bidict


WRAP_MODE = bidict(
    none=QtGui.QTextOption.NoWrap,
    word=QtGui.QTextOption.WordWrap,
    anywhere=QtGui.QTextOption.WrapAnywhere,
    boundary_or_anywhere=QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere,
)

WrapModeStr = Literal["none", "word", "anywhere", "boundary_or_anywhere"]

LINE_WRAP_MODE = bidict(
    none=QtWidgets.QPlainTextEdit.NoWrap,
    widget_width=QtWidgets.QPlainTextEdit.WidgetWidth,
)

LineWrapModeStr = Literal["none", "widget_width"]


QtWidgets.QPlainTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class PlainTextEdit(QtWidgets.QPlainTextEdit):

    value_changed = core.Signal()

    def __init__(
        self,
        text: str = "",
        parent: Optional[QtWidgets.QWidget] = None,
        read_only: bool = False,
    ):
        super().__init__(text, parent)
        self._allow_wheel_zoom = False
        self.validator: Optional[QtGui.QValidator] = None
        self.textChanged.connect(self._on_value_change)
        self.set_read_only(read_only)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            read_only=self.isReadOnly(),
            font=gui.Font(self.font()),
        )

    def __setstate__(self, state):
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])
        self.setReadOnly(state["read_only"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    def wheelEvent(self, event):
        """Handle wheel event for zooming."""
        if not self._allow_wheel_zoom:
            return None
        if event.modifiers() & constants.CTRL_MOD:
            self.zoomIn() if event.angleDelta().y() > 0 else self.zoomOut()
        else:
            super().wheelEvent(event)

    def allow_wheel_zoom(self, do_zoom: bool = True):
        self._allow_wheel_zoom = do_zoom

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

    def move_cursor(
        self,
        operation: gui.textcursor.MoveOperationStr,
        mode: gui.textcursor.MoveModeStr = "move",
    ):
        op = gui.textcursor.MOVE_OPERATION[operation]
        mode = gui.textcursor.MOVE_MODE[mode]
        self.moveCursor(op, mode)

    def append_text(self, text: str, newline: bool = True):
        if newline:
            self.appendPlainText(text)
        else:
            self.move_cursor("end")
            self.insertPlainText(text)
            self.move_cursor("end")

    def set_text(self, text: str):
        self.setPlainText(text)

    def set_syntaxhighlighter(self, syntax: str, style: Optional[str] = None):
        self._hl = syntaxhighlighters.PygmentsHighlighter(self.document(), syntax)
        if style is not None:
            self._hl.set_style(style)

    def text(self) -> str:
        return self.toPlainText()

    def select_text(self, start: int, end: int):
        with self.create_cursor() as c:
            c.select_text(start, end)

    def set_read_only(self, value: bool = True):
        """Make the PlainTextEdit read-only.

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def highlight_current_line(self, color="yellow"):
        extra_selections = []

        if not self.isReadOnly():
            selection = widgets.TextEdit.ExtraSelection()
            line_color = gui.Color(color)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def set_wrap_mode(self, mode: WrapModeStr):
        """Set word wrap mode.

        Args:
            mode: word wrap mode to use

        Raises:
            InvalidParamError: wrap mode does not exist
        """
        if mode not in WRAP_MODE:
            raise InvalidParamError(mode, WRAP_MODE)
        self.setWordWrapMode(WRAP_MODE[mode])

    def get_wrap_mode(self) -> str:
        """Get the current word wrap mode.

        Returns:
            Word wrap mode
        """
        return WRAP_MODE.inverse[self.wordWrapMode()]

    def set_line_wrap_mode(self, mode: LineWrapModeStr):
        """Set line wrap mode.

        Args:
            mode: line wrap mode to use

        Raises:
            InvalidParamError: line wrap mode does not exist
        """
        if mode not in LINE_WRAP_MODE:
            raise InvalidParamError(mode, LINE_WRAP_MODE)
        self.setLineWrapMode(LINE_WRAP_MODE[mode])

    def get_line_wrap_mode(self) -> LineWrapModeStr:
        """Get the current wrap mode.

        Returns:
            Wrap mode
        """
        return LINE_WRAP_MODE.inverse[self.lineWrapMode()]

    def _on_value_change(self):
        self.value_changed.emit()
        if self.validator is not None:
            self._set_validation_color()

    def _set_validation_color(self, state: bool = True):
        color = "orange" if not self.is_valid() else None
        self.set_background_color(color)

    def set_validator(self, validator: Optional[QtGui.QValidator]):
        self.validator = validator
        self._set_validation_color()

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

    val = custom_validators.RegexPatternValidator()
    app = widgets.app()
    widget = PlainTextEdit("This is a test")
    widget.set_validator(val)
    with widget.current_cursor() as c:
        c.select_text(2, 4)
    widget.show()
    app.main_loop()

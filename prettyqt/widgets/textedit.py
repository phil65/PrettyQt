from __future__ import annotations

from collections.abc import Iterator
import contextlib
from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, colors, mappers, types


AUTO_FORMATTING = mappers.FlagMap(
    QtWidgets.QTextEdit.AutoFormattingFlag,
    none=QtWidgets.QTextEdit.AutoFormattingFlag.AutoNone,
    bullet_list=QtWidgets.QTextEdit.AutoFormattingFlag.AutoBulletList,
    all=QtWidgets.QTextEdit.AutoFormattingFlag.AutoAll,
)

AutoFormattingStr = Literal["none", "bullet_list", "all"]

LINE_WRAP_MODE = bidict(
    none=QtWidgets.QTextEdit.LineWrapMode.NoWrap,
    widget_width=QtWidgets.QTextEdit.LineWrapMode.WidgetWidth,
    fixed_pixel_width=QtWidgets.QTextEdit.LineWrapMode.FixedPixelWidth,
    fixed_column_width=QtWidgets.QTextEdit.LineWrapMode.FixedColumnWidth,
)

LineWrapModeStr = Literal[
    "none", "widget_width", "fixed_pixel_width", "fixed_column_width"
]


QtWidgets.QTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class TextEdit(QtWidgets.QTextEdit):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            accept_rich_text=self.acceptRichText(),
            auto_formatting=self.get_auto_formatting(),
            cursor_width=self.cursorWidth(),
            document_title=self.documentTitle(),
            line_wrap_column_or_width=self.lineWrapColumnOrWidth(),
            line_wrap_mode=self.get_line_wrap_mode(),
            word_wrap_mode=self.get_word_wrap_mode(),
            overwrite_mode=self.overwriteMode(),
            placeholder_text=self.placeholderText(),
            read_only=self.isReadOnly(),
            tab_changes_focus=self.tabChangesFocus(),
            tab_stop_distance=self.tabStopDistance(),
            undo_redo_enabled=self.isUndoRedoEnabled(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_text(state["text"])
        self.setAcceptRichText(state["accept_rich_text"])
        self.set_auto_formatting(state["auto_formatting"])
        self.setCursorWidth(state["cursor_width"])
        self.setDocumentTitle(state["document_title"])
        self.setLineWrapColumnOrWidth(state["line_wrap_column_or_width"])
        self.set_line_wrap_mode(state["line_wrap_mode"])
        self.set_word_wrap_mode(state["word_wrap_mode"])
        self.setOverwriteMode(state["overwrite_mode"])
        self.setPlaceholderText(state["placeholder_text"])
        self.setReadOnly(state["read_only"])
        self.setTabChangesFocus(state["tab_changes_focus"])
        self.setTabStopDistance(state["tab_stop_distance"])
        self.setUndoRedoEnabled(state["undo_redo_enabled"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str) -> TextEdit:
        self.append_text(other)
        return self

    def on_value_change(self) -> None:
        self.value_changed.emit(self.text())

    @contextlib.contextmanager
    def create_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self.document())
        yield cursor
        self.setTextCursor(cursor)

    def get_text_cursor(self) -> gui.TextCursor:
        return gui.TextCursor(self.textCursor())

    def set_text(self, text: str) -> None:
        self.setPlainText(text)

    def append_text(self, text: str) -> None:
        self.append(text)

    def text(self) -> str:
        return self.toPlainText()

    def select_text(self, start: int, end: int) -> None:
        with self.create_cursor() as c:
            c.select_text(start, end)

    def set_read_only(self, value: bool = True) -> None:
        self.setReadOnly(value)

    def set_text_color(self, color: types.ColorType) -> None:
        color = colors.get_color(color)
        self.setTextColor(color)

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

    def set_auto_formatting(self, mode: AutoFormattingStr):
        """Set auto formatting mode.

        Args:
            mode: auto formatting mode to use

        Raises:
            InvalidParamError: auto formatting mode does not exist
        """
        if mode not in AUTO_FORMATTING:
            raise InvalidParamError(mode, AUTO_FORMATTING)
        self.setAutoFormatting(AUTO_FORMATTING[mode])

    def get_auto_formatting(self) -> AutoFormattingStr:
        """Get the current auto formatting mode.

        Returns:
            Auto formatting mode
        """
        return AUTO_FORMATTING.inverse[self.autoFormatting()]

    def set_word_wrap_mode(self, mode: gui.textoption.WordWrapModeStr):
        """Set word wrap mode.

        Args:
            mode: word wrap mode to use

        Raises:
            InvalidParamError: wrap mode does not exist
        """
        if mode not in gui.textoption.WORD_WRAP_MODE:
            raise InvalidParamError(mode, gui.textoption.WORD_WRAP_MODE)
        self.setWordWrapMode(gui.textoption.WORD_WRAP_MODE[mode])

    def get_word_wrap_mode(self) -> gui.textoption.WordWrapModeStr:
        """Get the current word wrap mode.

        Returns:
            Word wrap mode
        """
        return gui.textoption.WORD_WRAP_MODE.inverse[self.wordWrapMode()]


if __name__ == "__main__":
    app = widgets.app()
    widget = TextEdit("This is a test")
    widget.show()
    app.main_loop()

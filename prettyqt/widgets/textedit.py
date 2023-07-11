from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, colors, datatypes, texteditselecter


AutoFormattingStr = Literal["none", "bullet_list", "all"]

AUTO_FORMATTING: bidict[AutoFormattingStr, widgets.QTextEdit.AutoFormattingFlag] = bidict(
    none=widgets.QTextEdit.AutoFormattingFlag.AutoNone,
    bullet_list=widgets.QTextEdit.AutoFormattingFlag.AutoBulletList,
    all=widgets.QTextEdit.AutoFormattingFlag.AutoAll,
)

LineWrapModeStr = Literal[
    "none", "widget_width", "fixed_pixel_width", "fixed_column_width"
]

LINE_WRAP_MODE: bidict[LineWrapModeStr, widgets.QTextEdit.LineWrapMode] = bidict(
    none=widgets.QTextEdit.LineWrapMode.NoWrap,
    widget_width=widgets.QTextEdit.LineWrapMode.WidgetWidth,
    fixed_pixel_width=widgets.QTextEdit.LineWrapMode.FixedPixelWidth,
    fixed_column_width=widgets.QTextEdit.LineWrapMode.FixedColumnWidth,
)


class TextEditMixin(widgets.AbstractScrollAreaMixin):
    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.on_value_change)
        self.selecter = texteditselecter.TextEditSelecter(self)

    def __add__(self, other: str) -> TextEdit:
        self.append_text(other)
        return self

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "autoFormatting": AUTO_FORMATTING,
            "lineWrapMode": LINE_WRAP_MODE,
            "wordWrapMode": gui.textoption.WORD_WRAP_MODE,
        }
        return maps

    def on_value_change(self) -> None:
        self.value_changed.emit(self.text())

    def set_text(self, text: str) -> None:
        self.setPlainText(text)

    def append_text(
        self,
        text: str,
        newline: bool = True,
        ensure_visible: Literal["always", "when_bottom", "never"] = "always",
    ):
        scrollbar = self.verticalScrollBar()
        at_bottom = scrollbar.value() >= (scrollbar.maximum() - 4)
        prev_val = scrollbar.value()
        if newline:
            self.append(text)
        else:
            self.selecter.move_cursor("end")
            self.insertHtml(text)
            self.selecter.move_cursor("end")
        match ensure_visible:
            case "always":
                self.ensureCursorVisible()
            case "when_bottom":
                if at_bottom:
                    self.ensureCursorVisible()
            case "never":
                scrollbar.setValue(prev_val)

    def text(self) -> str:
        return self.toPlainText()

    def set_read_only(self, value: bool = True) -> None:
        self.setReadOnly(value)

    def set_text_color(self, color: datatypes.ColorType) -> None:
        color = colors.get_color(color)
        self.setTextColor(color)

    def set_line_wrap_mode(self, mode: LineWrapModeStr | widgets.QTextEdit.LineWrapMode):
        """Set line wrap mode.

        Args:
            mode: line wrap mode to use
        """
        self.setLineWrapMode(LINE_WRAP_MODE.get_enum_value(mode))

    def get_line_wrap_mode(self) -> LineWrapModeStr:
        """Get the current wrap mode.

        Returns:
            Wrap mode
        """
        return LINE_WRAP_MODE.inverse[self.lineWrapMode()]

    def set_auto_formatting(
        self, mode: AutoFormattingStr | widgets.QTextEdit.AutoFormattingFlag
    ):
        """Set auto formatting mode.

        Args:
            mode: auto formatting mode to use
        """
        self.setAutoFormatting(AUTO_FORMATTING.get_enum_value(mode))

    def get_auto_formatting(self) -> AutoFormattingStr:
        """Get the current auto formatting mode.

        Returns:
            Auto formatting mode
        """
        return AUTO_FORMATTING.inverse[self.autoFormatting()]

    def set_word_wrap_mode(
        self, mode: gui.textoption.WordWrapModeStr | gui.QTextOption.WrapMode
    ):
        """Set word wrap mode.

        Args:
            mode: word wrap mode to use
        """
        self.setWordWrapMode(gui.textoption.WORD_WRAP_MODE.get_enum_value(mode))

    def get_word_wrap_mode(self) -> gui.textoption.WordWrapModeStr:
        """Get the current word wrap mode.

        Returns:
            Word wrap mode
        """
        return gui.textoption.WORD_WRAP_MODE.inverse[self.wordWrapMode()]


class TextEdit(TextEditMixin, widgets.QTextEdit):
    """Widget that is used to edit and display both plain and rich text."""


if __name__ == "__main__":
    app = widgets.app()
    widget = TextEdit("This is a test")
    widget.show()
    app.exec()

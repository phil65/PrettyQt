from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, syntaxhighlighters, widgets
from prettyqt.utils import bidict, classhelpers, colors, datatypes, texteditselecter


LINE_WRAP_MODE = bidict(
    none=widgets.QPlainTextEdit.LineWrapMode.NoWrap,
    widget_width=widgets.QPlainTextEdit.LineWrapMode.WidgetWidth,
)

LineWrapModeStr = Literal["none", "widget_width"]


class PlainTextEditMixin(widgets.AbstractScrollAreaMixin):
    value_changed = core.Signal(str)

    def __init__(self, text: str = "", **kwargs):
        super().__init__(**kwargs)
        self._allow_wheel_zoom = False
        self._hl = None
        self._current_line_color = gui.Color(0, 0, 0, 0)
        self.selecter = texteditselecter.TextEditSelecter(self)
        self.validator: gui.QValidator | None = None
        self.textChanged.connect(self._on_value_change)
        doc = gui.TextDocument(self)
        layout = widgets.PlainTextDocumentLayout(doc)
        doc.setDocumentLayout(layout)
        self.setDocument(doc)
        self.set_text(text)

    def __add__(self, other: str):
        self.append_text(other)
        return self

    def wheelEvent(self, event):
        """Handle wheel event for zooming."""
        if not self._allow_wheel_zoom:
            return super().wheelEvent(event)
        if event.modifiers() & constants.CTRL_MOD:
            self.zoomIn() if event.angleDelta().y() > 0 else self.zoomOut()
            event.accept()
        else:
            super().wheelEvent(event)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "lineWrapMode": LINE_WRAP_MODE,
            "wordWrapMode": gui.textoption.WORD_WRAP_MODE,
        }
        return maps

    def allow_wheel_zoom(self, do_zoom: bool = True):
        self._allow_wheel_zoom = do_zoom

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
            self.appendPlainText(text)
        else:
            self.selecter.move_cursor("end")
            self.insertPlainText(text)
            self.selecter.move_cursor("end")
        match ensure_visible:
            case "always":
                self.ensureCursorVisible()
            case "when_bottom":
                if at_bottom:
                    self.ensureCursorVisible()
            case "never":
                scrollbar.setValue(prev_val)

    def set_text(self, text: str):
        self.setPlainText(text)

    def set_syntaxhighlighter(
        self, syntax: str | gui.QSyntaxHighlighter, style: str | None = None
    ):
        if isinstance(syntax, gui.QSyntaxHighlighter):
            self._hl = syntax
        else:
            self._hl = syntaxhighlighters.PygmentsHighlighter(
                self.document(), syntax, style
            )

    def text(self) -> str:
        return self.toPlainText()

    def set_read_only(self, value: bool = True):
        """Make the PlainTextEdit read-only.

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def show_whitespace_and_tabs(self, show: bool):
        """Set show white spaces flag."""
        doc = self.document()
        options = doc.defaultTextOption()
        flag = gui.QTextOption.Flag.ShowTabsAndSpaces
        if show:
            options.setFlags(options.flags() | flag)  # type: ignore
        else:
            options.setFlags(options.flags() & ~flag)  # type: ignore
        doc.setDefaultTextOption(options)

    def paintEvent(self, event: gui.QPaintEvent):
        if self._current_line_color:
            with gui.Painter(self.viewport()) as painter:
                cursor_rect = self.cursorRect()
                r = core.QRect(0, cursor_rect.top(), self.width(), cursor_rect.height())
                painter.set_pen(None)
                painter.setBrush(gui.Color(self._current_line_color))
                painter.drawRect(r)
        super().paintEvent(event)

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

    def set_line_wrap_mode(
        self, mode: LineWrapModeStr | widgets.QPlainTextEdit.LineWrapMode
    ):
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

    def _on_value_change(self):
        self.value_changed.emit(self.text())
        if self.validator is not None:
            self._set_validation_color()

    def _set_validation_color(self):
        color = None if self.is_valid() else "orange"
        self.set_background_color(color)

    def set_validator(
        self, validator: gui.QValidator | widgets.lineedit.ValidatorStr | None, **kwargs
    ) -> gui.QValidator:
        if isinstance(validator, str):
            ValidatorClass = classhelpers.get_class_for_id(gui.ValidatorMixin, validator)
            validator = ValidatorClass(**kwargs)
        self.validator = validator
        self._set_validation_color()
        return validator

    def set_regex_validator(self, regex: str, flags=0) -> gui.RegularExpressionValidator:
        validator = gui.RegularExpressionValidator(self)
        validator.set_regex(regex, flags)
        self.set_validator(validator)
        return validator

    def is_valid(self) -> bool:
        if self.validator is None:
            return True
        val = self.validator.validate(self.text(), 0)
        return val[0] == self.validator.State.Acceptable

    def set_value(self, value: str):
        self.setPlainText(value)

    def get_value(self) -> str:
        return self.text()

    def set_current_line_color(self, color: datatypes.ColorType):
        if self._current_line_color is None:
            self.cursorPositionChanged.connect(self.selecter._update_on_block_change)
        if color is None:
            self.cursorPositionChanged.disconnect(self.selecter._update_on_block_change)
        self._current_line_color = colors.get_color(color) if color else None

    def get_current_line_color(self) -> gui.Color:
        return self._current_line_color

    current_line_color = core.Property(
        gui.QColor, get_current_line_color, set_current_line_color
    )

    def get_visible_line_span(self) -> tuple[int, int]:
        block = self.firstVisibleBlock()
        start = block.blockNumber()
        page_step = self.v_scrollbar.pageStep()
        end = min(start + page_step, self.blockCount())
        return (start, end)

    def get_pixel_height(self, exact: bool = True) -> int:
        """Returns the pixel height of the text area."""
        widget_margins = self.contentsMargins()
        doc_height = self.document().get_pixel_height(exact=exact)
        return widget_margins.top() + doc_height + widget_margins.bottom()


class PlainTextEdit(PlainTextEditMixin, widgets.QPlainTextEdit):
    pass


if __name__ == "__main__":
    from prettyqt import validators

    val = validators.RegexPatternValidator()
    app = widgets.app()
    widget = widgets.PlainTextEdit("\n".join(f"abc{i}" for i in range(1000)))
    widget.show_whitespace_and_tabs(True)
    # widget.set_validator(val)
    # with widget.current_cursor() as c:
    #     c.select_text(2, 4)
    widget.set_current_line_color(gui.Color(128, 128, 128, 30))
    widget.show()
    app.sleep(2)
    print(widget.get_visible_line_span())
    app.exec()

from __future__ import annotations

import contextlib
from typing import Iterator

from qtpy import QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import colors


QtWidgets.QTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class TextEdit(QtWidgets.QTextEdit):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.on_value_change)

    def serialize_fields(self):
        return dict(text=self.text(), font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: str) -> TextEdit:
        if isinstance(other, str):
            self.append_text(other)
            return self

    def on_value_change(self) -> None:
        self.value_changed.emit(self.text())

    @contextlib.contextmanager
    def create_cursor(self) -> Iterator[gui.TextCursor]:
        cursor = gui.TextCursor(self.document())
        yield cursor
        self.setTextCursor(cursor)

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

    def set_text_color(self, color: colors.ColorType) -> None:
        color = colors.get_color(color)
        self.setTextColor(color)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TextEdit("This is a test")
    widget.show()
    app.main_loop()

from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class TextFrame(gui.TextObjectMixin, QtGui.QTextFrame):
    def __repr__(self):
        return get_repr(self)

    def get_first_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.firstCursorPosition())

    def get_last_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.lastCursorPosition())


if __name__ == "__main__":
    doc = gui.TextDocument()
    frame = TextFrame(doc)

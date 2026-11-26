from typing import TYPE_CHECKING

from prettyqt import gui
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from prettyqt.qt import QtGui

    _TextFrameBase = QtGui.QTextFrame
else:
    _TextFrameBase = object


class TextFrameMixin(gui.TextObjectMixin, _TextFrameBase):
    def __repr__(self):
        return get_repr(self)

    def get_first_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.firstCursorPosition())

    def get_last_cursor_position(self) -> gui.TextCursor:
        return gui.TextCursor(self.lastCursorPosition())


class TextFrame(TextFrameMixin, gui.QTextFrame):
    pass


if __name__ == "__main__":
    doc = gui.TextDocument()
    frame = TextFrame(doc)

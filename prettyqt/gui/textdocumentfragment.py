from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class TextDocumentFragment(QtGui.QTextDocumentFragment):
    def __repr__(self):
        return f"{type(self).__name__}({gui.TextDocument(self.toPlainText())})"

    def __str__(self):
        return self.toPlainText()

    def __bool__(self):
        return not self.isEmpty()

    @classmethod
    def from_plain_text(cls, text: str) -> TextDocumentFragment:
        return cls(cls.fromPlainText(text))


if __name__ == "__main__":
    doc = TextDocumentFragment.from_plain_text("abc")
    print(repr(doc))

from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import types


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

    def write_to_file(
        self,
        path: types.PathType,
        fmt: gui.textdocumentwriter.FormatStr | bytes | QtCore.QByteArray = "plaintext",
    ):
        writer = gui.TextDocumentWriter()
        writer.set_format(fmt)
        writer.set_file_name(path)
        return writer.write(self)


if __name__ == "__main__":
    doc = TextDocumentFragment.from_plain_text("abc")
    print(repr(doc))

from __future__ import annotations

from typing import Self

from prettyqt import gui
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class TextDocumentFragment(gui.QTextDocumentFragment):
    def __repr__(self):
        return get_repr(self, gui.TextDocument(self.toPlainText()))

    def __str__(self):
        return self.toPlainText()

    def __bool__(self):
        return not self.isEmpty()

    @classmethod
    def from_plain_text(cls, text: str) -> Self:
        return cls(cls.fromPlainText(text))

    def write_to_file(
        self,
        path: datatypes.PathType,
        fmt: gui.textdocumentwriter.FormatStr | bytes | QtCore.QByteArray = "plaintext",
    ):
        writer = gui.TextDocumentWriter()
        writer.set_format(fmt)
        writer.set_file_name(path)
        return writer.write(self)


if __name__ == "__main__":
    doc = TextDocumentFragment.from_plain_text("abc")
    print(repr(doc))

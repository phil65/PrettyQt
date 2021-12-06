from __future__ import annotations

import os

from prettyqt.qt import QtCore, QtGui


class TextDocumentWriter(QtGui.QTextDocumentWriter):
    def __repr__(self):
        return f"{type(self).__name__}({self.device()!r}, {self.format()!r})"

    def get_format(self) -> str:
        return bytes(self.format()).decode()

    def set_format(self, fmt: str | bytes | QtCore.QByteArray):
        new = fmt.encode() if isinstance(fmt, str) else fmt
        self.setFormat(new)

    def set_file_name(self, name: os.PathLike | str):
        path = name if isinstance(name, str) else os.fspath(name)
        self.setFileName(path)

    @classmethod
    def get_supported_document_formats(cls) -> list[str]:
        return [bytes(i).decode() for i in cls.supportedDocumentFormats()]


if __name__ == "__main__":
    doc = TextDocumentWriter("a.text", b"UTF-8")
    doc.set_format("UTF-8")
    print(doc.get_format())

from __future__ import annotations

import os
from typing import Literal

from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import types


FormatStr = Literal["plaintext", "HTML", "markdown", "ODF"]


class TextDocumentWriter(QtGui.QTextDocumentWriter):
    def __repr__(self):
        return f"{type(self).__name__}({self.device()!r}, {self.format()!r})"

    def get_format(self) -> FormatStr:
        return bytes(self.format()).decode()  # type: ignore

    def set_format(self, fmt: FormatStr | bytes | QtCore.QByteArray):
        new = fmt.encode() if isinstance(fmt, str) else fmt
        self.setFormat(new)

    def set_file_name(self, name: types.PathType):
        path = name if isinstance(name, str) else os.fspath(name)
        self.setFileName(path)

    @classmethod
    def get_supported_document_formats(cls) -> list[str]:
        return [bytes(i).decode() for i in cls.supportedDocumentFormats()]


if __name__ == "__main__":
    doc = TextDocumentWriter("a.text", b"plaintext")
    doc.set_format("UTF-8")
    print(doc.get_format())

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


FormatStr = Literal["plaintext", "HTML", "markdown", "ODF"]


class TextDocumentWriter(QtGui.QTextDocumentWriter):
    def __repr__(self):
        return get_repr(self, self.device(), self.format())

    def get_format(self) -> FormatStr:
        return self.format().data().decode()  # type: ignore

    def set_format(self, fmt: FormatStr | bytes | core.QByteArray):
        new = fmt.encode() if isinstance(fmt, str) else fmt
        self.setFormat(new)

    def set_file_name(self, name: datatypes.PathType):
        path = name if isinstance(name, str) else os.fspath(name)
        self.setFileName(path)

    @classmethod
    def get_supported_document_formats(cls) -> list[str]:
        return [i.data().decode() for i in cls.supportedDocumentFormats()]

    @classmethod
    def serialize_document(
        cls,
        document: QtGui.QTextDocument,
        fmt: FormatStr | bytes | core.QByteArray = "ODF",
    ) -> bytes:
        buffer = core.Buffer()
        writer = cls()
        writer.setDevice(buffer)
        writer.set_format(fmt)  # ODF Format
        writer.write(document)
        return buffer.data().data()


if __name__ == "__main__":
    doc = TextDocumentWriter("a.text", b"plaintext")
    doc.set_format("UTF-8")

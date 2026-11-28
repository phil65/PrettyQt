import contextlib
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


ErrorStr = Literal["none", "io", "encoding", "invalid_character", "custom"]

ERROR: bidict[ErrorStr, QtCore.QXmlStreamWriter.Error] = bidict(
    none=QtCore.QXmlStreamWriter.Error.None_,
    io=QtCore.QXmlStreamWriter.Error.IO,
    encoding=QtCore.QXmlStreamWriter.Error.Encoding,
    invalid_character=QtCore.QXmlStreamWriter.Error.InvalidCharacter,
    custom=QtCore.QXmlStreamWriter.Error.Custom,
)


class XmlStreamWriter(QtCore.QXmlStreamWriter):
    """XML writer with a simple streaming API."""

    def get_error(self) -> ErrorStr:
        """Return current writer error status.

        Returns:
            writer error status
        """
        return ERROR.inverse[self.error()]

    @contextlib.contextmanager
    def document(self, version: str | None = None, standalone: bool | None = None):
        """Context manager wrapping writeStartDocument / writeEndDocument."""
        if version is None:
            self.writeStartDocument()
        elif standalone is None:
            self.writeStartDocument(version)
        else:
            self.writeStartDocument(version, standalone)
        try:
            yield self
        finally:
            self.writeEndDocument()

    @contextlib.contextmanager
    def element(self, name: str, namespace_uri: str | None = None):
        """Context manager wrapping writeStartElement / writeEndElement."""
        if namespace_uri is None:
            self.writeStartElement(name)
        else:
            self.writeStartElement(namespace_uri, name)
        try:
            yield self
        finally:
            self.writeEndElement()

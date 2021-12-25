from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


ERROR = bidict(
    none=QtCore.QXmlStreamReader.Error.NoError,
    custom=QtCore.QXmlStreamReader.Error.CustomError,
    not_well_formed=QtCore.QXmlStreamReader.Error.NotWellFormedError,
    premature_end_of_document=QtCore.QXmlStreamReader.Error.PrematureEndOfDocumentError,
    unexpected_element=QtCore.QXmlStreamReader.Error.UnexpectedElementError,
)

FileErrorStr = Literal[
    "none",
    "custom",
    "not_well_formed",
    "premature_end_of_document",
    "unexpected_element",
]


class XmlStreamReader(QtCore.QXmlStreamReader):
    def __iter__(self):
        return self

    def __next__(self):
        while not self.atEnd():
            self.readNext()
            if self.hasError():
                raise RuntimeError(self.get_error())
            return self
        raise StopIteration

    def get_error(self) -> FileErrorStr:
        """Return file error status.

        Returns:
            file error status
        """
        return ERROR.inverse[self.error()]


if __name__ == "__main__":
    reader = XmlStreamReader("<a><b>fdd</b></a>")
    for elem in reader:
        print(elem.text())
    print(reader.get_error())

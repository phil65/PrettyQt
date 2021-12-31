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

TOKEN_TYPE = bidict(
    none=QtCore.QXmlStreamReader.TokenType.NoToken,
    invalid=QtCore.QXmlStreamReader.TokenType.Invalid,
    start_document=QtCore.QXmlStreamReader.TokenType.StartDocument,
    end_document=QtCore.QXmlStreamReader.TokenType.EndDocument,
    start_element=QtCore.QXmlStreamReader.TokenType.StartElement,
    end_element=QtCore.QXmlStreamReader.TokenType.EndElement,
    characters=QtCore.QXmlStreamReader.TokenType.Characters,
    comment=QtCore.QXmlStreamReader.TokenType.Comment,
    dtd=QtCore.QXmlStreamReader.TokenType.DTD,
    entity_reference=QtCore.QXmlStreamReader.TokenType.EntityReference,
    processing_instruction=QtCore.QXmlStreamReader.TokenType.ProcessingInstruction,
)

TokenTypeStr = Literal[
    "none",
    "invalid",
    "start_document",
    "end_document",
    "start_element",
    "end_element",
    "characters",
    "comment",
    "dtd",
    "entity_reference",
    "processing_instruction",
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

    def get_token_type(self) -> TokenTypeStr:
        """Get the current token type.

        Returns:
            token type
        """
        return TOKEN_TYPE.inverse[self.tokenType()]

    def read_next(self) -> TokenTypeStr:
        """Read the next token and returns its type.

        Returns:
            token type
        """
        return TOKEN_TYPE.inverse[self.readNext()]


if __name__ == "__main__":
    reader = XmlStreamReader("<a><b>fdd</b></a>")
    for elem in reader:
        print(elem.text())
    print(reader.get_error())

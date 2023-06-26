from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, datatypes


ContentTypeStr = Literal["mixed", "related", "form", "alternative"]

CONTENT_TYPES: bidict[ContentTypeStr, QtNetwork.QHttpMultiPart.ContentType] = bidict(
    mixed=QtNetwork.QHttpMultiPart.ContentType.MixedType,
    related=QtNetwork.QHttpMultiPart.ContentType.RelatedType,
    form=QtNetwork.QHttpMultiPart.ContentType.FormDataType,
    alternative=QtNetwork.QHttpMultiPart.ContentType.AlternativeType,
)


class HttpMultiPart(core.ObjectMixin, QtNetwork.QHttpMultiPart):
    def __add__(self, other: QtNetwork.QHttpPart):
        self.append(other)
        return self

    def set_content_type(
        self, typ: ContentTypeStr | QtNetwork.QHttpMultiPart.ContentType
    ):
        """Set content type.

        Args:
            typ: content type
        """
        self.setContentType(CONTENT_TYPES.get_enum_value(typ))

    def set_boundary(self, boundary: datatypes.ByteArrayType):
        boundary = datatypes.to_bytearray(boundary)
        self.setBoundary(boundary)

    def get_boundary(self) -> str:
        return self.boundary().data().decode()


if __name__ == "__main__":
    part = HttpMultiPart()
    print(type(part.boundary().data()))

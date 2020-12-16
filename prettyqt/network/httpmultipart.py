from typing import Union

from qtpy import QtCore, QtNetwork

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


CONTENT_TYPES = bidict(
    mixed=QtNetwork.QHttpMultiPart.MixedType,
    related=QtNetwork.QHttpMultiPart.RelatedType,
    form=QtNetwork.QHttpMultiPart.FormDataType,
    alternative=QtNetwork.QHttpMultiPart.AlternativeType,
)

QtNetwork.QHttpMultiPart.__bases__ = (core.Object,)


class HttpMultiPart(QtNetwork.QHttpMultiPart):
    def __add__(self, other: QtNetwork.QHttpPart):
        self.append(other)
        return self

    def set_content_type(self, typ: str):
        """Set content type.

        Valid values: "mixed", "related", "form", "alternative"

        Args:
            typ: content type

        Raises:
            InvalidParamError: content type does not exist
        """
        if typ not in CONTENT_TYPES:
            raise InvalidParamError(typ, CONTENT_TYPES)
        self.setContentType(CONTENT_TYPES[typ])

    def set_boundary(self, boundary: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(boundary, str):
            boundary = boundary.encode()
        if isinstance(boundary, bytes):
            boundary = QtCore.QByteArray(boundary)
        self.setBoundary(boundary)

    def get_boundary(self) -> str:
        return bytes(self.boundary()).decode()


if __name__ == "__main__":
    part = HttpMultiPart()

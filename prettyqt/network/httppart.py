from typing import Any

from prettyqt import network
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class HttpPart(network.QHttpPart):
    """Holds a body part to be used inside a HTTP multipart MIME message."""

    def set_body(self, body: datatypes.ByteArrayType):
        body = datatypes.to_bytearray(body)
        self.setBody(body)

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def set_header(
        self,
        name: network.networkrequest.KnownHeaderStr
        | network.QNetworkRequest.KnownHeaders,
        value: Any,
    ):
        self.setHeader(network.networkrequest.KNOWN_HEADER.get_enum_value(name), value)


if __name__ == "__main__":
    part = HttpPart()

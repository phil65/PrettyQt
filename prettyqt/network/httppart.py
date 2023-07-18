from __future__ import annotations

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

    def set_header(self, name: str, value: network.networkrequest.KnownHeaderStr):
        self.setHeader(network.networkrequest.KNOWN_HEADER[name], value)


if __name__ == "__main__":
    part = HttpPart()

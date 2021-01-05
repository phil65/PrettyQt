from __future__ import annotations

from typing import Dict, Union

from prettyqt import network
from prettyqt.qt import QtCore, QtNetwork


class HttpPart(QtNetwork.QHttpPart):
    def set_body(self, body: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(body, str):
            body = body.encode()
        if isinstance(body, bytes):
            body = QtCore.QByteArray(body)
        self.setBody(body)

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def set_header(self, name: str, value: network.networkrequest.KnownHeaderStr):
        self.setHeader(network.networkrequest.KNOWN_HEADER[name], value)


if __name__ == "__main__":
    part = HttpPart()

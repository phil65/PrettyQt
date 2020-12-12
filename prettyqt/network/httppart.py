from typing import Union, Dict

from qtpy import QtNetwork, QtCore

from prettyqt import network


class HttpPart(QtNetwork.QHttpPart):
    def set_body(self, body: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(body, str):
            body = body.encode()
        if isinstance(body, bytes):
            body = QtCore.QByteArray(body)
        self.setBody(body)

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(k.encode(), v.encode())

    def set_header(self, name: str, value: str):
        self.setHeader(network.networkrequest.KNOWN_HEADERS[name], value)


if __name__ == "__main__":
    part = HttpPart()

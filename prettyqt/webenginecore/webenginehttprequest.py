from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtWebEngineCore
from prettyqt.utils import InvalidParamError, bidict, types


METHODS = bidict(
    get=QtWebEngineCore.QWebEngineHttpRequest.Method.Get,
    post=QtWebEngineCore.QWebEngineHttpRequest.Method.Post,
)

MethodStr = Literal["get", "post"]


class WebEngineHttpRequest(QtWebEngineCore.QWebEngineHttpRequest):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_url()})"

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setHeader(QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode()))

    def get_headers(self) -> dict[str, str]:
        return {bytes(h).decode(): bytes(self.header(h)).decode() for h in self.headers()}

    def set_url(self, url: types.UrlType):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_post_data(self) -> str:
        return bytes(self.postData()).decode()

    def set_method(self, method: MethodStr):
        """Set method this WebEngine request is using.

        Args:
            method: method

        Raises:
            InvalidParamError: method does not exist
        """
        if method not in METHODS:
            raise InvalidParamError(method, METHODS)
        self.setMethod(METHODS[method])

    def get_method(self) -> MethodStr:
        """Get the method this WebEngine request is using.

        Returns:
            method
        """
        return METHODS.inverse[self.method()]


if __name__ == "__main__":
    request = WebEngineHttpRequest()
    request.set_headers(dict(a="b"))
    print(request.get_headers())

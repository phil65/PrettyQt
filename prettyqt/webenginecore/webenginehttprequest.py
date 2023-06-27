from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict, datatypes


MethodStr = Literal["get", "post"]

METHODS: bidict[MethodStr, QtWebEngineCore.QWebEngineHttpRequest.Method] = bidict(
    get=QtWebEngineCore.QWebEngineHttpRequest.Method.Get,
    post=QtWebEngineCore.QWebEngineHttpRequest.Method.Post,
)


class WebEngineHttpRequest(QtWebEngineCore.QWebEngineHttpRequest):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_url()})"

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setHeader(core.QByteArray(k.encode()), core.QByteArray(v.encode()))

    def get_headers(self) -> dict[str, str]:
        return {h.data().decode(): self.header(h).data().decode() for h in self.headers()}

    def set_url(self, url: datatypes.UrlType):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_post_data(self) -> str:
        return self.postData().data().decode()

    def set_method(
        self, method: MethodStr | QtWebEngineCore.QWebEngineHttpRequest.Method
    ):
        """Set method this WebEngine request is using.

        Args:
            method: method
        """
        self.setMethod(METHODS.get_enum_value(method))

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

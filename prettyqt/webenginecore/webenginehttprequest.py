from typing import Dict, Literal, Union

from qtpy import PYQT5, PYSIDE2, QtCore


if PYQT5:
    from PyQt5 import QtWebEngineCore  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


METHODS = bidict(
    get=QtWebEngineCore.QWebEngineHttpRequest.Get,
    post=QtWebEngineCore.QWebEngineHttpRequest.Post,
)

MethodStr = Literal["get", "post"]


class WebEngineHttpRequest(QtWebEngineCore.QWebEngineHttpRequest):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_url()})"

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setHeader(k.encode(), v.encode())

    def get_headers(self) -> Dict[str, str]:
        return {bytes(h).decode(): bytes(self.header(h)).decode() for h in self.headers()}

    def set_url(self, url: Union[str, QtCore.QUrl]):
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

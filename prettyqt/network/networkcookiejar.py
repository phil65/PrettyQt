from __future__ import annotations

from collections.abc import Iterator

from prettyqt import core
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import types


QtNetwork.QNetworkCookieJar.__bases__ = (core.Object,)


class NetworkCookieJar(QtNetwork.QNetworkCookieJar):
    def __add__(self, other: QtNetwork.QNetworkCookie):
        self.insertCookie(other)
        return self

    def __getitem__(self, url: str) -> list[QtNetwork.QNetworkCookie]:
        url = core.Url(url)
        return self.cookiesForUrl(url)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __iter__(self) -> Iterator[QtNetwork.QNetworkCookie]:
        return iter(self.allCookies())

    def set_cookies_from_url(
        self, cookies: list[QtNetwork.QNetworkCookie], url: types.UrlType
    ) -> bool:
        return self.setCookiesFromUrl(cookies, QtCore.QUrl(url))

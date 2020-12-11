from typing import List, Iterator, Union

from qtpy import QtNetwork, QtCore

from prettyqt import core


QtNetwork.QNetworkCookieJar.__bases__ = (core.Object,)


class NetworkCookieJar(QtNetwork.QNetworkCookieJar):
    def __add__(self, other: QtNetwork.QNetworkCookie):
        self.insertCookie(other)
        return self

    def __getitem__(self, url: str) -> List[QtNetwork.QNetworkCookie]:
        url = core.Url(url)
        return self.cookiesForUrl(url)

    def __repr__(self):
        return "NetworkCookieJar()"

    def __iter__(self) -> Iterator[QtNetwork.QNetworkCookie]:
        return iter(self.allCookies())

    def set_cookies_from_url(
        self, cookies: List[QtNetwork.QNetworkCookie], url: Union[QtCore.QUrl, str]
    ) -> bool:
        return self.setCookiesFromUrl(cookies, QtCore.QUrl(url))

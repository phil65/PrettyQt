from __future__ import annotations

from collections.abc import Iterator

from prettyqt import core
from prettyqt.qt import QtNetwork
from prettyqt.utils import datatypes, get_repr


class NetworkCookieJar(core.ObjectMixin, QtNetwork.QNetworkCookieJar):
    """Implements a simple jar of QNetworkCookie objects."""

    def __add__(self, other: QtNetwork.QNetworkCookie):
        self.insertCookie(other)
        return self

    def __getitem__(self, url: datatypes.UrlType) -> list[QtNetwork.QNetworkCookie]:
        url = core.Url(url)
        return self.cookiesForUrl(url)

    def __repr__(self):
        return get_repr(self)

    def __iter__(self) -> Iterator[QtNetwork.QNetworkCookie]:
        return iter(self.allCookies())

    def set_cookies_from_url(
        self, cookies: list[QtNetwork.QNetworkCookie], url: datatypes.UrlType
    ) -> bool:
        return self.setCookiesFromUrl(cookies, core.QUrl(url))


if __name__ == "__main__":
    jar = NetworkCookieJar()

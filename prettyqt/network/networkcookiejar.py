# -*- coding: utf-8 -*-

from qtpy import QtNetwork

from prettyqt import core


QtNetwork.QNetworkCookieJar.__bases__ = (core.Object,)


class NetworkCookieJar(QtNetwork.QNetworkCookieJar):
    def __getitem__(self, url: str) -> list:
        url = core.Url(url)
        return self.cookiesForUrl(url)

    def __repr__(self):
        return "NetworkCookieJar()"

    def __iter__(self):
        return iter(self.allCookies())

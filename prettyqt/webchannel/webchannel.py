from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWebChannel


QtWebChannel.QWebChannel.__bases__ = (core.Object,)


class WebChannel(QtWebChannel.QWebChannel):
    pass


if __name__ == "__main__":
    channel = WebChannel()

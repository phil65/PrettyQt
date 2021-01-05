from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWebEngineCore


QtWebEngineCore.QWebEngineUrlSchemeHandler.__bases__ = (core.Object,)


class WebEngineUrlSchemeHandler(QtWebEngineCore.QWebEngineUrlSchemeHandler):
    pass


if __name__ == "__main__":
    item = WebEngineUrlSchemeHandler()

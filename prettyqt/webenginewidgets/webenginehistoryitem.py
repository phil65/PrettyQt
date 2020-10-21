# -*- coding: utf-8 -*-

try:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
except ImportError:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core


class WebEngineHistoryItem(QtWebEngineWidgets.QWebEngineHistoryItem):
    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_last_visited(self) -> core.DateTime:
        return core.DateTime(self.lastVisited())


if __name__ == "__main__":
    item = WebEngineHistoryItem()

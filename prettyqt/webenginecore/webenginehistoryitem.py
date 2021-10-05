from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWebEngineCore


class WebEngineHistoryItem(QtWebEngineCore.QWebEngineHistoryItem):
    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_icon_url(self) -> core.Url:
        return core.Url(self.iconUrl())

    def get_last_visited(self) -> core.DateTime:
        return core.DateTime(self.lastVisited())

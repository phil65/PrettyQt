from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core


class WebEngineHistoryItem(QtWebEngineWidgets.QWebEngineHistoryItem):
    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_icon_url(self) -> core.Url:
        return core.Url(self.iconUrl())

    def get_last_visited(self) -> core.DateTime:
        return core.DateTime(self.lastVisited())

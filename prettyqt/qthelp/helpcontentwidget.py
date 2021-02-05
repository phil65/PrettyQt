from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtHelp


QtHelp.QHelpContentWidget.__bases__ = (widgets.TreeView,)


class HelpContentWidget(QtHelp.QHelpContentWidget):
    def index_of(self, url: QtCore.QUrl | str) -> QtCore.QModelIndex | None:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        idx = self.indexOf(url)
        if not idx.isValid():
            return None
        return idx

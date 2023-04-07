from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtHelp
from prettyqt.utils import types


class HelpContentWidget(widgets.TreeViewMixin, QtHelp.QHelpContentWidget):
    def index_of(self, url: types.UrlType) -> QtCore.QModelIndex | None:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        idx = self.indexOf(url)
        if not idx.isValid():
            return None
        return idx

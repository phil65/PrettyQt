from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtHelp
from prettyqt.utils import datatypes


class HelpContentWidget(widgets.TreeViewMixin, QtHelp.QHelpContentWidget):
    """Tree view for displaying help content model items."""

    def index_of(self, url: datatypes.UrlType) -> QtCore.QModelIndex | None:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        idx = self.indexOf(url)
        return idx if idx.isValid() else None

    @classmethod
    def setup_example(cls):
        return None

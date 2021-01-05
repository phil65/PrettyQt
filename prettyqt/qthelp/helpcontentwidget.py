from __future__ import annotations

from typing import Optional, Union

from prettyqt import widgets
from prettyqt.qt import QtCore, QtHelp


QtHelp.QHelpContentWidget.__bases__ = (widgets.TreeView,)


class HelpContentWidget(QtHelp.QHelpContentWidget):
    def index_of(self, url: Union[QtCore.QUrl, str]) -> Optional[QtCore.QModelIndex]:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        idx = self.indexOf(url)
        if not idx.isValid():
            return None
        return idx

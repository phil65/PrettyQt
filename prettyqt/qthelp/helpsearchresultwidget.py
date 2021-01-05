from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtHelp


QtHelp.QHelpSearchResultWidget.__bases__ = (widgets.Widget,)


class HelpSearchResultWidget(QtHelp.QHelpSearchResultWidget):
    def get_link_at(self, point: QtCore.QPoint) -> core.Url:
        return core.Url(self.linkAt(point))

from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtHelp
from prettyqt.utils import types


QtHelp.QHelpSearchResultWidget.__bases__ = (widgets.Widget,)


class HelpSearchResultWidget(QtHelp.QHelpSearchResultWidget):
    def get_link_at(self, point: types.PointType) -> core.Url:
        if isinstance(point, tuple):
            point = core.Point(*point)
        return core.Url(self.linkAt(point))

from qtpy import QtCore, QtHelp

from prettyqt import core, widgets


QtHelp.QHelpSearchResultWidget.__bases__ = (widgets.Widget,)


class HelpSearchResultWidget(QtHelp.QHelpSearchResultWidget):
    def get_link_at(self, point: QtCore.QPoint) -> core.Url:
        return core.Url(self.linkAt(point))

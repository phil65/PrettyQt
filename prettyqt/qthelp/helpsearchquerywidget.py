from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


QtHelp.QHelpSearchQueryWidget.__bases__ = (widgets.Widget,)


class HelpSearchQueryWidget(QtHelp.QHelpSearchQueryWidget):
    pass

from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


QtHelp.QHelpIndexWidget.__bases__ = (widgets.ListView,)


class HelpIndexWidget(QtHelp.QHelpIndexWidget):
    pass

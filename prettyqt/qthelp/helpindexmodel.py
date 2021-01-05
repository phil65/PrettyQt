from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


QtHelp.QHelpIndexModel.__bases__ = (core.StringListModel,)


class HelpIndexModel(QtHelp.QHelpIndexModel):
    pass

from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


QtHelp.QHelpContentModel.__bases__ = (core.AbstractItemModel,)


class HelpContentModel(QtHelp.QHelpContentModel):
    pass

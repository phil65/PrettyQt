from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpIndexModel(core.StringListModelMixin, QtHelp.QHelpIndexModel):
    pass

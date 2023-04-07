from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpContentModel(core.AbstractItemModelMixin, QtHelp.QHelpContentModel):
    pass

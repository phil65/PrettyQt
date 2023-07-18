from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpIndexModel(core.StringListModelMixin, QtHelp.QHelpIndexModel):
    """Model that supplies index keywords to views."""

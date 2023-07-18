from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


class HelpSearchQueryWidget(widgets.WidgetMixin, QtHelp.QHelpSearchQueryWidget):
    """Widget to enable the user to input a search term in a standardized input mask."""

from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


class HelpIndexWidget(widgets.ListViewMixin, QtHelp.QHelpIndexWidget):
    @classmethod
    def setup_example(cls):
        return None

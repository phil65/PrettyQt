from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpContentItem(QtHelp.QHelpContentItem):
    def __len__(self):
        return self.childCount()

    def get_url(self) -> core.Url:
        return core.Url(self.url())

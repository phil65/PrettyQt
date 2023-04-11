from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpContentItem:
    def __init__(self, item: QtHelp.QHelpContentItem):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __len__(self):
        return self.childCount()

    def get_url(self) -> core.Url:
        return core.Url(self.url())

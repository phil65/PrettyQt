from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpLink:
    """Struct provides the data associated with a help link."""

    def __init__(self, item: QtHelp.QHelpLink):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_url(self) -> core.Url:
        return core.Url(self.url)

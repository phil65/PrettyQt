from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt.qt import QtHelp


class HelpLink:
    """Struct provides the data associated with a help link."""

    def __init__(self, item: QtHelp.QHelpLink):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_url(self) -> core.Url:
        return core.Url(self.url)

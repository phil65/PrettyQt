from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt.qt import QtHelp


class HelpContentItem:
    """Item for use with QHelpContentModel."""

    def __init__(self, item: QtHelp.QHelpContentItem):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __len__(self):
        return self.childCount()

    def get_url(self) -> core.Url:
        return core.Url(self.url())

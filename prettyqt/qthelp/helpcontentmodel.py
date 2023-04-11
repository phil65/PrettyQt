from __future__ import annotations

from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


class HelpContentModel(core.AbstractItemModelMixin):
    def __init__(self, item: QtHelp.QHelpContentModel):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_content_item_at(self, index) -> qthelp.HelpContentItem:
        return qthelp.HelpContentItem(self.contentItemAt(index))

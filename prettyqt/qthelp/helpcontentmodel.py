from __future__ import annotations

from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


class HelpContentModel(core.AbstractItemModelMixin, QtHelp.QHelpContentModel):
    def get_content_item_at(self, index) -> qthelp.HelpContentItem:
        return qthelp.HelpContentItem(self.contentItemAt(index))


if __name__ == "__main__":
    model = HelpContentModel("test")

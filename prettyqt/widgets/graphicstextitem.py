from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsTextItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    def __repr__(self):
        return f"{type(self).__name__}({self.toPlainText()!r})"

    def serialize_fields(self):
        return dict(
            open_external_links=self.openExternalLinks(),
            text_width=self.textWidth(),
            plain_text=self.toPlainText(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setOpenExternalLinks(state["open_external_links"])
        self.setTextWidth(state["text_width"])
        self.setPlainText(state["plain_text"])

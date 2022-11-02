from __future__ import annotations

from collections.abc import Iterator

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsLayout.__bases__ = (widgets.GraphicsLayoutItem,)


class GraphicsLayout(QtWidgets.QGraphicsLayout):
    def __getitem__(self, index: int) -> QtWidgets.QGraphicsItem:
        layoutitem = self.itemAt(index)
        return layoutitem.graphicsItem()

    def __setitem__(self, index: int, value: QtWidgets.QGraphicsItem):
        layoutitem = self.itemAt(index)
        layoutitem.setGraphicsItem(value)

    def __delitem__(self, index: int):
        self.removeAt(index)

    def __iter__(self) -> Iterator[QtWidgets.QGraphicsItem]:
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item):
        return item in self.get_children()

    def __len__(self):
        # for PySide2
        return self.count()

    def get_children(self) -> list[QtWidgets.QGraphicsItem]:
        return list(self)

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)


if __name__ == "__main__":
    layout = GraphicsLayout()

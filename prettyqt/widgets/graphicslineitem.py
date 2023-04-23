from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class GraphicsLineItem(widgets.GraphicsItemMixin, QtWidgets.QGraphicsLineItem):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_line())})"

    def get_line(self) -> core.LineF:
        return core.LineF(self.line())


if __name__ == "__main__":
    item = GraphicsLineItem(core.Point(0, 0), core.Point(2, 2))
    print(repr(item))

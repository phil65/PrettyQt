from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QGraphicsLineItem.__bases__ = (widgets.GraphicsItem,)


class GraphicsLineItem(QtWidgets.QGraphicsLineItem):
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.get_line())})"

    def serialize_fields(self):
        return dict(line=self.get_line())

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setLine(state["line"])

    def get_line(self) -> core.Line:
        return core.LineF(self.line())


if __name__ == "__main__":
    item = GraphicsLineItem(core.Point(0, 0), core.Point(2, 2))
    print(repr(item))

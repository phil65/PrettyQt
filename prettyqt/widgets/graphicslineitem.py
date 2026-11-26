from prettyqt import core, widgets
from prettyqt.utils import get_repr


class GraphicsLineItem(widgets.GraphicsItemMixin, widgets.QGraphicsLineItem):
    """Line item that you can add to a QGraphicsScene."""

    def __repr__(self):
        return get_repr(self, self.get_line())

    def get_line(self) -> core.LineF:
        return core.LineF(self.line())


if __name__ == "__main__":
    item = GraphicsLineItem(core.LineF(0, 0, 2, 2))

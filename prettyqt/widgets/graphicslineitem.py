from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QGraphicsLineItem.__bases__ = (widgets.GraphicsItem,)


class GraphicsLineItem(QtWidgets.QGraphicsLineItem):
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.get_line())})"

    def get_line(self):
        return core.LineF(self.line())


if __name__ == "__main__":
    item = GraphicsLineItem(core.Point(0, 0), core.Point(2, 2))
    print(repr(item))

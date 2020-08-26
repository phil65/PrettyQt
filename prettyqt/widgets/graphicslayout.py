from qtpy import QtWidgets

from prettyqt import widgets

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

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item):
        return item in self.get_children()

    def get_children(self) -> list:
        return list(self)


if __name__ == "__main__":
    layout = GraphicsLayout()

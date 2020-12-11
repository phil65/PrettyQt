from qtpy import QtWidgets


class GraphicsLayoutItem(QtWidgets.QGraphicsLayoutItem):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

from qtpy import QtWidgets

from prettyqt import widgets

QtWidgets.QGraphicsLayout.__bases__ = (widgets.GraphicsLayoutItem,)


class GraphicsLayout(QtWidgets.QGraphicsLayout):
    pass

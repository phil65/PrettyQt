from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsProxyWidget.__bases__ = (widgets.GraphicsWidget,)


class GraphicsProxyWidget(QtWidgets.QGraphicsProxyWidget):

    pass

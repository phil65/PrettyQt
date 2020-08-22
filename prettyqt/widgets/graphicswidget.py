# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsWidget.__bases__ = (widgets.GraphicsObject, widgets.GraphicsLayoutItem)


class GraphicsWidget(QtWidgets.QGraphicsWidget):

    pass

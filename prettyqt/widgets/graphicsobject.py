# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QGraphicsObject.__bases__ = (core.Object, widgets.GraphicsItem)


class GraphicsObject(QtWidgets.QGraphicsObject):

    pass

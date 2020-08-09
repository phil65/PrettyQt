# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsOpacityEffect.__bases__ = (widgets.GraphicsEffect,)


class GraphicsOpacityEffect(QtWidgets.QGraphicsOpacityEffect):

    pass

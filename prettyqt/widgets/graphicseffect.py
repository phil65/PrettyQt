# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QGraphicsEffect.__bases__ = (core.Object,)


class GraphicsEffect(QtWidgets.QGraphicsEffect):

    pass

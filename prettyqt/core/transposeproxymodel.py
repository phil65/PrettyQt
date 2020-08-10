# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


QtCore.QTransposeProxyModel.__bases__ = (core.AbstractProxyModel,)


class TransposeProxyModel(QtCore.QTransposeProxyModel):
    pass

# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractProxyModel.__bases__ = (core.AbstractItemModel,)


class AbstractProxyModel(QtCore.QAbstractProxyModel):
    pass

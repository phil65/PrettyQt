# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class AbstractProxyModel(QtCore.QAbstractProxyModel):
    pass


AbstractProxyModel.__bases__[0].__bases__ = (core.AbstractItemModel,)

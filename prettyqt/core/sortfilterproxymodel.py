# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class SortFilterProxyModel(QtCore.QSortFilterProxyModel):

    HEADER = []


SortFilterProxyModel.__bases__[0].__bases__ = (core.AbstractProxyModel,)

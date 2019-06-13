# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QSortFilterProxyModel.__bases__ = (core.AbstractProxyModel,)


class SortFilterProxyModel(QtCore.QSortFilterProxyModel):

    HEADER = []

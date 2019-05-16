# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


class AbstractTableModel(QtCore.QAbstractTableModel):
    pass


AbstractTableModel.__bases__[0].__bases__ = (core.AbstractItemModel,)

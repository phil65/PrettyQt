# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractTableModel.__bases__ = (core.AbstractItemModel,)


class AbstractTableModel(QtCore.QAbstractTableModel):
    pass

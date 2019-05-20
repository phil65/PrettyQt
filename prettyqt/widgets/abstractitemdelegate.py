# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import core


class AbstractItemDelegate(QtWidgets.QAbstractItemDelegate):
    pass


AbstractItemDelegate.__bases__[0].__bases__ = (core.Object,)

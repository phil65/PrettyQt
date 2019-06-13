# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import core


QtWidgets.QAbstractItemDelegate.__bases__ = (core.Object,)


class AbstractItemDelegate(QtWidgets.QAbstractItemDelegate):
    pass

# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class ItemDelegate(QtWidgets.QItemDelegate):
    pass


ItemDelegate.__bases__[0].__bases__ = (widgets.AbstractItemDelegate,)

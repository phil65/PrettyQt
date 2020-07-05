# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QItemDelegate.__bases__ = (widgets.AbstractItemDelegate,)


class ItemDelegate(QtWidgets.QItemDelegate):
    pass

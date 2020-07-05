# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QAbstractListModel.__bases__ = (core.AbstractItemModel,)


class AbstractListModel(QtCore.QAbstractListModel):
    pass

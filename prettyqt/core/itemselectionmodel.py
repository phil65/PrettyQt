# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QItemSelectionModel.__bases__ = (core.Object,)


class ItemSelectionModel(QtCore.QItemSelectionModel):
    pass

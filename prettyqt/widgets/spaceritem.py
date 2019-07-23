# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QSpacerItem.__bases__ = (widgets.LayoutItem,)


class SpacerItem(QtWidgets.QSpacerItem):
    pass

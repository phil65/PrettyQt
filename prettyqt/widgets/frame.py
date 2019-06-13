# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QFrame.__bases__ = (widgets.Widget,)


class Frame(QtWidgets.QFrame):
    pass

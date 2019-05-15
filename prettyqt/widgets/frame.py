# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class Frame(QtWidgets.QFrame):
    pass


Frame.__bases__[0].__bases__ = (widgets.Widget,)

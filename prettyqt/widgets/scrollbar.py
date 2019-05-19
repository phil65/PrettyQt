# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, core


class ScrollBar(QtWidgets.QScrollBar):
    value_changed = core.Signal(int)


ScrollBar.__bases__[0].__bases__ = (widgets.AbstractSlider,)

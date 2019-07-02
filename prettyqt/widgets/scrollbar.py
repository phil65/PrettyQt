# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, core
from prettyqt.utils import bidict

ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal,
                      vertical=QtCore.Qt.Vertical)


QtWidgets.QScrollBar.__bases__ = (widgets.AbstractSlider,)


class ScrollBar(QtWidgets.QScrollBar):

    value_changed = core.Signal(int)

    def __init__(self, orientation="horizontal", parent=None):
        super().__init__(ORIENTATIONS[orientation], parent)
        self.valueChanged.connect(self.on_value_change)

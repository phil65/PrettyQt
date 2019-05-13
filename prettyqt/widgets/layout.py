# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class Layout(QtWidgets.QLayout):

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

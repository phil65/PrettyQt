# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets


class ButtonGroup(QtWidgets.QButtonGroup):
    def __getitem__(self, index):
        return self.button(index)

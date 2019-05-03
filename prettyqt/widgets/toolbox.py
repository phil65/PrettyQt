# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class ToolBox(QtWidgets.QToolBox):

    def __getitem__(self, index):
        return self.widget(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __len__(self):
        return self.count()

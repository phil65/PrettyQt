# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


class StandardItemModel(QtGui.QStandardItemModel):

    def __iter__(self):
        items = [self.item(index) for index in range(self.rowCount())]
        return iter(items)

    def add_item(self, label):
        item = gui.StandardItem(label)
        self.appendRow(item)

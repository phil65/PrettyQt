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

    def __add__(self, other):
        if isinstance(other, QtGui.QStandardItem):
            self.appendRow(other)
            return self

    def add_item(self, label):
        item = gui.StandardItem(label)
        self.appendRow(item)

# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore


class ModelIndex(QtCore.QModelIndex):
    def __getitem__(self, flag):
        return self.data(flag)

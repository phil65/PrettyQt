# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class Dir(QtCore.QDir):

    def __str__(self):
        return self.absolutePath()

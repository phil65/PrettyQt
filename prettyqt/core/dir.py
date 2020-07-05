# -*- coding: utf-8 -*-
"""
"""

import pathlib

from qtpy import QtCore


class Dir(QtCore.QDir):

    def __str__(self):
        return self.absolutePath()

    def to_path(self):
        return pathlib.Path(self.absolutePath())

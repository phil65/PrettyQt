# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


QtGui.QPicture.__bases__ = (gui.PaintDevice,)


class Picture(QtGui.QPicture):
    pass

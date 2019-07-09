# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import gui


QtGui.QImage.__bases__ = (gui.PaintDevice,)


class Image(QtGui.QImage):
    pass


if __name__ == "__main__":
    image = Image()

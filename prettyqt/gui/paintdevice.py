# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui


class PaintDevice(QtGui.QPaintDevice):
    pass


if __name__ == "__main__":
    device = PaintDevice()

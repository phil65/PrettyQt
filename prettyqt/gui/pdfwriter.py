# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore

from prettyqt import core, widgets


class PdfWriter(QtGui.QPdfWriter):

    def setup(self, size):
        dpi = widgets.DesktopWidget().logicalDpiX()
        self.setResolution(dpi)
        self.setPageMargins(QtCore.QMarginsF(0, 0, 0, 0))
        self.setPageSizeMM(core.SizeF(size.width(), size.height()) / dpi * 25.4)

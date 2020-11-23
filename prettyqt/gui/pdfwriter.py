# -*- coding: utf-8 -*-

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core


class PdfWriter(QtGui.QPdfWriter):
    def setup(self, size: QtCore.QSize):
        dpi = QtWidgets.QDesktopWidget().logicalDpiX()
        self.setResolution(dpi)
        self.setPageMargins(QtCore.QMarginsF(0, 0, 0, 0))
        self.setPageSizeMM(core.SizeF(size.width(), size.height()) / dpi * 25.4)

# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core, gui, widgets


class PdfWriter(QtGui.QPdfWriter):

    def setup(self, size):
        dpi = widgets.DesktopWidget().logicalDpiX()
        self.setResolution(dpi)
        self.setPageMargins(core.MarginsF(0, 0, 0, 0))
        self.setPageSizeMM(core.SizeF(size.width(), size.height()) / dpi * 25.4)

    def testus(self):
        self.setup(self.getTargetRect().size())
        painter = gui.Painter(self)
        try:
            dct = dict(antialias=True,
                       background=self.background,
                       painter=painter)
            self.setExportMode(True, dct)
            painter.use_antialiasing()
            self.getScene().render(painter,
                                   core.RectF(self.getTargetRect()),
                                   core.RectF(self.getSourceRect()))
        finally:
            self.setExportMode(False)
        painter.end()

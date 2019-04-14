# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import gui


class SplashScreen(QtWidgets.QSplashScreen):

    def __init__(self, path, width=None):
        pix = gui.Pixmap(str(path))
        if width:
            pix = pix.scaledToWidth(width)
        super().__init__(pix)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint)
        self.setEnabled(False)

    def __enter__(self):
        self.show()
        return self

    def __exit__(self, typ, value, traceback):
        self.hide()

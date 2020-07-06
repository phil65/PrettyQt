# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import bidict


H_ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    center=QtCore.Qt.AlignHCenter,
    justify=QtCore.Qt.AlignJustify,
)

V_ALIGNMENTS = bidict(
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
    center=QtCore.Qt.AlignVCenter,
    baseline=QtCore.Qt.AlignBaseline,
)


QtWidgets.QSplashScreen.__bases__ = (widgets.Widget,)


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, path, width=None):
        pix = gui.Pixmap(str(path))
        if width:
            pix = pix.scaledToWidth(width)
        super().__init__(pix)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setEnabled(False)

    def __enter__(self):
        self.show()
        return self

    def __exit__(self, typ, value, traceback):
        self.hide()

    def set_text(self, text, color="black", h_align="center", v_align="bottom"):
        self.showMessage(
            text,
            color=gui.Color(color),
            alignment=H_ALIGNMENTS[h_align] | V_ALIGNMENTS[v_align],
        )

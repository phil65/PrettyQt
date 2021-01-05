from __future__ import annotations

import os
from typing import Optional, Union

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import types


QtWidgets.QSplashScreen.__bases__ = (widgets.Widget,)


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(
        self, path: Union[os.PathLike, str, QtGui.QPixmap], width: Optional[int] = None
    ):
        pix = gui.Pixmap(os.fspath(path)) if not isinstance(path, QtGui.QPixmap) else path
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

    def set_text(
        self,
        text: str,
        color: types.ColorType = "black",
        h_align: constants.HorizontalAlignmentStr = "center",
        v_align: constants.VerticalAlignmentStr = "bottom",
    ):
        self.showMessage(
            text,
            color=gui.Color(color),
            alignment=constants.H_ALIGNMENT[h_align] | constants.V_ALIGNMENT[v_align],
        )

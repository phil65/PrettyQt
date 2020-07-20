# -*- coding: utf-8 -*-
"""
"""

from typing import Optional
from qtpy import QtWidgets, QtGui, QtCore


class ToolTip(QtWidgets.QToolTip):
    @classmethod
    def show_text(
        cls,
        position: Optional[QtCore.QPoint] = None,
        text: str = "",
        linebreak_px: int = 400,
    ):
        if position is None:
            cursor = QtGui.QCursor()
            position = cursor.pos()
        cls.showText(position, f'<div style="max-width: {linebreak_px}px">{text}</div>')


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    ToolTip.show_text(text="test")
    app.exec_()

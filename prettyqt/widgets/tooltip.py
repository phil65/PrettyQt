from __future__ import annotations

from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import types


class ToolTip(QtWidgets.QToolTip):
    @classmethod
    def show_text(
        cls,
        position: types.PointType | None = None,
        text: str = "",
        linebreak_px: int = 400,
    ):
        if position is None:
            position = QtGui.QCursor.pos()
        elif isinstance(position, tuple):
            position = QtCore.QPoint(*position)
        cls.showText(position, f'<div style="max-width: {linebreak_px}px">{text}</div>')


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    ToolTip.show_text(text="test")
    app.main_loop()

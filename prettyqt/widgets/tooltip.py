from __future__ import annotations

from prettyqt.qt import QtCore, QtGui, QtWidgets


class ToolTip(QtWidgets.QToolTip):
    @classmethod
    def show_text(
        cls,
        position: QtCore.QPoint | None = None,
        text: str = "",
        linebreak_px: int = 400,
    ):
        if position is None:
            position = QtGui.QCursor.pos()
        cls.showText(position, f'<div style="max-width: {linebreak_px}px">{text}</div>')


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    ToolTip.show_text(text="test")
    app.main_loop()

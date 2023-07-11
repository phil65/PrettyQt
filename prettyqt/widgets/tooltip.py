from __future__ import annotations

from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import datatypes


class ToolTip(QtWidgets.QToolTip):
    """Tool tips (balloon help) for any widget."""

    @classmethod
    def show_text(
        cls,
        position: datatypes.PointType | None = None,
        text: str = "",
        linebreak_px: int = 400,
    ):
        cls.showText(
            QtGui.QCursor.pos() if position is None else datatypes.to_point(position),
            f'<div style="max-width: {linebreak_px}px">{text}</div>',
        )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    ToolTip.show_text(text="test")
    app.exec()

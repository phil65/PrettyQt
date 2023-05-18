from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui


class ClickableLabel(widgets.Label):
    """A label widget that behaves like a button."""

    clicked = core.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, alignment="left")
        self.setFont(QtGui.QFont("Arial"))
        self.setFixedHeight(24)
        self.set_size_policy("minimum", "expanding")

    def setText(self, text: str):
        fm = gui.FontMetrics(self.font())
        width = fm.width(text)
        self.setFixedWidth(width + 18)
        super().setText(text)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        return super().mouseReleaseEvent(ev)

    def enterEvent(self, event: QtCore.QEvent):
        with self.edit_font() as font:
            font.setUnderline(True)
        self.set_cursor("pointing_hand")
        self.update()
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent):
        with self.edit_font() as font:
            font.setUnderline(False)
        self.unsetCursor()
        return super().leaveEvent(event)


if __name__ == "__main__":
    app = widgets.app()
    widget = ClickableLabel("test", tool_tip="testus")
    widget.show()
    app.main_loop()

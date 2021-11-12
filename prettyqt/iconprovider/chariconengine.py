from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtGui


ZERO_COORD = core.Point(0, 0)


class CharIconEngine(gui.IconEngine):
    """Specialization of QtGui.QIconEngine used to draw font-based icons."""

    def __init__(self, iconic, options):
        super().__init__()
        self.iconic = iconic
        self.options = options

    def paint(self, painter: QtGui.QPainter, rect: QtCore.QRect, mode, state):
        self.iconic.paint(painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state) -> QtGui.QPixmap:
        pm = QtGui.QPixmap(size)
        pm.fill(QtCore.Qt.GlobalColor.transparent)  # type: ignore
        rect = core.Rect(ZERO_COORD, size)
        painter = gui.Painter(pm)
        self.paint(painter, rect, mode, state)
        return pm

from __future__ import annotations

from prettyqt import constants, core, gui


ZERO_COORD = core.Point(0, 0)


class CharIconEngine(gui.IconEngine):
    """Specialization of gui.QIconEngine used to draw font-based icons."""

    def __init__(self, iconic, options):
        super().__init__()
        self.iconic = iconic
        self.options = options

    def paint(self, painter: gui.QPainter, rect: core.QRect, mode, state):
        self.iconic.paint(painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state) -> gui.QPixmap:
        pm = gui.QPixmap(size)
        pm.fill(constants.GlobalColor.transparent)  # type: ignore
        rect = core.Rect(ZERO_COORD, size)
        with gui.Painter(pm) as painter:
            self.paint(painter, rect, mode, state)
        return pm

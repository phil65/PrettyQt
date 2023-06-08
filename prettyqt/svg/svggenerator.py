from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtSvg


class SvgGenerator(gui.PaintDeviceMixin, QtSvg.QSvgGenerator):
    def get_viewbox(self) -> core.Rect:
        return core.Rect(self.viewBox())

    def get_viewboxf(self) -> core.RectF:
        return core.RectF(self.viewBoxF())

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def set_size(self, size: QtCore.QSize | QtCore.QSizeF | tuple[int, int]):
        match size:
            case (int(), int()):
                new_size = QtCore.QSize(*size)
            case QtCore.QSizeF():
                new_size = size.toSize()
            case QtCore.QSize():
                new_size = size
        self.setSize(new_size)

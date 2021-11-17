from __future__ import annotations

from prettyqt import core, gui, svg
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import colors, types


class SVGBufferIconEngine(gui.IconEngine):
    """A custom QIconEngine that can render an SVG buffer.

    An icon engine provides the rendering functions for a ``QIcon``.
    Each icon has a corresponding icon engine that is responsible for drawing
    the icon with a requested size, mode and state.  While the built-in
    QIconEngine is capable of rendering SVG files, it's not able to receive the
    raw XML string from memory.
    This ``QIconEngine`` takes in SVG data as a raw xml string or bytes.
    see: https://doc.qt.io/qt-5/qiconengine.html
    """

    def __init__(self, xml: str, color: types.ColorType = "black") -> None:
        self._xml = xml
        self._color = colors.get_color(color)
        super().__init__()

    def paint(
        self,
        painter: QtGui.QPainter,
        rect: QtCore.QRect,
        mode: QtGui.QIcon.Mode,
        state: QtGui.QIcon.State,
    ):
        """Paint the icon int ``rect`` using ``painter``."""
        color = self._color
        if mode == QtGui.QIcon.Mode.Disabled:
            color = self._color.transparent(0.3)

        xml = self._xml.replace('fill="currentColor"', color.get_name("svg_argb"))
        xml_byte = xml.encode()
        renderer = svg.SvgRenderer(xml_byte)
        renderer.render(painter, core.RectF(rect))

    def clone(self):
        """Required to subclass abstract QIconEngine."""
        return SVGBufferIconEngine(self._xml, self._color)

    def pixmap(
        self, size: QtCore.QSize, mode: QtGui.QIcon.Mode, state: QtGui.QIcon.State
    ) -> QtGui.QPixmap:
        """Return the icon as a pixmap with requested size, mode, and state."""
        img = gui.Image(size, QtGui.QImage.Format.Format_ARGB32)
        img.fill(QtCore.Qt.GlobalColor.transparent)
        pixmap = QtGui.QPixmap.fromImage(
            img, QtCore.Qt.ImageConversionFlag.NoFormatConversion
        )
        rect = QtCore.QRect(QtCore.QPoint(0, 0), size)
        self.paint(QtGui.QPainter(pixmap), rect, mode, state)
        return pixmap

    def change_color(self, color: types.ColorType) -> None:
        self._color = colors.get_color(color)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    engine = SVGBufferIconEngine("")
    widget = widgets.TreeView()
    widget.show()
    app.main_loop()

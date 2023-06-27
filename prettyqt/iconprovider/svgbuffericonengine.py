from __future__ import annotations

from prettyqt import constants, core, gui, svg
from prettyqt.utils import colors, datatypes


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

    def __init__(self, xml: str, color: datatypes.ColorType = "black") -> None:
        self._xml = xml
        self._color = colors.get_color(color)
        super().__init__()

    def paint(
        self,
        painter: gui.QPainter,
        rect: core.QRect,
        mode: gui.QIcon.Mode,
        state: gui.QIcon.State,
    ):
        """Paint the icon int ``rect`` using ``painter``."""
        color = self._color
        if mode == gui.QIcon.Mode.Disabled:
            color = self._color.transparent(0.3)

        xml = self._xml.replace('fill="currentColor"', color.get_name("svg_argb"))
        xml_byte = xml.encode()
        renderer = svg.SvgRenderer(xml_byte)
        renderer.render(painter, core.RectF(rect))

    def clone(self):
        """Required to subclass abstract QIconEngine."""
        return SVGBufferIconEngine(self._xml, self._color)

    def pixmap(
        self, size: core.QSize, mode: gui.QIcon.Mode, state: gui.QIcon.State
    ) -> gui.QPixmap:
        """Return the icon as a pixmap with requested size, mode, and state."""
        img = gui.Image(size, gui.QImage.Format.Format_ARGB32)
        img.fill(constants.GlobalColor.transparent)
        pixmap = gui.QPixmap.fromImage(
            img, constants.ImageConversionFlag.NoFormatConversion
        )
        rect = core.QRect(core.QPoint(0, 0), size)
        self.paint(gui.QPainter(pixmap), rect, mode, state)
        return pixmap

    def change_color(self, color: datatypes.ColorType) -> None:
        self._color = colors.get_color(color)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    engine = SVGBufferIconEngine("")
    widget = widgets.TreeView()
    widget.show()
    app.exec()

from __future__ import annotations


import math
import os

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui


def fit_image(width, height, pwidth, pheight):
    """Fit image in box of width pwidth and height pheight.

    Arguments:
        width: Width of image
        height: Height of image
        pwidth: Width of box
        pheight: Height of box

    Returns:
        scaled, new_width, new_height.
    """
    if height < 1 or width < 1:
        return False, int(width), int(height)
    scaled = height > pheight or width > pwidth
    if height > pheight:
        corrf = pheight / float(height)
        width, height = math.floor(corrf * width), pheight
    if width > pwidth:
        corrf = pwidth / float(width)
        width, height = pwidth, math.floor(corrf * height)
    if height > pheight:
        corrf = pheight / float(height)
        width, height = math.floor(corrf * width), pheight
    return scaled, int(width), int(height)


def draw_size(p, rect, w, h):
    rect = rect.adjusted(0, 0, 0, -4)
    f = p.font()
    f.setBold(True)
    p.setFont(f)
    sz = "\u00a0%d x %d\u00a0" % (w, h)
    flags = (
        QtCore.Qt.AlignmentFlag.AlignBottom
        | QtCore.Qt.AlignmentFlag.AlignRight
        | QtCore.Qt.TextFlag.TextSingleLine
    )
    szrect = p.boundingRect(rect, flags, sz)
    p.fillRect(szrect.adjusted(0, 0, 0, 4), gui.Color(0, 0, 0, 200))
    p.setPen(gui.Pen(gui.Color(255, 255, 255)))
    p.drawText(rect, flags, sz)


class ImageViewer(widgets.Widget):
    def __init__(
        self,
        parent=None,
        show_border: bool = True,
        show_size: bool = False,
        border_width: int = 1,
    ):
        super().__init__(parent)
        self._border_width = border_width
        self._pixmap = gui.Pixmap()
        self.setMinimumSize(core.Size(150, 200))
        self.draw_border = show_border
        self.show_size = show_size

    def set_image(self, pixmap: QtGui.QPixmap | os.PathLike):
        match pixmap:
            case QtGui.QPixmap():
                self._pixmap = pixmap
            case os.PathLike():
                self._pixmap = gui.Pixmap.from_file(pixmap)
        self._pixmap = pixmap
        self.updateGeometry()
        self.update()

    def toggle_show_size(self):
        self.show_size ^= True
        self.update()

    def pixmap(self):
        return self._pixmap

    def sizeHint(self):
        if self._pixmap.isNull():
            return self.minimumSize()
        return self._pixmap.size()

    def paintEvent(self, event):
        super().paintEvent(event)
        pmap = self._pixmap
        w, h = pmap.width(), pmap.height()
        ow, oh = w, h
        cw, ch = self.rect().width(), self.rect().height()
        scaled, nw, nh = fit_image(w, h, cw, ch)
        if scaled:
            pmap = pmap.scaled(
                int(nw * pmap.devicePixelRatio()),
                int(nh * pmap.devicePixelRatio()),
                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        w = pmap.width() // pmap.devicePixelRatio()
        h = pmap.height() // pmap.devicePixelRatio()

        x = abs(cw - w) // 2
        y = abs(ch - h) // 2
        target = core.Rect(x, y, w, h)
        with gui.Painter(self) as p:
            p.setRenderHints(
                gui.Painter.RenderHint.Antialiasing
                | gui.Painter.RenderHint.SmoothPixmapTransform
            )
            p.drawPixmap(target, pmap)
            if self.draw_border:
                pen = gui.Pen()
                pen.setWidth(self._border_width)
                p.setPen(pen)
                p.drawRect(target)
            if self.show_size:
                draw_size(p, target, ow, oh)


if __name__ == "__main__":
    from prettyqt import iconprovider

    app = widgets.app()
    widget = ImageViewer()
    icon = iconprovider.get_icon("mdi.folder")
    widget.set_image(icon.pixmap(256))
    widget.show()
    with app.debug_mode():
        app.main_loop()

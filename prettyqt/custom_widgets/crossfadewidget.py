from __future__ import annotations

import os

from prettyqt import core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets


class CrossFadeWidget(widgets.Widget):
    def __init__(
        self,
        pixmap_1: QtGui.QPixmap | os.PathLike | None = None,
        pixmap_2: QtGui.QPixmap | os.PathLike | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.pixmap_1 = None
        self.pixmap_2 = None
        self.set_pixmap_1(pixmap_1)
        self.set_pixmap_2(pixmap_2)
        self.set_blend_factor(0.0)
        self.timeline = core.TimeLine(finished=self.close)
        self.timeline.value_changed.connect(self.set_blend_factor)
        self.set_size_policy("fixed", "fixed")

    def start_fade(self, duration: int = 500):
        self.timeline.setDuration(duration)
        self.timeline.start()
        # self.show()

    def set_pixmap_1(self, pixmap: QtGui.QPixmap | str | QtWidgets.QWidget):
        match pixmap:
            case QtGui.QPixmap():
                self.pixmap_1 = pixmap
            case str():
                self.pixmap_1 = gui.Pixmap(pixmap)
            case QtWidgets.QWidget():
                self.pixmap_1 = pixmap.grab()
        self.updateGeometry()
        self.repaint()

    def set_pixmap_2(self, pixmap: QtGui.QPixmap | str | QtWidgets.QWidget):
        match pixmap:
            case QtGui.QPixmap():
                self.pixmap_2 = pixmap
            case str():
                self.pixmap_2 = gui.Pixmap(pixmap)
            case QtWidgets.QWidget():
                self.pixmap_2 = pixmap.grab()
        self.updateGeometry()
        self.repaint()

    def set_blend_factor(self, factor: float):
        self._blend_factor = factor
        self.repaint()

    def get_blend_factor(self) -> float:
        """Pixmap blending factor between 0.0 and 1.0."""
        return self._blend_factor

    def sizeHint(self):
        """Return max size of both."""
        size1 = self.pixmap_1.size() if self.pixmap_1 else super().sizeHint()
        size2 = self.pixmap_2.size() if self.pixmap_2 else super().sizeHint()
        return size1.expandedTo(size2)

    def paintEvent(self, event):
        """Paint the interpolated pixmap image."""
        with gui.Painter(self) as p:
            p.setClipRect(event.rect())
            factor = self.get_blend_factor() ** 2
            if self.pixmap_1 and 1.0 - factor:
                p.setOpacity(1.0 - factor)
                p.drawPixmap(core.Point(0, 0), self.pixmap_1)
            if self.pixmap_2 and factor:
                p.setOpacity(factor)
                p.drawPixmap(core.Point(0, 0), self.pixmap_2)

    blend_factor = core.Property(float, get_blend_factor, set_blend_factor)


if __name__ == "__main__":
    app = widgets.app()
    w1 = widgets.RadioButton("fdsfsdf")
    w2 = widgets.PlainTextEdit("fbbb")
    widget = CrossFadeWidget(w1, w2)
    container = widgets.Widget()
    container.set_layout("vertical")
    container.box.add(widget)
    slider = widgets.Slider("horizontal", maximum=100)
    container.box.add(slider)
    slider.valueChanged.connect(lambda x: widget.set_blend_factor(x / 100))
    container.show()
    with app.debug_mode():
        app.main_loop()

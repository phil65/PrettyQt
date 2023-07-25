from __future__ import annotations

from prettyqt import core, gui, widgets


class FaderWidget(widgets.Widget):
    pixmap_opacity = 1.0

    def __init__(
        self,
        old_widget: widgets.QWidget,
        new_widget: widgets.QWidget,
        duration: int = 300,
    ):
        super().__init__(new_widget)

        pr = gui.Window().devicePixelRatio()
        self.old_pixmap = gui.Pixmap(new_widget.size() * pr)
        self.old_pixmap.setDevicePixelRatio(pr)
        old_widget.render(self.old_pixmap)

        self.timeline = core.TimeLine(duration=duration, finished=self.close)
        self.timeline.value_changed.connect(self.animate)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    @classmethod
    def setup_example(cls):
        return None

    def paintEvent(self, event):
        with gui.Painter(self) as painter:
            painter.setOpacity(self.pixmap_opacity)
            painter.drawPixmap(0, 0, self.old_pixmap)

    def animate(self, value: float):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


if __name__ == "__main__":
    app = widgets.app()
    w1 = widgets.RadioButton("fdsfsdf")
    w2 = widgets.PlainTextEdit("fbbb")
    widget = FaderWidget(w1, w2)
    with app.debug_mode():
        app.exec()

from __future__ import annotations

from prettyqt import gui, widgets
from prettyqt.qt import QtCore


class OverlayBorder(widgets.Widget):
    """Border which surrounds a widget and follows it."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._do_resize()
        self._width = 4
        self._color = gui.Color(255, 0, 0)
        parent.installEventFilter(self)

    def eventFilter(self, source, event):
        match event.type():
            case QtCore.QEvent.Type.Resize:
                self._do_resize()
        return False

    def _do_resize(self):
        parent = self.parent()
        self.setGeometry(0, 0, parent.width(), parent.height())

    def paintEvent(self, ev):
        with gui.Painter(self) as p:
            pen = gui.Pen(self._color, self._width)
            p.setPen(pen)
            p.drawRect(self.rect())


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit()
    errorbox = OverlayBorder(widget)
    widget.show()
    app.main_loop()

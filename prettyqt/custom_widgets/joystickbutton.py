from __future__ import annotations

from math import hypot

from prettyqt import core, widgets
from prettyqt.qt import QtGui, QtWidgets


class JoystickButton(widgets.PushButton):
    state_changed = core.Signal(object)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.radius = 200
        self.setCheckable(True)
        self.state = [0, 0]
        self.set_state(0, 0)
        self.setFixedWidth(50)
        self.setFixedHeight(50)

    def mousePressEvent(self, ev):
        self.setChecked(True)
        self.press_pos = ev.position()
        ev.accept()

    def mouseMoveEvent(self, ev):
        dif = ev.position() - self.press_pos
        self.set_state(dif.x(), -dif.y())

    def mouseReleaseEvent(self, ev):
        self.setChecked(False)
        self.set_state(0, 0)

    def wheelEvent(self, ev):
        ev.accept()

    def doubleClickEvent(self, ev):
        ev.accept()

    def get_state(self):
        return self.state

    def set_state(self, x, y):
        xy = [x, y]
        d = hypot(xy[0], xy[1])  # length
        nxy = [0, 0]
        for i in [0, 1]:
            if xy[i] == 0:
                nxy[i] = 0
            else:
                nxy[i] = xy[i] / d

        if d > self.radius:
            d = self.radius
        d = (d / self.radius) ** 2
        xy = [nxy[0] * d, nxy[1] * d]

        w2 = self.width() / 2
        h2 = self.height() / 2
        self.spot_pos = core.Point(int(w2 * (1 + xy[0])), int(h2 * (1 - xy[1])))
        self.update()
        if self.state == xy:
            return
        self.state = xy
        self.state_changed.emit(self.state)

    def paintEvent(self, ev):
        super().paintEvent(ev)
        p = QtGui.QPainter(self)
        p.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        p.drawEllipse(self.spot_pos.x() - 3, self.spot_pos.y() - 3, 6, 6)

    def resizeEvent(self, ev):
        self.set_state(*self.state)
        super().resizeEvent(ev)


if __name__ == "__main__":
    app = widgets.app()
    widget = JoystickButton()
    widget.show()
    app.main_loop()

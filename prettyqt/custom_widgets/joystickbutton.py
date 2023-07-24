from __future__ import annotations

from math import hypot

from prettyqt import core, gui, widgets


class JoystickButton(widgets.PushButton):
    state_changed = core.Signal(object)

    def __init__(self, parent: widgets.QWidget | None = None):
        super().__init__(parent)
        self.radius = 200
        self.setCheckable(True)
        self._state = (0.0, 0.0)
        self.set_state((0, 0))
        self.setFixedWidth(50)
        self.setFixedHeight(50)

    def mousePressEvent(self, ev):
        self.setChecked(True)
        self.press_pos = ev.position()
        ev.accept()

    def mouseMoveEvent(self, ev):
        dif = ev.position() - self.press_pos
        self.set_state((dif.x(), -dif.y()))

    def mouseReleaseEvent(self, ev):
        self.setChecked(False)
        self.set_state((0, 0))

    def wheelEvent(self, ev):
        ev.accept()

    def doubleClickEvent(self, ev):
        ev.accept()

    def get_state(self) -> tuple[float, float]:
        return self._state

    def set_state(self, state: tuple[float, float]):
        d = hypot(state[0], state[1])  # length
        nxy = [0 if i == 0 else i / d for i in state]
        d = min(d, self.radius)
        d = (d / self.radius) ** 2
        state = (nxy[0] * d, nxy[1] * d)

        w2 = self.width() / 2
        h2 = self.height() / 2
        self.spot_pos = core.Point(int(w2 * (1 + state[0])), int(h2 * (1 - state[1])))
        self.update()
        if self._state == state:
            return
        self._state = state
        self.state_changed.emit(self._state)

    def paintEvent(self, ev):
        super().paintEvent(ev)
        p = gui.QPainter(self)
        p.setBrush(gui.QBrush(gui.QColor(0, 0, 0)))
        p.drawEllipse(self.spot_pos.x() - 3, self.spot_pos.y() - 3, 6, 6)

    def resizeEvent(self, ev):
        self.set_state(self._state)
        super().resizeEvent(ev)

    state = core.Property(
        tuple,
        get_state,
        set_state,
        doc="Button state.",
    )


if __name__ == "__main__":
    app = widgets.app()
    widget = JoystickButton()
    widget.show()
    app.exec()

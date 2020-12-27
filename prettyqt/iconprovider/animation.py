from typing import Dict, Tuple

from prettyqt import core
from prettyqt.qt import QtWidgets


class Spin:
    def __init__(
        self, parent_widget: QtWidgets.QWidget, interval: int = 10, step: int = 1
    ):
        self.parent_widget = parent_widget
        self.interval = interval
        self.step = step
        self.info: Dict[QtWidgets.QWidget, Tuple[core.Timer, int, int]] = {}

    def _update(self):
        if self.parent_widget not in self.info:
            return
        timer, angle, step = self.info[self.parent_widget]

        if angle >= 360:
            angle = 0

        angle += step
        self.info[self.parent_widget] = timer, angle, step
        self.parent_widget.update()

    def setup(self, icon_painter, painter, rect):

        if self.parent_widget not in self.info:
            timer = core.Timer(self.parent_widget)
            timer.timeout.connect(self._update)
            self.info[self.parent_widget] = timer, 0, self.step
            timer.start(self.interval)
        else:
            timer, angle, self.step = self.info[self.parent_widget]
            with painter.offset_by(rect.width() * 0.5, rect.height() * 0.5):
                painter.rotate(angle)


class Pulse(Spin):
    def __init__(self, parent_widget):
        super().__init__(parent_widget, interval=300, step=45)

from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class Dial(widgets.AbstractSliderMixin, QtWidgets.QDial):
    value_changed = core.Signal(int)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.valueChanged.connect(self.on_value_change)


if __name__ == "__main__":
    app = widgets.app()
    slider = Dial()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.main_loop()

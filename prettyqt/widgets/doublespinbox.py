from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class DoubleSpinBox(widgets.AbstractSpinBoxMixin, QtWidgets.QDoubleSpinBox):
    value_changed = core.Signal(float)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        default_value: float | None = None,
    ):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def set_range(self, start: float | None, end: float | None):
        if start is None:
            start = -float("inf")
        if end is None:
            end = float("inf")
        self.setRange(start, end)


if __name__ == "__main__":
    app = widgets.app()
    widget = DoubleSpinBox()
    widget.show()
    app.main_loop()

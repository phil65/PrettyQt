from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class SpinBox(widgets.AbstractSpinBoxMixin, QtWidgets.QSpinBox):
    value_changed = core.Signal(int)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        default_value: int | None = None,
    ):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def set_range(self, start: int | None, end: int | None):
        if start is None:
            start = -2147483647
        if end is None:
            end = 2147483647
        self.setRange(start, end)

    def set_step_size(self, step_size):
        self.setSingleStep(step_size)


if __name__ == "__main__":
    app = widgets.app()
    widget = SpinBox()
    widget.show()
    app.main_loop()

from __future__ import annotations

from prettyqt import core, widgets

MAX_VAL = 2147483647


class SpinBox(widgets.AbstractSpinBoxMixin, widgets.QSpinBox):
    value_changed = core.Signal(int)

    def __init__(self, *args, maximum: int = MAX_VAL, **kwargs):
        super().__init__(*args, maximum=maximum, **kwargs)
        self.valueChanged.connect(self.value_changed)

    def set_range(self, start: int | None, end: int | None):
        self.setMinimum(start)
        self.setMaximum(end)

    setRange = set_range

    def set_minimum(self, value: int | None):
        if value is None:
            value = -MAX_VAL
        super().setMinimum(value)

    setMinimum = set_minimum

    def set_maximum(self, value: int | None):
        if value is None:
            value = MAX_VAL
        super().setMaximum(value)

    setMaximum = set_maximum

    def set_step_size(self, step_size):
        self.setSingleStep(step_size)


if __name__ == "__main__":
    app = widgets.app()
    widget = SpinBox()
    widget.show()
    app.exec()

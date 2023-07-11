from __future__ import annotations

from prettyqt import core, widgets


class DoubleSpinBox(widgets.AbstractSpinBoxMixin, widgets.QDoubleSpinBox):
    """Spin box widget that takes doubles."""

    value_changed = core.Signal(float)

    def __init__(self, *args, maximum: float = float("inf"), **kwargs):
        super().__init__(*args, maximum=maximum, **kwargs)
        self.valueChanged.connect(self.value_changed)

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, float)

    def set_range(self, start: float | None, end: float | None):
        self.set_minimum(start)
        self.set_maximum(end)

    setRange = set_range

    def set_minimum(self, value: float | None):
        if value is None:
            value = -float("inf")
        super().setMinimum(value)

    setMinimum = set_minimum

    def set_maximum(self, value: float | None):
        if value is None:
            value = float("inf")
        super().setMaximum(value)

    setMaximum = set_maximum


if __name__ == "__main__":
    app = widgets.app()
    widget = DoubleSpinBox()
    widget.show()
    app.exec()

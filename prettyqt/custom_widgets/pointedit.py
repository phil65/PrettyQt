from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import datatypes


class PointEdit(widgets.Widget):
    value_changed = core.Signal(core.Point)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spinbox_x = widgets.SpinBox()
        self.spinbox_y = widgets.SpinBox()
        with widgets.HBoxLayout.create(self) as layout:
            layout.add(widgets.Label("x"))
            layout.add(self.spinbox_x)
            layout.add(widgets.Label("y"))
            layout.add(self.spinbox_y)
        self.spinbox_x.value_changed.connect(self._on_value_change)
        self.spinbox_y.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Point:
        return core.Point(
            self.spinbox_x.get_value(),
            self.spinbox_y.get_value(),
        )

    def set_value(self, value: datatypes.PointType):
        if isinstance(value, tuple):
            value = core.Point(*value)
        self._value = value
        self.spinbox_x.set_value(value.x())
        self.spinbox_y.set_value(value.y())

    value = core.Property(core.Point, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = PointEdit(window_title="Test")
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()

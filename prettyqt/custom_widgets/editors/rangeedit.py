from __future__ import annotations

from prettyqt import core, widgets


class RangeEdit(widgets.Widget):
    value_changed = core.Signal(range)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_margin(0)
        self.spinbox_start = widgets.SpinBox(maximum=999999)
        self.spinbox_stop = widgets.SpinBox(maximum=999999)
        self.spinbox_step = widgets.SpinBox(minimum=1, maximum=999999)
        layout = self.set_layout("horizontal", margin=0)
        layout.add(widgets.Label("Start", alignment="center_right"))
        layout.add(self.spinbox_start)
        layout.add(widgets.Label("Stop", alignment="center_right"))
        layout.add(self.spinbox_stop)
        layout.add(widgets.Label("Step", alignment="center_right"))
        layout.add(self.spinbox_step)

        self.spinbox_start.value_changed.connect(self._on_value_change)
        self.spinbox_stop.value_changed.connect(self._on_value_change)
        self.spinbox_step.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> range:
        return range(
            self.spinbox_start.get_value(),
            self.spinbox_stop.get_value(),
            self.spinbox_step.get_value(),
        )

    def set_value(self, value: range | tuple[int, int, int]):
        if isinstance(value, tuple):
            value = range(*value)
        self._value = value
        self.spinbox_start.set_value(value.start)
        self.spinbox_stop.set_value(value.stop)
        self.spinbox_step.set_value(value.step)


if __name__ == "__main__":
    app = widgets.app()
    widget = RangeEdit(window_title="Test")
    widget.set_value(range(0, 10, 1))
    widget.value_changed.connect(print)
    widget.show()
    app.exec()

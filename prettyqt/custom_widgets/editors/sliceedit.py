from __future__ import annotations

from prettyqt import core, widgets


class SliceEdit(widgets.Widget):
    value_changed = core.Signal(slice)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_margin(0)
        self.checkbox_start = widgets.CheckBox()
        self.checkbox_stop = widgets.CheckBox()
        self.checkbox_step = widgets.CheckBox()
        self.spinbox_start = widgets.SpinBox(maximum=999999)
        self.spinbox_stop = widgets.SpinBox(maximum=999999)
        self.spinbox_step = widgets.SpinBox(maximum=999999)
        layout = self.set_layout("horizontal", margin=0)
        layout.add(widgets.Label("Start", alignment="center_right"))
        layout.add(self.checkbox_start)
        layout.add(self.spinbox_start)
        layout.add(widgets.Label("Stop", alignment="center_right"))
        layout.add(self.checkbox_stop)
        layout.add(self.spinbox_stop)
        layout.add(widgets.Label("Step", alignment="center_right"))
        layout.add(self.checkbox_step)
        layout.add(self.spinbox_step)
        self.checkbox_start.value_changed.connect(self.spinbox_start.setEnabled)
        self.checkbox_stop.value_changed.connect(self.spinbox_stop.setEnabled)
        self.checkbox_step.value_changed.connect(self.spinbox_step.setEnabled)
        self.spinbox_start.value_changed.connect(self._on_value_change)
        self.spinbox_stop.value_changed.connect(self._on_value_change)
        self.spinbox_step.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> slice:
        return slice(
            self.spinbox_start.get_value(),
            self.spinbox_stop.get_value(),
            self.spinbox_step.get_value(),
        )

    def set_value(self, value: slice | tuple[int | None, int | None, int | None]):
        if isinstance(value, tuple):
            value = slice(*value)
        self.checkbox_start.set_value(value.start is not None)
        self.checkbox_stop.set_value(value.stop is not None)
        self.checkbox_step.set_value(value.step is not None)
        self.spinbox_start.setEnabled(value.start is not None)
        self.spinbox_stop.setEnabled(value.stop is not None)
        self.spinbox_step.setEnabled(value.step is not None)
        if value.start is not None:
            self.spinbox_start.set_value(value.start)
        if value.stop is not None:
            self.spinbox_stop.set_value(value.stop)
        if value.step is not None:
            self.spinbox_step.set_value(value.step)


if __name__ == "__main__":
    app = widgets.app()
    widget = SliceEdit(window_title="Test")
    widget.set_value(slice(None, 3, 1))
    widget.value_changed.connect(print)
    widget.show()
    app.exec()

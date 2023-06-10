from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.utils import datatypes


class SizeEdit(widgets.Widget):
    value_changed = core.Signal(core.Size)

    def __init__(self, *args, object_name: str = "size_edit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_margin(0)
        self.spinbox_width = widgets.SpinBox(maximum=999999)
        self.spinbox_height = widgets.SpinBox(maximum=999999)
        layout = self.set_layout("horizontal", margin=0)
        layout.add(widgets.Label("width", alignment="center_right"))
        layout.add(self.spinbox_width)
        layout.add(widgets.Label("height", alignment="center_right"))
        layout.add(self.spinbox_height)
        self.spinbox_width.value_changed.connect(self._on_value_change)
        self.spinbox_height.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Size:
        return core.Size(
            self.spinbox_width.get_value(),
            self.spinbox_height.get_value(),
        )

    def set_value(self, value: datatypes.SizeType):
        if isinstance(value, tuple):
            value = core.Size(*value)
        self._value = value
        self.spinbox_width.set_value(value.width())
        self.spinbox_height.set_value(value.height())

    value = core.Property(core.Size, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = SizeEdit(window_title="Test")
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()

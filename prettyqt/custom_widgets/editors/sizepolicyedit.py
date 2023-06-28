from __future__ import annotations

from prettyqt import core, widgets


class SizePolicyEdit(widgets.Widget):
    value_changed = core.Signal(widgets.QSizePolicy)

    def __init__(self, *args, object_name: str = "sizepolicy_edit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.set_margin(0)
        self.cb_horizontal = widgets.ComboBox()
        self.cb_vertical = widgets.ComboBox()
        self.cb_control_type = widgets.ComboBox()
        layout = self.set_layout("horizontal", margin=0)
        layout.add(widgets.Label("Horizontal:", alignment="center_right"))
        layout.add(self.cb_horizontal)
        layout.add(widgets.Label("Vertical:", alignment="center_right"))
        layout.add(self.cb_vertical)
        layout.add(widgets.Label("Control type:", alignment="center_right"))
        layout.add(self.cb_control_type)
        self.cb_vertical.add_items(widgets.sizepolicy.SIZE_POLICY.keys())
        self.cb_horizontal.add_items(widgets.sizepolicy.SIZE_POLICY.keys())
        self.cb_control_type.add_items(widgets.sizepolicy.CONTROL_TYPE.keys())
        self.cb_horizontal.value_changed.connect(self._on_value_change)
        self.cb_vertical.value_changed.connect(self._on_value_change)
        self.cb_control_type.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Point:
        policy = widgets.SizePolicy()
        policy.set_horizontal_policy(self.cb_horizontal.get_value())
        policy.set_vertical_policy(self.cb_vertical.get_value())
        policy.set_control_type(self.cb_control_type.get_value())
        return policy

    def set_value(self, value: widgets.QSizePolicy):
        self._value = value
        self.cb_horizontal.set_value(
            widgets.sizepolicy.SIZE_POLICY.inverse[value.horizontalPolicy()]
        )
        self.cb_vertical.set_value(
            widgets.sizepolicy.SIZE_POLICY.inverse[value.verticalPolicy()]
        )
        self.cb_control_type.set_value(
            widgets.sizepolicy.CONTROL_TYPE.inverse[value.controlType()]
        )

    value = core.Property(widgets.QSizePolicy, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = SizePolicyEdit(window_title="Test")
    widget.set_value(widgets.SizePolicy())
    widget.show()
    app.exec()

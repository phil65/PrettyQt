from __future__ import annotations

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets


class SizePolicyEdit(widgets.Widget):
    value_changed = core.Signal(QtWidgets.QSizePolicy)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cb_horizontal = widgets.ComboBox()
        self.cb_vertical = widgets.ComboBox()
        with widgets.HBoxLayout.create(self) as layout:
            layout.add(widgets.Label("horizontal"))
            layout.add(self.cb_horizontal)
            layout.add(widgets.Label("vertical"))
            layout.add(self.cb_vertical)
        self.cb_vertical.add_items(widgets.sizepolicy.SIZE_POLICY.keys())
        self.cb_horizontal.add_items(widgets.sizepolicy.SIZE_POLICY.keys())
        self.cb_horizontal.value_changed.connect(self._on_value_change)
        self.cb_vertical.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Point:
        policy = widgets.SizePolicy()
        policy.set_horizontal_policy(self.cb_horizontal.get_value())
        policy.set_vertical_policy(self.cb_vertical.get_value())
        return policy

    def set_value(self, value: QtWidgets.QSizePolicy):
        self._value = value
        self.cb_horizontal.set_value(
            widgets.sizepolicy.SIZE_POLICY.inverse[value.horizontalPolicy()]
        )
        self.cb_vertical.set_value(
            widgets.sizepolicy.SIZE_POLICY.inverse[value.verticalPolicy()]
        )

    value = core.Property(QtWidgets.QSizePolicy, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = SizePolicyEdit(window_title="Test")
    widget.set_value(widgets.SizePolicy())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()

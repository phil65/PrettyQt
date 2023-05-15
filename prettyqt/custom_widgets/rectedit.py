from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import datatypes


class RectEdit(widgets.Widget):
    value_changed = core.Signal(QtCore.QRect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spinbox_x = widgets.SpinBox(maximum=999999)
        self.spinbox_y = widgets.SpinBox(maximum=999999)
        self.spinbox_width = widgets.SpinBox(maximum=999999)
        self.spinbox_height = widgets.SpinBox(maximum=999999)
        with widgets.HBoxLayout.create(self) as layout:
            layout.add(widgets.Label("x"))
            layout.add(self.spinbox_x)
            layout.add(widgets.Label("y"))
            layout.add(self.spinbox_y)
            layout.add(widgets.Label("w"))
            layout.add(self.spinbox_width)
            layout.add(widgets.Label("h"))
            layout.add(self.spinbox_height)

        self.spinbox_x.value_changed.connect(self._on_value_change)
        self.spinbox_y.value_changed.connect(self._on_value_change)
        self.spinbox_width.value_changed.connect(self._on_value_change)
        self.spinbox_height.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Rect:
        return core.Rect(
            self.spinbox_x.get_value(),
            self.spinbox_y.get_value(),
            self.spinbox_width.get_value(),
            self.spinbox_height.get_value(),
        )

    def set_value(self, value: datatypes.RectType):
        if isinstance(value, tuple):
            value = core.Rect(*value)
        self._value = value
        self.spinbox_x.set_value(value.x())
        self.spinbox_y.set_value(value.y())
        self.spinbox_width.set_value(value.width())
        self.spinbox_height.set_value(value.height())

    value = core.Property(core.Rect, get_value, set_value, user=True)


class RegionEdit(RectEdit):
    value_changed = core.Signal(QtGui.QRegion)

    def get_value(self) -> gui.Region:
        return gui.Region(
            self.spinbox_x.get_value(),
            self.spinbox_y.get_value(),
            self.spinbox_width.get_value(),
            self.spinbox_height.get_value(),
        )

    def set_value(self, value: QtGui.QRegion):
        if isinstance(value, tuple):
            value = gui.Region(*value)
        self._value = value
        bounding_rect = value.boundingRect()
        self.spinbox_x.set_value(bounding_rect.x())
        self.spinbox_y.set_value(bounding_rect.y())
        self.spinbox_width.set_value(bounding_rect.width())
        self.spinbox_height.set_value(bounding_rect.height())

    value = core.Property(gui.Region, get_value, set_value, user=True)


if __name__ == "__main__":
    app = widgets.app()
    widget = RegionEdit(window_title="Test")
    widget.set_value(QtGui.QRegion())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()

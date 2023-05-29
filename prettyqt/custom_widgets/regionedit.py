from __future__ import annotations

from prettyqt import core, custom_widgets, gui, widgets
from prettyqt.qt import QtGui


class RegionEdit(custom_widgets.rectedit.BaseRectEdit):
    Widget = widgets.SpinBox
    value_changed = core.Signal(QtGui.QRegion)
    Typ = QtGui.QRegion

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
    from prettyqt import widgets

    app = widgets.app()
    widget = RegionEdit(window_title="Test")
    widget.set_value(QtGui.QRegion())
    widget.value_changed.connect(print)
    widget.show()
    app.main_loop()

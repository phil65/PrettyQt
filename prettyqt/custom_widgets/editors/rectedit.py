from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import datatypes


class BaseRectEdit(widgets.Widget):
    Typ: type
    Widget: type[QtWidgets.QWidget]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_margin(0)
        self.spinbox_x = self.Widget(maximum=999999)
        self.spinbox_y = self.Widget(maximum=999999)
        self.spinbox_width = widgets.SpinBox(maximum=999999)
        self.spinbox_height = widgets.SpinBox(maximum=999999)
        layout = self.set_layout("horizontal", margin=0)
        layout.add(widgets.Label("x", alignment="center_right"))
        layout.add(self.spinbox_x)
        layout.add(widgets.Label("y", alignment="center_right"))
        layout.add(self.spinbox_y)
        layout.add(widgets.Label("w", alignment="center_right"))
        layout.add(self.spinbox_width)
        layout.add(widgets.Label("h", alignment="center_right"))
        layout.add(self.spinbox_height)

        self.spinbox_x.value_changed.connect(self._on_value_change)
        self.spinbox_y.value_changed.connect(self._on_value_change)
        self.spinbox_width.value_changed.connect(self._on_value_change)
        self.spinbox_height.value_changed.connect(self._on_value_change)

    def _on_value_change(self):
        self._value = self.get_value()
        self.value_changed.emit(self._value)

    def get_value(self) -> core.Rect | core.RectF:
        return self.Typ(
            self.spinbox_x.get_value(),
            self.spinbox_y.get_value(),
            self.spinbox_width.get_value(),
            self.spinbox_height.get_value(),
        )

    def set_value(self, value: datatypes.RectType | datatypes.RectFType):
        if isinstance(value, tuple):
            value = self.Typ(*value)
        self._value = value
        self.spinbox_x.set_value(value.x())
        self.spinbox_y.set_value(value.y())
        self.spinbox_width.set_value(value.width())
        self.spinbox_height.set_value(value.height())


class RectEdit(BaseRectEdit):
    Typ = QtCore.QRect
    Widget = widgets.SpinBox
    value_changed = core.Signal(QtCore.QRect)

    def set_value(self, value: datatypes.RectType):
        super().set_value(value)

    def get_value(self) -> core.Rect:
        return super().get_value()

    value = core.Property(QtCore.QRect, get_value, set_value, user=True)


class RectFEdit(BaseRectEdit):
    Typ = QtCore.QRectF
    Widget = widgets.DoubleSpinBox
    value_changed = core.Signal(QtCore.QRectF)

    def set_value(self, value: datatypes.RectFType):
        super().set_value(value)

    def get_value(self) -> core.RectF:
        return super().get_value()

    value = core.Property(QtCore.QRectF, get_value, set_value, user=True)


class RegionEdit(BaseRectEdit):
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
    app = widgets.app()
    widget = RectFEdit(window_title="Test")
    widget.set_value(QtCore.QRectF())
    widget.value_changed.connect(print)
    widget.show()
    app.exec()

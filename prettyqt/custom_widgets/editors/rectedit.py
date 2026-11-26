from typing import ClassVar

from prettyqt import core, gui, widgets
from prettyqt.utils import datatypes


class BaseRectEdit(widgets.Widget):
    Typ: ClassVar[type]
    Widget: ClassVar[type[widgets.SpinBox | widgets.DoubleSpinBox]]
    value_changed: ClassVar[core.Signal]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_margin(0)
        self.spinbox_x = self.Widget(maximum=999999)
        self.spinbox_y = self.Widget(maximum=999999)
        self.spinbox_width = self.Widget(maximum=999999)
        self.spinbox_height = self.Widget(maximum=999999)
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

    def get_value(self) -> core.Rect | core.RectF | gui.QRegion:
        return self.Typ(
            self.spinbox_x.value(),
            self.spinbox_y.value(),
            self.spinbox_width.value(),
            self.spinbox_height.value(),
        )

    def set_value(self, value: core.QRect | core.QRectF):
        self._value = value
        self.spinbox_x.set_value(value.x())
        self.spinbox_y.set_value(value.y())
        self.spinbox_width.set_value(value.width())
        self.spinbox_height.set_value(value.height())


class RectEdit(BaseRectEdit):
    Typ = core.QRect
    Widget = widgets.SpinBox
    value_changed = core.Signal(core.QRect)
    spinbox_x: widgets.SpinBox
    spinbox_y: widgets.SpinBox
    spinbox_width: widgets.SpinBox
    spinbox_height: widgets.SpinBox

    def set_value(self, value: datatypes.RectType):
        super().set_value(datatypes.to_rect(value))

    def get_value(self) -> core.Rect:
        return core.Rect(
            self.spinbox_x.value(),
            self.spinbox_y.value(),
            self.spinbox_width.value(),
            self.spinbox_height.value(),
        )

    value = core.Property(
        core.QRect,
        get_value,
        set_value,
        user=True,
        doc="Current value",
    )


class RectFEdit(BaseRectEdit):
    Typ = core.QRectF
    Widget = widgets.DoubleSpinBox
    value_changed = core.Signal(core.QRectF)
    spinbox_x: widgets.DoubleSpinBox
    spinbox_y: widgets.DoubleSpinBox
    spinbox_width: widgets.DoubleSpinBox
    spinbox_height: widgets.DoubleSpinBox

    def set_value(self, value: datatypes.RectFType):
        super().set_value(datatypes.to_rectf(value))

    def get_value(self) -> core.RectF:
        return core.RectF(
            self.spinbox_x.value(),
            self.spinbox_y.value(),
            self.spinbox_width.value(),
            self.spinbox_height.value(),
        )

    value = core.Property(
        core.QRectF,
        get_value,
        set_value,
        user=True,
        doc="Current value",
    )


class RegionEdit(BaseRectEdit):
    Widget = widgets.SpinBox
    value_changed = core.Signal(gui.QRegion)
    Typ = gui.QRegion
    spinbox_x: widgets.SpinBox
    spinbox_y: widgets.SpinBox
    spinbox_width: widgets.SpinBox
    spinbox_height: widgets.SpinBox

    def get_value(self) -> gui.Region:
        return gui.Region(
            self.spinbox_x.value(),
            self.spinbox_y.value(),
            self.spinbox_width.value(),
            self.spinbox_height.value(),
        )

    def set_value(self, value: gui.QRegion | tuple[int, int, int, int]):
        if isinstance(value, tuple):
            value = gui.Region(*value)
        self._value = value
        bounding_rect = value.boundingRect()
        self.spinbox_x.set_value(bounding_rect.x())
        self.spinbox_y.set_value(bounding_rect.y())
        self.spinbox_width.set_value(bounding_rect.width())
        self.spinbox_height.set_value(bounding_rect.height())

    value = core.Property(
        gui.Region,
        get_value,
        set_value,
        user=True,
        doc="Current value",
    )


if __name__ == "__main__":
    app = widgets.app()
    widget = RectFEdit(window_title="Test")
    widget.set_value(core.QRectF())
    widget.value_changed.connect(print)
    widget.show()
    app.exec()

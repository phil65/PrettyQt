from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import datatypes


class CursorMoveAnimation(core.VariantAnimation):
    def __init__(
        self,
        duration: int = 1000,
        end: datatypes.PointType = (0, 0),
        start: datatypes.PointType | None = None,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.set_easing(easing)

        start = gui.Cursor.pos() if start is None else core.Point(*start)
        self.set_start_value(start)
        self.set_end_value(end)
        self.setDuration(duration)
        self.valueChanged.connect(gui.Cursor.setPos)

    def set_start_value(self, point: datatypes.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setStartValue(point)

    def set_end_value(self, point: datatypes.PointType):
        if isinstance(point, tuple):
            point = core.Point(*point)
        self.setEndValue(point)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    animation = CursorMoveAnimation()
    animation.set_end_value((100, 100))
    btn = widgets.PushButton("ts")
    btn.show()
    animation.start()
    app.main_loop()

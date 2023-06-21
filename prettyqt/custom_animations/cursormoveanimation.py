from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import datatypes


class CursorMoveAnimation(core.VariantAnimation):
    """Animation to move mouse cursor. None for start / end uses current position."""

    def __init__(
        self,
        duration: int = 1000,
        start: datatypes.PointType | None = None,
        end: datatypes.PointType = (0, 0),
        easing: core.easingcurve.TypeStr = "in_out_sine",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.set_easing(easing)
        self.set_start_value(start)
        self.set_end_value(end)
        self.setDuration(duration)
        self.valueChanged.connect(gui.Cursor.setPos)

    def set_start_value(self, point: datatypes.PointType | None):
        """Set start position of mouse move."""
        point = gui.Cursor.pos() if point is None else datatypes.to_point(point)
        self.setStartValue(point)

    def set_end_value(self, point: datatypes.PointType | None):
        """Set start position of mouse move."""
        point = gui.Cursor.pos() if point is None else datatypes.to_point(point)
        self.setEndValue(point)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    animation = CursorMoveAnimation()
    animation.set_end_value((100, 100))
    btn = widgets.PushButton("ts")
    btn.show()
    animation.start()
    app.exec()

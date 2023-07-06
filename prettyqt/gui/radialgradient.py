from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import get_repr


class RadialGradient(gui.GradientMixin, gui.QRadialGradient):
    def __repr__(self):
        return get_repr(
            self,
            self.get_center(),
            self.centerRadius(),
            self.get_focal_point(),
            self.focalRadius(),
        )

    def get_center(self) -> core.PointF:
        return core.PointF(self.center())

    def get_focal_point(self) -> core.PointF:
        return core.PointF(self.focalPoint())

    def get_css(self) -> str:
        """Convert gradient to a CSS string. Can be used for stylesheets."""
        cx, cy = self.center().x(), self.center().y()
        fx, fy = self.focalPoint().x(), self.focalPoint().y()
        stops = self.stops()
        stops = "\n".join(f"    stop: {stop:f} {color.name()}" for stop, color in stops)
        spread = self.get_spread()
        # couldnt find equivalent for focalRadius on first sight.
        return (
            "qradialgradient(\n"
            f"    cx: {cx}, cy: {cy}, radius: {self.radius()}, fx: {fx}, fy: {fy},\n"
            f"    spread:{spread},\n"
            f"{stops})"
        )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    grad = RadialGradient()
    grad.set_color_at(0, "red")
    grad.set_color_at(0.5, "blue")
    grad.set_color_at(1, "green")
    print(grad.get_css())
    btn = widgets.PushButton("TestButton")
    btn.setStyleSheet(f"QPushButton{{ background-color:{grad.get_css()} }}")
    btn.show()
    app.exec()

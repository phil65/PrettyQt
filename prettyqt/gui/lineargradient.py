from __future__ import annotations

from prettyqt import core, gui
from prettyqt.utils import get_repr


class LinearGradient(gui.GradientMixin, gui.QLinearGradient):
    def __repr__(self):
        return get_repr(self, self.get_start(), self.get_final_stop())

    def get_start(self) -> core.PointF:
        return core.PointF(self.start())

    def get_final_stop(self) -> core.PointF:
        return core.PointF(self.finalStop())

    def get_css(self) -> str:
        """Convert gradient to a CSS string. Can be used for stylesheets."""
        stop, finalStop = self.start(), self.finalStop()
        x1, y1, x2, y2 = stop.x(), stop.y(), finalStop.x(), finalStop.y()
        stops = self.stops()
        stops = "\n".join(f"    stop: {stop:f} {color.name()}" for stop, color in stops)
        spread = self.get_spread()
        return (
            "qlineargradient(\n"
            f"    x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}, spread:{spread},\n"
            f"{stops})"
        )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    grad = LinearGradient()
    grad.set_color_at(0, "red")
    grad.set_color_at(0.5, "blue")
    grad.set_color_at(1, "green")
    print(grad.get_css())
    btn = widgets.PushButton("TestButton")
    btn.setStyleSheet(f"QPushButton{{ background-color:{grad.get_css()} }}")
    btn.show()
    app.exec()

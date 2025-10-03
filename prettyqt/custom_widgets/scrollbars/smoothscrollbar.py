from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core, gui, widgets


if TYPE_CHECKING:
    from prettyqt import constants


class SmoothScrollBar(widgets.ScrollBar):
    scroll_ended = core.Signal()

    def __init__(
        self,
        orientation: constants.Orientation | constants.OrientationStr = "horizontal",
        parent: widgets.QAbstractScrollArea | None = None,
        animation_duration: int = 500,
        easing: core.easingcurve.TypeStr | core.QEasingCurve.Type = "out_cubic",
        trigger: bool = False,
    ):
        super().__init__(orientation, parent)
        self._value = self.value()
        self.widget = parent
        self._animation = core.PropertyAnimation()
        self._animation.apply_to(self.value)
        self._animation.set_easing(easing)
        self._animation.setDuration(animation_duration)
        self._animation.finished.connect(self.scroll_ended)
        self.widget.viewport().installEventFilter(self)
        if trigger:
            self.widget.h_scrollbar.valueChanged.connect(gui.Cursor.fake_mouse_move)

    def mouseMoveEvent(self, e):
        self._animation.stop()
        self._value = self.value()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self._animation.stop()
        self._value = self.value()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._animation.stop()
        self._value = self.value()
        super().mouseReleaseEvent(e)

    def setValue(self, value: int):
        if value == self.value():
            return
        self._animation.stop()
        self.scroll_ended.emit()
        self._animation.set_range(self.value(), value)
        self._animation.start()

    def scroll_by_value(self, value: int):
        """Scroll by given distance."""
        self._value += value
        self._value = min(max(self.minimum(), self._value), self.maximum())
        self.setValue(self._value)

    def scroll_to(self, value: int):
        """Scroll to given position."""
        self._value = value
        self._value = min(max(self.minimum(), self._value), self.maximum())
        self.setValue(self._value)

    def reset_value(self, value):
        self._value = value

    def eventFilter(self, source, event) -> bool:
        if event.type() == core.Event.Type.Wheel and source == self.widget.viewport():
            self.widget.v_scrollbar.scroll_by_value(-event.angleDelta().y())
            return True
        return False

    def set_animation_duration(self, duration: int):
        self._animation.setDuration(duration)

    def get_animation_duration(self) -> int:
        return self._animation.duration()

    def set_animation_easing(
        self,
        easing: core.easingcurve.TypeStr | core.QEasingCurve.Type = "out_cubic",
    ):
        self._animation.set_easing(easing)

    def get_animation_easing(self) -> core.easingcurve.TypeStr:
        return self._animation.get_easing()

    def animationEasing(self) -> core.QEasingCurve.Type:
        return self._animation.type()

    animation_duration = core.Property(
        int,
        set_animation_duration,
        get_animation_duration,
        doc="Duration for the animation",
    )
    animation_easing = core.Property(
        core.EasingCurve.Type,
        set_animation_easing,
        get_animation_easing,
        doc="Animation easing type",
    )


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("fusion")
    widget = widgets.PlainTextEdit("\n".join(f"abc{i}" for i in range(1000)))
    scrollbar = SmoothScrollBar("vertical", parent=widget)
    widget.setVerticalScrollBar(scrollbar)
    widget.show()
    with app.debug_mode():
        app.exec()

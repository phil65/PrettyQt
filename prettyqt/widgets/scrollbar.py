from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets


class ScrollBarMixin(widgets.AbstractSliderMixin):
    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation | constants.OrientationStr = "horizontal",
        parent: QtWidgets.QWidget | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent)
        self.valueChanged.connect(self.on_value_change)

    def scroll_to_next_row(self):
        """Scroll to the next row."""
        self.setValue(self.value() + self.singleStep())

    def scroll_to_previous_row(self):
        """Scroll to the previous row."""
        self.setValue(self.value() - self.singleStep())


class ScrollBar(ScrollBarMixin, QtWidgets.QScrollBar):
    pass


class SmoothScrollBar(ScrollBar):
    scroll_ended = core.Signal()

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation | constants.OrientationStr = "horizontal",
        parent: QtWidgets.QAbstractScrollArea | None = None,
        animation_duration: int = 500,
        easing: core.easingcurve.TypeStr = "out_cubic",
        trigger: bool = False,
    ):
        super().__init__(orientation, parent)
        self._value = self.value()
        self.widget = parent
        self.animation = core.PropertyAnimation()
        self.animation.apply_to(self.value)
        self.animation.set_easing(easing)
        self.animation.setDuration(animation_duration)
        self.animation.finished.connect(self.scroll_ended)
        self.widget.viewport().installEventFilter(self)
        if trigger:
            self.widget.h_scrollbar.valueChanged.connect(gui.Cursor.fake_mouse_move)

    def mouseMoveEvent(self, e):
        self.animation.stop()
        self._value = self.value()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self.animation.stop()
        self._value = self.value()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.animation.stop()
        self._value = self.value()
        super().mouseReleaseEvent(e)

    def setValue(self, value: int):
        if value == self.value():
            return
        self.animation.stop()
        self.scroll_ended.emit()
        self.animation.set_range(self.value(), value)
        self.animation.start()

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

    def eventFilter(self, source, event):
        if event.type() == core.Event.Type.Wheel and source == self.widget.viewport():
            self.widget.v_scrollbar.scroll_by_value(-event.angleDelta().y())
            return True
        return False

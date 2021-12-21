from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


INPUT = bidict(
    press=QtWidgets.QScroller.Input.InputPress,
    move=QtWidgets.QScroller.Input.InputMove,
    release=QtWidgets.QScroller.Input.InputRelease,
)

InputStr = Literal["press", "move", "release"]

SCROLLER_GESTURE_TYPE = bidict(
    touch=QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
    left_mouse_button=QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
    middle_mouse_button=QtWidgets.QScroller.ScrollerGestureType.MiddleMouseButtonGesture,
    right_mouse_button=QtWidgets.QScroller.ScrollerGestureType.RightMouseButtonGesture,
)

ScrollGestureTypeStr = Literal[
    "touch", "left_mouse_button", "middle_mouse_button", "right_mouse_button"
]

STATE = bidict(
    inactive=QtWidgets.QScroller.State.Inactive,
    pressed=QtWidgets.QScroller.State.Pressed,
    dragging=QtWidgets.QScroller.State.Dragging,
    scrolling=QtWidgets.QScroller.State.Scrolling,
)

StateStr = Literal["inactive", "pressed", "dragging", "scrolling"]

QtWidgets.QScroller.__bases__ = (core.Object,)


class Scroller:
    def __init__(self, item: QtWidgets.QScroller):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_state(self) -> StateStr:
        """Return current state.

        Returns:
            state
        """
        return STATE.inverse[self.state()]

    def get_velocity(self) -> core.PointF:
        return core.PointF(self.velocity())

    def get_pixel_per_meter(self) -> core.PointF:
        return core.PointF(self.pixelPerMeter())

    def get_final_position(self) -> core.PointF:
        return core.PointF(self.finalPosition())

    def handle_input(
        self, input_type: InputStr, position: types.PointFType, timestamp: int = 0
    ) -> bool:
        if isinstance(position, tuple):
            position = core.PointF(*position)
        if input_type not in INPUT:
            raise InvalidParamError(input_type, INPUT)
        return self.handleInput(INPUT[input_type], position, timestamp)

    def get_scroller_properties(self) -> widgets.ScrollerProperties:
        return widgets.ScrollerProperties(self.scrollerProperties())

    @classmethod
    def get_scroller(cls, obj: QtCore.QObject):
        return cls(QtWidgets.QScroller.scroller(obj))

    @staticmethod
    def grab_gesture(
        target: QtCore.QObject, gesture_type: ScrollGestureTypeStr = "touch"
    ) -> str:
        if gesture_type not in SCROLLER_GESTURE_TYPE:
            raise InvalidParamError(gesture_type, SCROLLER_GESTURE_TYPE)
        gesture = QtWidgets.QScroller.grabGesture(
            target, SCROLLER_GESTURE_TYPE[gesture_type]
        )
        if gesture >= 256:
            gesture -= 256
        return constants.GESTURE_TYPE.inverse[gesture]


if __name__ == "__main__":
    app = widgets.app()
    w = QtWidgets.QPlainTextEdit()
    scroller = Scroller.get_scroller(w)

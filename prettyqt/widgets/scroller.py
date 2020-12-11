from qtpy import QtWidgets, QtCore

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError

INPUT = bidict(
    press=QtWidgets.QScroller.InputPress,
    move=QtWidgets.QScroller.InputMove,
    release=QtWidgets.QScroller.InputRelease,
)

SCROLLER_GESTURE_TYPE = bidict(
    touch=QtWidgets.QScroller.TouchGesture,
    left_mouse_button=QtWidgets.QScroller.LeftMouseButtonGesture,
    middle_mouse_button=QtWidgets.QScroller.MiddleMouseButtonGesture,
    right_mouse_button=QtWidgets.QScroller.RightMouseButtonGesture,
)

GESTURE_TYPE = bidict(
    tap=QtCore.Qt.TapGesture,
    tap_and_hold=QtCore.Qt.TapAndHoldGesture,
    pan=QtCore.Qt.PanGesture,
    pinch=QtCore.Qt.PinchGesture,
    swipe=QtCore.Qt.SwipeGesture,
    custom=QtCore.Qt.CustomGesture,
)

STATE = bidict(
    inactive=QtWidgets.QScroller.Inactive,
    pressed=QtWidgets.QScroller.Pressed,
    dragging=QtWidgets.QScroller.Dragging,
    scrolling=QtWidgets.QScroller.Scrolling,
)

QtWidgets.QScroller.__bases__ = (core.Object,)


class Scroller:
    def __init__(self, item: QtWidgets.QScroller):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_state(self) -> str:
        """Return current state.

        Possible values: "inactive", "pressed", "dragging", "scrolling"

        Returns:
            state
        """
        return STATE.inv[self.state()]

    def get_velocity(self) -> core.PointF:
        return core.PointF(self.velocity())

    def get_pixel_per_meter(self) -> core.PointF:
        return core.PointF(self.pixelPerMeter())

    def get_final_position(self) -> core.PointF:
        return core.PointF(self.finalPosition())

    def handle_input(
        self, input_type: str, position: QtCore.QPointF, timestamp: int = 0
    ) -> bool:
        if input_type not in INPUT:
            raise InvalidParamError(input_type, INPUT)
        return self.handleInput(INPUT[input_type], position, timestamp)

    def get_scroller_properties(self) -> widgets.ScrollerProperties:
        return widgets.ScrollerProperties(self.scrollerProperties())

    @classmethod
    def get_scroller(cls, obj: QtCore.QObject):
        return cls(QtWidgets.QScroller.scroller(obj))

    @staticmethod
    def grab_gesture(target: QtCore.QObject, gesture_type: str = "touch") -> str:
        if gesture_type not in SCROLLER_GESTURE_TYPE:
            raise InvalidParamError(gesture_type, SCROLLER_GESTURE_TYPE)
        gesture = QtWidgets.QScroller.grabGesture(
            target, SCROLLER_GESTURE_TYPE[gesture_type]
        )
        if gesture >= 256:
            gesture -= 256
        return GESTURE_TYPE.inv[gesture]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = QtWidgets.QPlainTextEdit()
    scroller = Scroller.get_scroller(w)

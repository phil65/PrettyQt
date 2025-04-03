from __future__ import annotations

from typing import Literal, Self

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict, datatypes


InputStr = Literal["press", "move", "release"]

INPUT: bidict[InputStr, widgets.QScroller.Input] = bidict(
    press=widgets.QScroller.Input.InputPress,
    move=widgets.QScroller.Input.InputMove,
    release=widgets.QScroller.Input.InputRelease,
)

ScrollGestureTypeStr = Literal[
    "touch", "left_mouse_button", "middle_mouse_button", "right_mouse_button"
]

SCROLLER_GESTURE_TYPE: bidict[
    ScrollGestureTypeStr, widgets.QScroller.ScrollerGestureType
] = bidict(
    touch=widgets.QScroller.ScrollerGestureType.TouchGesture,
    left_mouse_button=widgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
    middle_mouse_button=widgets.QScroller.ScrollerGestureType.MiddleMouseButtonGesture,
    right_mouse_button=widgets.QScroller.ScrollerGestureType.RightMouseButtonGesture,
)


StateStr = Literal["inactive", "pressed", "dragging", "scrolling"]

STATE: bidict[StateStr, widgets.QScroller.State] = bidict(
    inactive=widgets.QScroller.State.Inactive,
    pressed=widgets.QScroller.State.Pressed,
    dragging=widgets.QScroller.State.Dragging,
    scrolling=widgets.QScroller.State.Scrolling,
)


class Scroller(core.ObjectMixin):
    """Enables kinetic scrolling for any scrolling widget or graphics item."""

    def __init__(self, item: widgets.QScroller):
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
        self,
        input_type: InputStr | widgets.QScroller.Input,
        position: datatypes.PointFType,
        timestamp: int = 0,
    ) -> bool:
        return self.handleInput(
            INPUT.get_enum_value(input_type), datatypes.to_pointf(position), timestamp
        )

    def get_scroller_properties(self) -> widgets.ScrollerProperties:
        return widgets.ScrollerProperties(self.scrollerProperties())

    @classmethod
    def get_scroller(cls, obj: core.QObject) -> Self:
        return cls(widgets.QScroller.scroller(obj))

    @staticmethod
    def grab_gesture(
        target: core.QObject,
        gesture_type: (
            ScrollGestureTypeStr | widgets.QScroller.ScrollerGestureType
        ) = "touch",
    ) -> constants.GestureTypeStr:
        gesture = widgets.QScroller.grabGesture(
            target, SCROLLER_GESTURE_TYPE.get_enum_value(gesture_type)
        )
        if gesture >= 256:  # noqa: PLR2004
            gesture -= 256
        return constants.GESTURE_TYPE.inverse[gesture]

    @staticmethod
    def grabbed_gesture(target: core.QObject) -> constants.GestureTypeStr:
        return constants.GESTURE_TYPE.inverse[widgets.QScroller.grabbedGesture(target)]


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.QPlainTextEdit()
    scroller = Scroller.get_scroller(w)

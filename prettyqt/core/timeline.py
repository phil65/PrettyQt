# -*- coding: utf-8 -*-

from typing import Union, Callable

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

DIRECTION = bidict(forward=QtCore.QTimeLine.Forward, backward=QtCore.QTimeLine.Backward)

STATE = bidict(
    not_running=QtCore.QTimeLine.NotRunning,
    paused=QtCore.QTimeLine.Paused,
    running=QtCore.QTimeLine.Running,
)

QtCore.QTimeLine.__bases__ = (core.Object,)


class TimeLine(QtCore.QTimeLine):
    def serialize_fields(self):
        return dict(
            current_time=self.currentTime(),
            direction=self.get_direction(),
            duration=self.duration(),
            easing_curve=self.easingCurve(),
            loop_count=self.loopCount(),
            update_interval=self.updateInterval(),
        )

    def set_direction(self, direction: str):
        """Set the direction.

        Allowed values are "forward", "backward"

        Args:
            direction: direction

        Raises:
            InvalidParamError: direction does not exist
        """
        if direction not in DIRECTION:
            raise InvalidParamError(direction, DIRECTION)
        self.setDirection(DIRECTION[direction])

    def get_direction(self) -> str:
        """Return current direction.

        Possible values: "forward", "backward"

        Returns:
            direction
        """
        return DIRECTION.inv[self.direction()]

    def get_state(self) -> str:
        """Return current state.

        Possible values: "not_running", "paused", "running"

        Returns:
            state
        """
        return STATE.inv[self.state()]

    def set_easing(
        self, easing_type: Union[str, Callable[[float], float]]
    ) -> core.EasingCurve:
        curve = core.EasingCurve()
        if isinstance(easing_type, str):
            curve.set_type(easing_type)
        else:
            curve.set_custom_type(easing_type)
        self.setEasingCurve(curve)
        return curve

    def get_easing(self) -> Union[str, Callable[[float], float]]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        if typ == "custom":
            return curve.get_custom_type()
        else:
            return typ

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


DIRECTION = bidict(
    forward=QtCore.QTimeLine.Direction.Forward,
    backward=QtCore.QTimeLine.Direction.Backward,
)

DirectionStr = Literal["forward", "backward"]

STATE = bidict(
    not_running=QtCore.QTimeLine.State.NotRunning,
    paused=QtCore.QTimeLine.State.Paused,
    running=QtCore.QTimeLine.State.Running,
)

StateStr = Literal["not_running", "paused", "running"]


class TimeLine(core.ObjectMixin, QtCore.QTimeLine):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"direction": DIRECTION}
        return maps

    def set_direction(self, direction: DirectionStr):
        """Set the direction.

        Args:
            direction: direction

        Raises:
            InvalidParamError: direction does not exist
        """
        if direction not in DIRECTION:
            raise InvalidParamError(direction, DIRECTION)
        self.setDirection(DIRECTION[direction])

    def get_direction(self) -> DirectionStr:
        """Return current direction.

        Returns:
            direction
        """
        return DIRECTION.inverse[self.direction()]

    def get_state(self) -> StateStr:
        """Return current state.

        Returns:
            state
        """
        return STATE.inverse[self.state()]

    def set_easing(
        self, easing_type: core.easingcurve.TypeStr | Callable[[float], float]
    ) -> core.EasingCurve:
        curve = core.EasingCurve()
        if isinstance(easing_type, str):
            curve.set_type(easing_type)
        else:
            curve.set_custom_type(easing_type)
        self.setEasingCurve(curve)
        return curve

    def get_easing(self) -> core.easingcurve.TypeStr | Callable[[float], float]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        return curve.get_custom_type() if typ == "custom" else typ


if __name__ == "__main__":
    timeline = TimeLine(finished=print, value_changed=print)

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


DirectionStr = Literal["forward", "backward"]

DIRECTION: bidict[DirectionStr, core.QTimeLine.Direction] = bidict(
    forward=core.QTimeLine.Direction.Forward,
    backward=core.QTimeLine.Direction.Backward,
)


StateStr = Literal["not_running", "paused", "running"]

STATE: bidict[StateStr, core.QTimeLine.State] = bidict(
    not_running=core.QTimeLine.State.NotRunning,
    paused=core.QTimeLine.State.Paused,
    running=core.QTimeLine.State.Running,
)


class TimeLine(core.ObjectMixin, core.QTimeLine):
    """Timeline for controlling animations."""

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"direction": DIRECTION}
        return maps

    def set_direction(self, direction: DirectionStr | core.QTimeLine.Direction):
        """Set the direction.

        Args:
            direction: direction
        """
        self.setDirection(DIRECTION.get_enum_value(direction))

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
        self,
        easing_type: core.easingcurve.TypeStr
        | core.QEasingCurve.Type
        | Callable[[float], float],
    ) -> core.EasingCurve:
        curve = core.EasingCurve()
        if callable(easing_type):
            curve.set_custom_type(easing_type)
        else:
            curve.set_type(easing_type)
        self.setEasingCurve(curve)
        return curve

    def get_easing(self) -> core.easingcurve.TypeStr | Callable[[float], float]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        return curve.get_custom_type() if typ == "custom" else typ


if __name__ == "__main__":
    timeline = TimeLine(finished=print, value_changed=print)

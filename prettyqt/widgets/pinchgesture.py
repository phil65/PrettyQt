from __future__ import annotations

from typing import Literal

from prettyqt import core, widgets
from prettyqt.utils import bidict


CHANGE_FLAGS = bidict(
    scale_factor=widgets.QPinchGesture.ChangeFlag.ScaleFactorChanged,
    rotation_angle=widgets.QPinchGesture.ChangeFlag.RotationAngleChanged,
    center_point=widgets.QPinchGesture.ChangeFlag.CenterPointChanged,
)

ChangeFlagStr = Literal["scale_factor", "rotation_angle", "center_point"]


class PinchGesture(widgets.GestureMixin, widgets.QPinchGesture):
    """Describes a pinch gesture made by the user."""

    def get_start_center_point(self) -> core.PointF:
        return core.PointF(self.startCenterPoint())

    def get_center_point(self) -> core.PointF:
        return core.PointF(self.centerPoint())

    def get_last_center_point(self) -> core.PointF:
        return core.PointF(self.lastCenterPoint())

    def get_change_flags(self) -> list[ChangeFlagStr]:
        return CHANGE_FLAGS.get_list(self.changeFlags())

    def set_change_flags(self, **kwargs):
        val = widgets.QPinchGesture.ChangeFlag(0)
        for k, v in kwargs.items():
            if v is True:
                val |= CHANGE_FLAGS[k]
        flag = widgets.QPinchGesture.ChangeFlag(val)  # type: ignore
        self.setChangeFlags(flag)  # type: ignore

    def get_total_change_flags(self) -> list[ChangeFlagStr]:
        return CHANGE_FLAGS.get_list(self.totalChangeFlags())

    def set_total_change_flags(self, **kwargs):
        val = widgets.QPinchGesture.ChangeFlag(0)
        for k, v in kwargs.items():
            if v is True:
                val |= CHANGE_FLAGS[k]
        flag = widgets.QPinchGesture.ChangeFlag(val)  # type: ignore
        self.setTotalChangeFlags(flag)  # type: ignore


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = PinchGesture()

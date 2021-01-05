from __future__ import annotations

from typing import List, Literal

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


CHANGE_FLAGS = bidict(
    scale_factor=QtWidgets.QPinchGesture.ScaleFactorChanged,
    rotation_angle=QtWidgets.QPinchGesture.RotationAngleChanged,
    center_point=QtWidgets.QPinchGesture.CenterPointChanged,
)

ChangeFlagStr = Literal["scale_factor", "rotation_angle", "center_point"]

QtWidgets.QPinchGesture.__bases__ = (widgets.Gesture,)


class PinchGesture(QtWidgets.QPinchGesture):
    def get_start_center_point(self) -> core.PointF:
        return core.PointF(self.startCenterPoint())

    def get_center_point(self) -> core.PointF:
        return core.PointF(self.centerPoint())

    def get_last_center_point(self) -> core.PointF:
        return core.PointF(self.lastCenterPoint())

    def get_change_flags(self) -> List[ChangeFlagStr]:
        return [k for k, v in CHANGE_FLAGS.items() if v & self.changeFlags()]

    def set_change_flags(self, **kwargs):
        flag = QtWidgets.QPinchGesture.ChangeFlags()
        for k, v in kwargs.items():
            if v is True:
                flag |= CHANGE_FLAGS[k]
        self.setChangeFlags(flag)

    def get_total_change_flags(self) -> List[ChangeFlagStr]:
        return [k for k, v in CHANGE_FLAGS.items() if v & self.totalChangeFlags()]

    def set_total_change_flags(self, **kwargs):
        flag = QtWidgets.QPinchGesture.ChangeFlags()
        for k, v in kwargs.items():
            if v is True:
                flag |= CHANGE_FLAGS[k]
        self.setTotalChangeFlags(flag)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    gesture = PinchGesture()

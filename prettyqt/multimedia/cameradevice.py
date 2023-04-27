from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict


POSITION = bidict(
    unspecified=QtMultimedia.QCameraDevice.Position.UnspecifiedPosition,
    back=QtMultimedia.QCameraDevice.Position.BackFace,
    front=QtMultimedia.QCameraDevice.Position.FrontFace,
)

PositionStr = Literal["unspecified", "back", "front"]


class CameraDevice(QtMultimedia.QCameraDevice):
    def get_position(self) -> PositionStr:
        return POSITION.inverse[self.position()]


if __name__ == "__main__":
    fmt = CameraDevice()

from __future__ import annotations

from typing import Literal

from prettyqt import multimedia
from prettyqt.utils import bidict


PositionStr = Literal["unspecified", "back", "front"]

POSITION: bidict[PositionStr, multimedia.QCameraDevice.Position] = bidict(
    unspecified=multimedia.QCameraDevice.Position.UnspecifiedPosition,
    back=multimedia.QCameraDevice.Position.BackFace,
    front=multimedia.QCameraDevice.Position.FrontFace,
)


class CameraDevice(multimedia.QCameraDevice):
    def get_position(self) -> PositionStr:
        return POSITION.inverse[self.position()]

    def get_video_formats(self) -> list[multimedia.CameraFormat]:
        return [multimedia.CameraFormat(i) for i in self.videoFormats()]


if __name__ == "__main__":
    fmt = CameraDevice()

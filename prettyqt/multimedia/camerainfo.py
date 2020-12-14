from typing import Optional

from qtpy import QtMultimedia


class CameraInfo(QtMultimedia.QCameraInfo):
    def __repr__(self):
        return f"{type(self).__name__}({self.deviceName()!r})"

    @classmethod
    def get_cameras(cls):
        return iter(cls(i) for i in cls.availableCameras())

    @classmethod
    def get_camera(cls, name: Optional[str] = None):
        if name is None:
            return cls(cls.defaultCamera())
        for cam in cls.get_cameras():
            if cam.deviceName() == name:
                return cam


if __name__ == "__main__":
    caminfo = CameraInfo()
    cams = caminfo.get_camera()
    print(cams)

from __future__ import annotations

from prettyqt.qt import QtMultimedia


class CameraFormat(QtMultimedia.QCameraFormat):
    def __bool__(self):
        return not self.isNull()


if __name__ == "__main__":
    fmt = CameraFormat()

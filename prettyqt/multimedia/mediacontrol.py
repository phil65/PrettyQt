from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtMultimedia


QtMultimedia.QMediaControl.__bases__ = (core.Object,)


class MediaControl(QtMultimedia.QMediaControl):
    pass

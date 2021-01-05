from __future__ import annotations

from prettyqt import multimedia
from prettyqt.qt import QtMultimediaWidgets


QtMultimediaWidgets.QVideoWidgetControl.__bases__ = (multimedia.MediaControl,)


class VideoWidgetControl(QtMultimediaWidgets.QVideoWidgetControl):
    pass

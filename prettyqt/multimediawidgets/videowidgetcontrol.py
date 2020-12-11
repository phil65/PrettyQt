from qtpy import QtMultimediaWidgets

from prettyqt import multimedia


QtMultimediaWidgets.QVideoWidgetControl.__bases__ = (multimedia.MediaControl,)


class VideoWidgetControl(QtMultimediaWidgets.QVideoWidgetControl):
    pass

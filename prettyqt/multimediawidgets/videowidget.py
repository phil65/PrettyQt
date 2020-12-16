from qtpy import QtCore, QtMultimediaWidgets

from prettyqt import multimedia, widgets


QtMultimediaWidgets.QVideoWidget.__bases__ = (
    widgets.Widget,
    multimedia.MediaBindableInterface,
)


class VideoWidget(QtMultimediaWidgets.QVideoWidget):
    def __init__(self, *args, **kwargs):
        self.doubleclick_for_fullscreen = False
        super().__init__(*args, **kwargs)

    def set_doubleclick_for_fullscreen(self, value: bool = True):
        self.doubleclick_for_fullscreen = value

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.doubleclick_for_fullscreen:
            self.setFullScreen(not self.isFullScreen())
            event.accept()
        return super().mouseDoubleClickEvent(event)

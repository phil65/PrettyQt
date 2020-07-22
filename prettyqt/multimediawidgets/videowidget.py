# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtMultimediaWidgets

from prettyqt import multimedia, widgets


QtMultimediaWidgets.QVideoWidget.__bases__ = (
    widgets.Widget,
    multimedia.MediaBindableInterface,
)


class VideoWidget(QtMultimediaWidgets.QVideoWidget):
    pass

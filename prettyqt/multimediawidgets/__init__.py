from __future__ import annotations

from prettyqt.qt.QtMultimediaWidgets import *  # noqa: F403

from .graphicsvideoitem import GraphicsVideoItem
from .videowidget import VideoWidget
from prettyqt.qt import QtMultimediaWidgets

QT_MODULE = QtMultimediaWidgets

__all__ = ["VideoWidget", "GraphicsVideoItem"]

"""Multimediawidgets module."""

from prettyqt.qt.QtMultimediaWidgets import *  # noqa: F403

from .videowidget import VideoWidget
from .graphicsvideoitem import GraphicsVideoItem

__all__ = ["VideoWidget", "GraphicsVideoItem"]

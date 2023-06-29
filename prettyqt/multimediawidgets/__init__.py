"""Multimediawidgets module."""

from prettyqt.qt.QtMultimediaWidgets import *  # noqa: F403

from .graphicsvideoitem import GraphicsVideoItem
from .videowidget import VideoWidget


__all__ = ["VideoWidget", "GraphicsVideoItem"]

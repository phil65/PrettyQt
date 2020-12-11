"""Multimediawidgets module."""

from prettyqt import core

if core.VersionNumber.get_qt_version() >= (5, 13, 0):
    from .videowidgetcontrol import VideoWidgetControl
from .videowidget import VideoWidget
from .graphicsvideoitem import GraphicsVideoItem

__all__ = ["VideoWidgetControl", "VideoWidget", "GraphicsVideoItem"]

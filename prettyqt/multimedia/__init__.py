"""A rich set of classes to handle multimedia content."""

from __future__ import annotations

from prettyqt.qt.QtMultimedia import *  # noqa: F403

from .mediametadata import MediaMetaData
from .audioformat import AudioFormat
from .audiodevice import AudioDevice
from .cameraformat import CameraFormat
from .cameradevice import CameraDevice
from .camera import Camera
from .mediaplayer import MediaPlayer
from .screencapture import ScreenCapture
from .mediarecorder import MediaRecorder
from prettyqt.qt import QtMultimedia

QT_MODULE = QtMultimedia

__all__ = [
    "AudioFormat",
    "AudioDevice",
    "Camera",
    "CameraDevice",
    "CameraFormat",
    "MediaPlayer",
    "MediaRecorder",
    "ScreenCapture",
    "MediaMetaData",
]

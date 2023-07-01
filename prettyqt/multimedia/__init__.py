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

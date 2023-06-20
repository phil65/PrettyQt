"""multimedia module.

contains QtMultimedia-based classes
"""

from .mediametadata import MediaMetadata
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
    "MediaMetadata",
]

"""multimedia module.

contains QtMultimedia-based classes
"""

from .audioformat import AudioFormat
from .cameraformat import CameraFormat
from .cameradevice import CameraDevice
from .camera import Camera
from .mediaplayer import MediaPlayer


__all__ = [
    "AudioFormat",
    "Camera",
    "CameraDevice",
    "CameraFormat",
    "MediaPlayer",
]

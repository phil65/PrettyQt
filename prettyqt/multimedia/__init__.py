"""multimedia module.

contains QtMultimedia-based classes
"""

from .audioformat import AudioFormat
from .audiodevice import AudioDevice
from .cameraformat import CameraFormat
from .cameradevice import CameraDevice
from .camera import Camera
from .mediaplayer import MediaPlayer


__all__ = [
    "AudioFormat",
    "AudioDevice",
    "Camera",
    "CameraDevice",
    "CameraFormat",
    "MediaPlayer",
]

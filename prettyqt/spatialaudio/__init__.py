"""Create sound scenes in 3D space containing different sound sources."""

from __future__ import annotations

from prettyqt.qt.QtSpatialAudio import *  # noqa: F403

from .ambientsound import AmbientSound
from .audioengine import AudioEngine
from .audiolistener import AudioListener
from .audioroom import AudioRoom
from .spatialsound import SpatialSound
from prettyqt.qt import QtSpatialAudio

QT_MODULE = QtSpatialAudio

__all__ = ["AmbientSound", "AudioEngine", "AudioListener", "AudioRoom", "SpatialSound"]

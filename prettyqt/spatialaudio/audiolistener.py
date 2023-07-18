from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import datatypes


class AudioListener(core.ObjectMixin, QtSpatialAudio.QAudioListener):
    """Defines the position and orientation of the person listening to a sound field."""

    def set_position(self, position: datatypes.Vector3DType):
        self.setPosition(datatypes.to_vector3d(position))

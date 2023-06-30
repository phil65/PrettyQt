from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import datatypes


class AudioListener(core.ObjectMixin, QtSpatialAudio.QAudioListener):
    def set_position(self, position: datatypes.Vector3DType):
        self.setPosition(datatypes.to_vector3d(position))

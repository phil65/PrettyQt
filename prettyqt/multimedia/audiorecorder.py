from __future__ import annotations

from prettyqt import multimedia
from prettyqt.qt import QtMultimedia


QtMultimedia.QAudioRecorder.__bases__ = (multimedia.MediaRecorder,)


class AudioRecorder(QtMultimedia.QAudioRecorder):
    pass

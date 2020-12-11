from qtpy import QtMultimedia

from prettyqt import multimedia


QtMultimedia.QAudioRecorder.__bases__ = (multimedia.MediaRecorder,)


class AudioRecorder(QtMultimedia.QAudioRecorder):
    pass

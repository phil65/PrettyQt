from __future__ import annotations

import pathlib

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import bidict, datatypes


LoopsStr = Literal["infinite", "once"]

LOOPS: bidict[LoopsStr, QtSpatialAudio.QAmbientSound.Loops] = bidict(
    infinite=QtSpatialAudio.QAmbientSound.Loops.Infinite,
    once=QtSpatialAudio.QAmbientSound.Loops.Once,
)


class AmbientSound(core.ObjectMixin, QtSpatialAudio.QAmbientSound):
    """A stereo overlay sound."""

    def set_source(self, source: datatypes.UrlType):
        self.setSource(datatypes.to_local_url(source))

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toString())


if __name__ == "__main__":
    engine = QtSpatialAudio.QAudioEngine()
    sound = AmbientSound(engine)
    sound.get_source()

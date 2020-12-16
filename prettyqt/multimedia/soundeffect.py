import pathlib
from typing import Union

from qtpy import QtCore, QtMultimedia

from prettyqt import core
from prettyqt.utils import bidict


STATUS = bidict(
    null=QtMultimedia.QSoundEffect.Null,
    loading=QtMultimedia.QSoundEffect.Loading,
    ready=QtMultimedia.QSoundEffect.Ready,
    error=QtMultimedia.QSoundEffect.Error,
)

QtMultimedia.QSoundEffect.__bases__ = (core.Object,)


class SoundEffect(QtMultimedia.QSoundEffect):
    def get_status(self) -> str:
        return STATUS.inverse[self.status()]

    def set_source(self, source: Union[str, pathlib.Path, QtCore.QUrl]):
        if not isinstance(source, QtCore.QUrl):
            source = core.Url.from_user_input(str(source))
        self.setSource(source)

    def get_source(self) -> core.Url:
        return core.Url(self.source())

    def set_loop_count(self, count: Union[str, int]):
        if count == "inf":
            count = QtMultimedia.QSoundEffect.Infinite
        self.setLoopCount(count)

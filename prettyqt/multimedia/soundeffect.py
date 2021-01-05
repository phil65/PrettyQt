from __future__ import annotations

import os
from typing import Literal, Union

from prettyqt import core
from prettyqt.qt import QtCore, QtMultimedia
from prettyqt.utils import bidict


STATUS = bidict(
    null=QtMultimedia.QSoundEffect.Null,
    loading=QtMultimedia.QSoundEffect.Loading,
    ready=QtMultimedia.QSoundEffect.Ready,
    error=QtMultimedia.QSoundEffect.Error,
)

StatusStr = Literal["null", "loading", "ready", "error"]

QtMultimedia.QSoundEffect.__bases__ = (core.Object,)


class SoundEffect(QtMultimedia.QSoundEffect):
    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]

    def set_source(self, source: Union[str, os.PathLike, QtCore.QUrl]):
        if not isinstance(source, QtCore.QUrl):
            source = core.Url.from_user_input(os.fspath(source))
        self.setSource(source)

    def get_source(self) -> core.Url:
        return core.Url(self.source())

    def set_loop_count(self, count: Union[Literal["inf"], int]):
        if count == "inf":
            count = QtMultimedia.QSoundEffect.Infinite
        self.setLoopCount(count)

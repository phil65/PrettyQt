from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


CACHE_MODE = bidict(
    none=QtGui.QMovie.CacheMode.CacheNone, all=QtGui.QMovie.CacheMode.CacheAll
)

CacheModeStr = Literal["none", "all"]

MOVIE_STATE = bidict(
    not_running=QtGui.QMovie.MovieState.NotRunning,
    paused=QtGui.QMovie.MovieState.Paused,
    running=QtGui.QMovie.MovieState.Running,
)

MovieStateStr = Literal["not_running", "paused", "running"]


QtGui.QMovie.__bases__ = (core.Object,)


class Movie(QtGui.QMovie):
    def __repr__(self):
        return f"{type(self).__name__}({self.fileName()!r}, {self.get_format()!r})"

    def serialize_fields(self):
        return dict(
            speed=self.speed(),
            cache_mode=self.get_cache_mode(),
            scaled_size=self.scaledSize(),
            background_color=self.backgroundColor(),
        )

    def set_cache_mode(self, mode: CacheModeStr):
        """Set cache mode.

        Args:
            mode: cache mode

        Raises:
            InvalidParamError: cache mode does not exist
        """
        if mode not in CACHE_MODE:
            raise InvalidParamError(mode, CACHE_MODE)
        self.setCacheMode(CACHE_MODE[mode])

    def get_cache_mode(self) -> CacheModeStr:
        """Get the current cache mode.

        Returns:
            cache mode
        """
        return CACHE_MODE.inverse[self.cacheMode()]

    def get_state(self) -> MovieStateStr:
        """Get the current state.

        Returns:
            state
        """
        return MOVIE_STATE.inverse[self.state()]

    def get_format(self) -> bytes:
        return bytes(self.format())

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        return [bytes(i).decode() for i in cls.supportedFormats()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    movie = Movie()
    print(repr(movie))

from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, get_repr


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


class Movie(core.ObjectMixin, QtGui.QMovie):
    def __repr__(self):
        return get_repr(self, self.fileName(), self.get_format())

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

    def get_format(self) -> str:
        return self.format().data().decode()

    @classmethod
    def get_supported_formats(cls) -> list[str]:
        return [i.data().decode() for i in cls.supportedFormats()]


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    movie = Movie()
    print(repr(movie.get_format()))

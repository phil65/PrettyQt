from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


CacheModeStr = Literal["none", "all"]

CACHE_MODE: bidict[CacheModeStr, QtGui.QMovie.CacheMode] = bidict(
    none=QtGui.QMovie.CacheMode.CacheNone, all=QtGui.QMovie.CacheMode.CacheAll
)

MovieStateStr = Literal["not_running", "paused", "running"]

MOVIE_STATE: bidict[MovieStateStr, QtGui.QMovie.MovieState] = bidict(
    not_running=QtGui.QMovie.MovieState.NotRunning,
    paused=QtGui.QMovie.MovieState.Paused,
    running=QtGui.QMovie.MovieState.Running,
)


class Movie(core.ObjectMixin, QtGui.QMovie):
    def __repr__(self):
        return get_repr(self, self.fileName(), self.get_format())

    def set_cache_mode(self, mode: CacheModeStr | QtGui.QMovie.CacheMode):
        """Set cache mode.

        Args:
            mode: cache mode
        """
        self.setCacheMode(CACHE_MODE.get_enum_value(mode))

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

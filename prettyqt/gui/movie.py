# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError

CACHE_MODES = bidict(none=QtGui.QMovie.CacheNone, all=QtGui.QMovie.CacheAll)

MOVIE_STATES = bidict(
    not_running=QtGui.QMovie.NotRunning,
    paused=QtGui.QMovie.Paused,
    running=QtGui.QMovie.Running,
)

QtGui.QMovie.__bases__ = (core.Object,)


class Movie(QtGui.QMovie):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def serialize_fields(self):
        return dict(
            speed=self.speed(),
            cache_mode=self.get_cache_mode(),
            scaled_size=self.scaledSize(),
            background_color=self.backgroundColor(),
        )

    def set_cache_mode(self, mode: str):
        """Set cache mode.

        Valid values for cache_mode: "none", "all"

        Args:
            cache_mode: cache mode

        Raises:
            InvalidParamError: cache mode does not exist
        """
        if mode not in CACHE_MODES:
            raise InvalidParamError(mode, CACHE_MODES)
        self.setCacheMode(CACHE_MODES[mode])

    def get_cache_mode(self) -> str:
        """Get the current cache mode.

        Possible values: "none", "all"

        Returns:
            cache mode
        """
        return CACHE_MODES.inv[self.cacheMode()]


if __name__ == "__main__":
    movie = Movie()

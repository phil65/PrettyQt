# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtMultimedia

from prettyqt import multimedia
from prettyqt.utils import bidict


STATES = bidict(
    stopped=QtMultimedia.QMediaPlayer.StoppedState,
    playing=QtMultimedia.QMediaPlayer.PlayingState,
    paused=QtMultimedia.QMediaPlayer.PausedState,
)

ERRORS = bidict(
    none=QtMultimedia.QMediaPlayer.NoError,
    resource=QtMultimedia.QMediaPlayer.ResourceError,
    format=QtMultimedia.QMediaPlayer.FormatError,
    network=QtMultimedia.QMediaPlayer.NetworkError,
    access_denies=QtMultimedia.QMediaPlayer.AccessDeniedError,
    service_missing=QtMultimedia.QMediaPlayer.ServiceMissingError,
)

MEDIA_STATUS = bidict(
    unknown=QtMultimedia.QMediaPlayer.UnknownMediaStatus,
    no_media=QtMultimedia.QMediaPlayer.NoMedia,
    loading=QtMultimedia.QMediaPlayer.LoadingMedia,
    loaded=QtMultimedia.QMediaPlayer.LoadedMedia,
    stalled=QtMultimedia.QMediaPlayer.StalledMedia,
    buffering=QtMultimedia.QMediaPlayer.BufferingMedia,
    buffered=QtMultimedia.QMediaPlayer.BufferedMedia,
    end=QtMultimedia.QMediaPlayer.EndOfMedia,
    invalid=QtMultimedia.QMediaPlayer.InvalidMedia,
)

QtMultimedia.QMediaPlayer.__bases__ = (multimedia.MediaObject,)


class MediaPlayer(QtMultimedia.QMediaPlayer):
    def get_state(self) -> str:
        """returns current state

        Possible values: "stopped", "playing", "paused"

        Returns:
            state
        """
        return STATES.inv[self.state()]

    def get_media_status(self) -> str:
        """returns current media status

        Possible values: "unknown", "no_media", "loading", "loaded", "stalled",
                         "buffering", "buffered", "end", "invalid"

        Returns:
            media status
        """
        return MEDIA_STATUS.inv[self.mediaStatus()]

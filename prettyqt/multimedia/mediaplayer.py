from __future__ import annotations

from typing import Literal

from prettyqt import multimedia
from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict


STATES = bidict(
    stopped=QtMultimedia.QMediaPlayer.State.StoppedState,
    playing=QtMultimedia.QMediaPlayer.State.PlayingState,
    paused=QtMultimedia.QMediaPlayer.State.PausedState,
)

StateStr = Literal["stopped", "playing", "paused"]

ERROR = bidict(
    none=QtMultimedia.QMediaPlayer.Error.NoError,
    resource=QtMultimedia.QMediaPlayer.Error.ResourceError,
    format=QtMultimedia.QMediaPlayer.Error.FormatError,
    network=QtMultimedia.QMediaPlayer.Error.NetworkError,
    access_denied=QtMultimedia.QMediaPlayer.Error.AccessDeniedError,
    service_missing=QtMultimedia.QMediaPlayer.Error.ServiceMissingError,
)

ErrorStr = Literal[
    "none", "resource", "format", "network", "access_denied", "service_missing"
]

MEDIA_STATUS = bidict(
    unknown=QtMultimedia.QMediaPlayer.MediaStatus.UnknownMediaStatus,
    no_media=QtMultimedia.QMediaPlayer.MediaStatus.NoMedia,
    loading=QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia,
    loaded=QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia,
    stalled=QtMultimedia.QMediaPlayer.MediaStatus.StalledMedia,
    buffering=QtMultimedia.QMediaPlayer.MediaStatus.BufferingMedia,
    buffered=QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia,
    end=QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia,
    invalid=QtMultimedia.QMediaPlayer.MediaStatus.InvalidMedia,
)

MediaStatusStr = Literal[
    "unknown",
    "no_media",
    "loading",
    "loaded",
    "stalled",
    "buffering",
    "buffered",
    "end",
    "invalid",
]

QtMultimedia.QMediaPlayer.__bases__ = (multimedia.MediaObject,)


class MediaPlayer(QtMultimedia.QMediaPlayer):
    def get_state(self) -> StateStr:
        """Return current state.

        Returns:
            state
        """
        return STATES.inverse[self.state()]

    def get_media_status(self) -> MediaStatusStr:
        """Return current media status.

        Returns:
            media status
        """
        return MEDIA_STATUS.inverse[self.mediaStatus()]

    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERROR.inverse[self.error()]

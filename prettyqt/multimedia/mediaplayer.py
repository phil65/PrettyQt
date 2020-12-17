from typing import Literal

from qtpy import QtMultimedia

from prettyqt import multimedia
from prettyqt.utils import bidict


STATES = bidict(
    stopped=QtMultimedia.QMediaPlayer.StoppedState,
    playing=QtMultimedia.QMediaPlayer.PlayingState,
    paused=QtMultimedia.QMediaPlayer.PausedState,
)

StateStr = Literal["stopped", "playing", "paused"]

ERROR = bidict(
    none=QtMultimedia.QMediaPlayer.NoError,
    resource=QtMultimedia.QMediaPlayer.ResourceError,
    format=QtMultimedia.QMediaPlayer.FormatError,
    network=QtMultimedia.QMediaPlayer.NetworkError,
    access_denied=QtMultimedia.QMediaPlayer.AccessDeniedError,
    service_missing=QtMultimedia.QMediaPlayer.ServiceMissingError,
)

ErrorStr = Literal[
    "none", "resource", "format", "network", "access_denied", "service_missing"
]

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

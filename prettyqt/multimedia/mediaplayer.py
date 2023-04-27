from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtMultimedia
from prettyqt.utils import bidict, datatypes


PLAYBACK_STATE = bidict(
    stopped=QtMultimedia.QMediaPlayer.PlaybackState.StoppedState,
    playing=QtMultimedia.QMediaPlayer.PlaybackState.PlayingState,
    paused=QtMultimedia.QMediaPlayer.PlaybackState.PausedState,
)

PlaybackStateStr = Literal["stopped", "playing", "paused"]

ERROR = bidict(
    none=QtMultimedia.QMediaPlayer.Error.NoError,
    resource=QtMultimedia.QMediaPlayer.Error.ResourceError,
    format=QtMultimedia.QMediaPlayer.Error.FormatError,
    network=QtMultimedia.QMediaPlayer.Error.NetworkError,
    access_denied=QtMultimedia.QMediaPlayer.Error.AccessDeniedError,
)

ErrorStr = Literal["none", "resource", "format", "network", "access_denied"]

MEDIA_STATUS = bidict(
    none=QtMultimedia.QMediaPlayer.MediaStatus.NoMedia,
    loading=QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia,
    loaded=QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia,
    stalled=QtMultimedia.QMediaPlayer.MediaStatus.StalledMedia,
    buffering=QtMultimedia.QMediaPlayer.MediaStatus.BufferingMedia,
    buffered=QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia,
    end=QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia,
    invalid=QtMultimedia.QMediaPlayer.MediaStatus.InvalidMedia,
)

MediaStatusStr = Literal[
    "none",
    "loading",
    "loaded",
    "stalled",
    "buffering",
    "buffered",
    "end",
    "invalid",
]


class MediaPlayer(core.ObjectMixin, QtMultimedia.QMediaPlayer):
    def set_source_device(
        self, device: QtCore.QIODevice, url: datatypes.UrlType | None = None
    ):
        if not isinstance(url, QtCore.QUrl):
            url = QtCore.QUrl(url)
        elif url is None:
            url = QtCore.QUrl()
        self.setSourceDevice(device, url)

    def set_source(self, url: datatypes.UrlType):
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        self.setSource(url)

    def get_source(self) -> core.Url | None:
        url = self.source()
        return core.Url(url) if url.isValid() else None

    def get_playback_state(self) -> PlaybackStateStr:
        """Return current playback state.

        Returns:
            playback state
        """
        return PLAYBACK_STATE.inverse[self.playbackState()]

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


if __name__ == "__main__":
    player = MediaPlayer()
    source = player.get_source()
    print(source.isValid())

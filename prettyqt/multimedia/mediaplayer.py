from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict, datatypes


PlaybackStateStr = Literal["stopped", "playing", "paused"]

PLAYBACK_STATE: bidict[
    PlaybackStateStr, QtMultimedia.QMediaPlayer.PlaybackState
] = bidict(
    stopped=QtMultimedia.QMediaPlayer.PlaybackState.StoppedState,
    playing=QtMultimedia.QMediaPlayer.PlaybackState.PlayingState,
    paused=QtMultimedia.QMediaPlayer.PlaybackState.PausedState,
)

ErrorStr = Literal["none", "resource", "format", "network", "access_denied"]

ERROR: bidict[ErrorStr, QtMultimedia.QMediaPlayer.Error] = bidict(
    none=QtMultimedia.QMediaPlayer.Error.NoError,
    resource=QtMultimedia.QMediaPlayer.Error.ResourceError,
    format=QtMultimedia.QMediaPlayer.Error.FormatError,
    network=QtMultimedia.QMediaPlayer.Error.NetworkError,
    access_denied=QtMultimedia.QMediaPlayer.Error.AccessDeniedError,
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

MEDIA_STATUS: bidict[MediaStatusStr, QtMultimedia.QMediaPlayer.MediaStatus] = bidict(
    none=QtMultimedia.QMediaPlayer.MediaStatus.NoMedia,
    loading=QtMultimedia.QMediaPlayer.MediaStatus.LoadingMedia,
    loaded=QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia,
    stalled=QtMultimedia.QMediaPlayer.MediaStatus.StalledMedia,
    buffering=QtMultimedia.QMediaPlayer.MediaStatus.BufferingMedia,
    buffered=QtMultimedia.QMediaPlayer.MediaStatus.BufferedMedia,
    end=QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia,
    invalid=QtMultimedia.QMediaPlayer.MediaStatus.InvalidMedia,
)


class MediaPlayer(core.ObjectMixin, QtMultimedia.QMediaPlayer):
    def set_source_device(
        self, device: core.QIODevice, url: datatypes.UrlType | None = None
    ):
        url = datatypes.to_local_url(url)
        self.setSourceDevice(device, url)

    def set_source(self, url: datatypes.UrlType):
        url = datatypes.to_local_url(url)
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

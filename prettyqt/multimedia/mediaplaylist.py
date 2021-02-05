from __future__ import annotations

import os
from typing import Iterator, Literal

from prettyqt import core, multimedia
from prettyqt.qt import QtMultimedia
from prettyqt.utils import InvalidParamError, bidict


PLAYBACK_MODE = bidict(
    item_once=QtMultimedia.QMediaPlaylist.CurrentItemOnce,
    item_in_loop=QtMultimedia.QMediaPlaylist.CurrentItemInLoop,
    sequential=QtMultimedia.QMediaPlaylist.Sequential,
    loop=QtMultimedia.QMediaPlaylist.Loop,
    random=QtMultimedia.QMediaPlaylist.Random,
)

PlaybackModeStr = Literal["item_once", "item_in_loop", "sequential", "loop", "random"]

QtMultimedia.QMediaPlaylist.__bases__ = (core.Object, multimedia.MediaBindableInterface)


class MediaPlaylist(QtMultimedia.QMediaPlaylist):
    playback_mode_changed = core.Signal(str)

    def __len__(self) -> int:
        return self.mediaCount()

    def __getitem__(self, item: int) -> multimedia.MediaContent:
        return multimedia.MediaContent(self.media(item))

    def __delitem__(self, item: int):
        self.removeMedia(item)

    def __iter__(self) -> Iterator[multimedia.MediaContent]:
        return iter(self[i] for i in range(self.mediaCount()))

    # def serialize(self) -> Dict[str, Any]:
    #     return dict(current_index=self.currentIndex(),
    #                 playback_mode=self.get_playback_mode(),
    #                 items=list(self))

    def add_media(self, media: os.PathLike | str, pos: int | None = None) -> bool:
        url = core.Url(os.fspath(media))
        mediacontent = multimedia.MediaContent(url)
        if pos is None:
            return self.addMedia(mediacontent)
        else:
            return self.insertMedia(pos, mediacontent)

    def get_media_url(self, index: int) -> core.Url:
        url = self.media(index).request().url()
        return core.Url(url)

    def set_playback_mode(self, mode: PlaybackModeStr):
        """Set playback mode for given item view.

        Args:
            mode: playback mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in PLAYBACK_MODE:
            raise InvalidParamError(mode, PLAYBACK_MODE)
        self.setPlaybackMode(PLAYBACK_MODE[mode])

    def get_playback_mode(self) -> PlaybackModeStr:
        """Return current playback mode.

        Returns:
            playback mode
        """
        return PLAYBACK_MODE.inverse[self.playbackMode()]

    # def on_playback_mode_changed(self, mode: int):
    #     self.playback_mode_changed.emit(PLAYBACK_MODE.inverse[mode])

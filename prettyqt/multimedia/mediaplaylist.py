import pathlib
from typing import Iterator, Optional, Union

from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import InvalidParamError, bidict


PLAYBACK_MODES = bidict(
    item_once=QtMultimedia.QMediaPlaylist.CurrentItemOnce,
    item_in_loop=QtMultimedia.QMediaPlaylist.CurrentItemInLoop,
    sequential=QtMultimedia.QMediaPlaylist.Sequential,
    loop=QtMultimedia.QMediaPlaylist.Loop,
    random=QtMultimedia.QMediaPlaylist.Random,
)

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

    # def serialize(self):
    #     return dict(current_index=self.currentIndex(),
    #                 playback_mode=self.get_playback_mode(),
    #                 items=list(self))

    def add_media(
        self, media: Union[pathlib.Path, str], pos: Optional[int] = None
    ) -> bool:
        url = core.Url(str(media))
        mediacontent = multimedia.MediaContent(url)
        if pos is None:
            return self.addMedia(mediacontent)
        else:
            return self.insertMedia(pos, mediacontent)

    def get_media_url(self, index: int) -> core.Url:
        url = self.media(index).request().url()
        return core.Url(url)

    def set_playback_mode(self, mode: str):
        """Set playback mode for given item view.

        Allowed values are "item_once", "item_in_loop", "sequential", "loop", "random"

        Args:
            mode: playback mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in PLAYBACK_MODES:
            raise InvalidParamError(mode, PLAYBACK_MODES)
        self.setPlaybackMode(PLAYBACK_MODES[mode])

    def get_playback_mode(self) -> str:
        """Return current playback mode.

        Possible values: "item_once", "item_in_loop", "sequential", "loop", "random"

        Returns:
            playback mode
        """
        return PLAYBACK_MODES.inverse[self.playbackMode()]

    # def on_playback_mode_changed(self, mode: int):
    #     self.playback_mode_changed.emit(PLAYBACK_MODES.inverse[mode])

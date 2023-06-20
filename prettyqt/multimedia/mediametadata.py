from __future__ import annotations

from collections.abc import MutableMapping
from typing import Literal

from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict, datatypes, get_repr


KEY = bidict(
    title=QtMultimedia.QMediaMetaData.Key.Title,
    author=QtMultimedia.QMediaMetaData.Key.Author,
    comment=QtMultimedia.QMediaMetaData.Key.Comment,
    description=QtMultimedia.QMediaMetaData.Key.Description,
    genre=QtMultimedia.QMediaMetaData.Key.Genre,
    date=QtMultimedia.QMediaMetaData.Key.Date,
    language=QtMultimedia.QMediaMetaData.Key.Language,
    publisher=QtMultimedia.QMediaMetaData.Key.Publisher,
    copyright=QtMultimedia.QMediaMetaData.Key.Copyright,
    url=QtMultimedia.QMediaMetaData.Key.Url,
    duration=QtMultimedia.QMediaMetaData.Key.Duration,
    media_type=QtMultimedia.QMediaMetaData.Key.MediaType,
    file_format=QtMultimedia.QMediaMetaData.Key.FileFormat,
    audio_bit_rate=QtMultimedia.QMediaMetaData.Key.AudioBitRate,
    audio_codec=QtMultimedia.QMediaMetaData.Key.AudioCodec,
    video_bitrate=QtMultimedia.QMediaMetaData.Key.VideoBitRate,
    video_codec=QtMultimedia.QMediaMetaData.Key.VideoCodec,
    video_frame_rate=QtMultimedia.QMediaMetaData.Key.VideoFrameRate,
    album_title=QtMultimedia.QMediaMetaData.Key.AlbumTitle,
    album_artist=QtMultimedia.QMediaMetaData.Key.AlbumArtist,
    contributing_artist=QtMultimedia.QMediaMetaData.Key.ContributingArtist,
    track_number=QtMultimedia.QMediaMetaData.Key.TrackNumber,
    composer=QtMultimedia.QMediaMetaData.Key.Composer,
    lead_performer=QtMultimedia.QMediaMetaData.Key.LeadPerformer,
    thumbnail_image=QtMultimedia.QMediaMetaData.Key.ThumbnailImage,
    cover_art_image=QtMultimedia.QMediaMetaData.Key.CoverArtImage,
    orientation=QtMultimedia.QMediaMetaData.Key.Orientation,
    resolution=QtMultimedia.QMediaMetaData.Key.Resolution,
)

KeyStr = Literal[
    "title",
    "author",
    "comment",
    "description",
    "genre",
    "date",
    "language",
    "publisher",
    "copyright",
    "url",
    "duration",
    "media_type",
    "file_format",
    "audio_bit_rate",
    "audio_codec",
    "video_bitrate",
    "video_codec",
    "video_frame_rate",
    "album_title",
    "album_artist",
    "contributing_artist",
    "track_number",
    "composer",
    "lead_performer",
    "thumbnail_image",
    "cover_art_image",
    "orientation",
    "resolution",
]


class MediaMetaData(
    QtMultimedia.QMediaMetaData,
    MutableMapping,
    metaclass=datatypes.QABCMeta,
):
    def __repr__(self):
        return get_repr(self, dict(self))

    def __setitem__(self, key: KeyStr, value: datatypes.Variant):
        if isinstance(key, str):
            key = KEY[key]
        self.insert(key, value)

    def __getitem__(self, key: KeyStr) -> datatypes.Variant:
        if isinstance(key, str):
            key = KEY[key]
        if key not in self.keys():
            raise KeyError(key)
        return self.value(key)

    def __delitem__(self, key: KeyStr):
        if isinstance(key, str):
            key = KEY[key]
        self.remove(key)

    def __bool__(self):
        return not self.isEmpty()

    def __iter__(self):
        return iter(self.keys())


if __name__ == "__main__":
    from prettyqt import core
    metadata = MediaMetaData()
    metadata["resolution"] = core.QSize(10, 10)
    print(metadata)

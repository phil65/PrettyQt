from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterator, Tuple

from qtpy import QtMultimedia

from prettyqt.utils import InvalidParamError, bidict


QUALITIES = bidict(
    very_low=QtMultimedia.QMultimedia.VeryLowQuality,
    low=QtMultimedia.QMultimedia.LowQuality,
    normal=QtMultimedia.QMultimedia.NormalQuality,
    high=QtMultimedia.QMultimedia.HighQuality,
    very_high=QtMultimedia.QMultimedia.VeryHighQuality,
)


@dataclass
class Settings:
    codec: str
    encoding_options: Dict[str, Any]
    quality: str
    resolution: Tuple[int, int]


class ImageEncoderSettings(QtMultimedia.QImageEncoderSettings):
    def __getitem__(self, index: str):
        return self.to_dict()[index]

    def __setitem__(self, index: str, value):
        if index == "codec":
            self.setCodec(value)
        elif index == "encoding_options":
            self.setEncodingOptions(value)
        elif index == "resolution":
            self.setResolution(*value)
        elif index == "quality":
            self.set_quality(value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict().keys())

    def __len__(self):
        return len(self.to_dict())

    def set_quality(self, quality: str):
        if quality not in QUALITIES:
            raise InvalidParamError(quality, QUALITIES)
        self.setQuality(QUALITIES[quality])

    def get_quality(self) -> str:
        return QUALITIES.inverse[self.quality()]

    def to_dataclass(self) -> Settings:
        size = self.resolution()
        return Settings(
            codec=self.codec(),
            encoding_options=self.encodingOptions(),
            resolution=(size.width(), size.height()),
            quality=self.get_quality(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.to_dataclass())

    @classmethod
    def from_dataclass(cls, data: Settings) -> ImageEncoderSettings:
        instance = cls()
        instance.setCodec(data.codec)
        instance.setEncodingOptions(data.encoding_options)
        instance.setResolution(*data.resolution)
        instance.set_quality(data.quality)
        return instance

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ImageEncoderSettings:
        settings = Settings(**data)
        return cls.from_dataclass(settings)

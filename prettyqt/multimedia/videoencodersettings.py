# -*- coding: utf-8 -*-
"""
"""
from dataclasses import dataclass, asdict
from typing import Tuple

from qtpy import QtMultimedia, QtCore

from prettyqt.utils import bidict

QUALITIES = bidict(
    very_low=QtMultimedia.QMultimedia.VeryLowQuality,
    low=QtMultimedia.QMultimedia.LowQuality,
    normal=QtMultimedia.QMultimedia.NormalQuality,
    high=QtMultimedia.QMultimedia.HighQuality,
    very_high=QtMultimedia.QMultimedia.VeryHighQuality,
)

ENCODING_MODES = bidict(
    constant_quality=QtMultimedia.QMultimedia.ConstantQualityEncoding,
    constant_bit_rate=QtMultimedia.QMultimedia.ConstantBitRateEncoding,
    average_bit_rate=QtMultimedia.QMultimedia.AverageBitRateEncoding,
    two_pass_encoding=QtMultimedia.QMultimedia.TwoPassEncoding,
)


@dataclass
class Settings(object):
    bitrate: int
    codec: str
    encoding_mode: str
    encoding_options: dict
    quality: str
    frame_rate: float
    resolution: Tuple[int, int]


class VideoEncoderSettings(QtMultimedia.QVideoEncoderSettings):
    def set_encoding_mode(self, mode: str):
        if mode not in ENCODING_MODES:
            raise ValueError()
        self.setEncodingMode(ENCODING_MODES[mode])

    def get_encoding_mode(self) -> str:
        return ENCODING_MODES.inv[self.encodingMode()]

    def set_quality(self, quality: str):
        if quality not in QUALITIES:
            raise ValueError()
        self.setQuality(QUALITIES[quality])

    def get_quality(self) -> str:
        return QUALITIES.inv[self.quality()]

    def to_dataclass(self) -> Settings:
        size = self.resolution()
        return Settings(
            bitrate=self.bitRate(),
            codec=self.codec(),
            encoding_mode=self.get_encoding_mode(),
            encoding_options=self.encodingOptions(),
            frame_rate=self.frameRate(),
            resolution=(size.width(), size.height()),
            quality=self.get_quality(),
        )

    def to_dict(self) -> dict:
        return asdict(self.to_dataclass())

    @classmethod
    def from_dataclass(cls, data: Settings) -> "VideoEncoderSettings":
        instance = cls()
        instance.setBitRate(data.bitrate)
        instance.setCodec(data.codec)
        instance.set_encoding_mode(data.encoding_mode)
        instance.setEncodingOptions(data.encoding_options)
        instance.setResolution(QtCore.QSize(*data.resolution))
        instance.set_quality(data.quality)
        return instance

    @classmethod
    def from_dict(cls, data: dict) -> "VideoEncoderSettings":
        settings = Settings(**data)
        return cls.from_dataclass(settings)

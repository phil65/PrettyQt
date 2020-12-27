from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterator, Literal

from prettyqt.qt import QtMultimedia
from prettyqt.utils import InvalidParamError, bidict


QUALITY = bidict(
    very_low=QtMultimedia.QMultimedia.VeryLowQuality,
    low=QtMultimedia.QMultimedia.LowQuality,
    normal=QtMultimedia.QMultimedia.NormalQuality,
    high=QtMultimedia.QMultimedia.HighQuality,
    very_high=QtMultimedia.QMultimedia.VeryHighQuality,
)

QualityStr = Literal["very_low", "low", "normal", "high", "very_high"]

ENCODING_MODE = bidict(
    constant_quality=QtMultimedia.QMultimedia.ConstantQualityEncoding,
    constant_bit_rate=QtMultimedia.QMultimedia.ConstantBitRateEncoding,
    average_bit_rate=QtMultimedia.QMultimedia.AverageBitRateEncoding,
    two_pass_encoding=QtMultimedia.QMultimedia.TwoPassEncoding,
)

EncodingModeStr = Literal[
    "constant_quality", "constant_bit_rate", "average_bit_rate", "two_pass_encoding"
]


@dataclass
class Settings:
    bitrate: int
    channel_count: int
    codec: str
    encoding_mode: EncodingModeStr
    encoding_options: Dict[str, Any]
    quality: QualityStr
    sample_rate: int


class AudioEncoderSettings(QtMultimedia.QAudioEncoderSettings):
    def __getitem__(self, index: str):
        return self.to_dict()[index]

    def __setitem__(self, index: str, value):
        if index == "bitrate":
            self.setBitRate(value)
        elif index == "channel_count":
            self.setChannelCount(value)
        elif index == "codec":
            self.setCodec(value)
        elif index == "encoding_mode":
            self.set_encoding_mode(value)
        elif index == "encoding_options":
            self.setEncodingOptions(value)
        elif index == "quality":
            self.set_quality(value)
        elif index == "sample_rate":
            self.setSampleRate(value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict().keys())

    def __len__(self):
        return len(self.to_dict())

    def set_encoding_mode(self, mode: EncodingModeStr):
        if mode not in ENCODING_MODE:
            raise InvalidParamError(mode, ENCODING_MODE)
        self.setEncodingMode(ENCODING_MODE[mode])

    def get_encoding_mode(self) -> EncodingModeStr:
        return ENCODING_MODE.inverse[self.encodingMode()]

    def set_quality(self, quality: QualityStr):
        if quality not in QUALITY:
            raise InvalidParamError(quality, QUALITY)
        self.setQuality(QUALITY[quality])

    def get_quality(self) -> QualityStr:
        return QUALITY.inverse[self.quality()]

    def to_dataclass(self) -> Settings:
        return Settings(
            bitrate=self.bitRate(),
            channel_count=self.channelCount(),
            codec=self.codec(),
            encoding_mode=self.get_encoding_mode(),
            encoding_options=self.encodingOptions(),
            quality=self.get_quality(),
            sample_rate=self.sampleRate(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.to_dataclass())

    @classmethod
    def from_dataclass(cls, data: Settings) -> AudioEncoderSettings:
        instance = cls()
        instance.setBitRate(data.bitrate)
        instance.setChannelCount(data.channel_count)
        instance.setCodec(data.codec)
        instance.set_encoding_mode(data.encoding_mode)
        instance.setEncodingOptions(data.encoding_options)
        instance.set_quality(data.quality)
        instance.setSampleRate(data.sample_rate)
        return instance

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AudioEncoderSettings:
        settings = Settings(**data)
        return cls.from_dataclass(settings)

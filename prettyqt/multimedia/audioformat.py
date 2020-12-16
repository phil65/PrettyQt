from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterator

from qtpy import QtMultimedia

from prettyqt.utils import InvalidParamError, bidict


ENDIAN = bidict(
    big_endian=QtMultimedia.QAudioFormat.BigEndian,
    little_endian=QtMultimedia.QAudioFormat.LittleEndian,
)

SAMPLE_TYPES = bidict(
    unknown=QtMultimedia.QAudioFormat.Unknown,
    signed_int=QtMultimedia.QAudioFormat.SignedInt,
    unsigned_int=QtMultimedia.QAudioFormat.UnSignedInt,
    float=QtMultimedia.QAudioFormat.Float,
)


@dataclass
class Settings:
    sample_rate: int
    channel_count: int
    sample_size: int
    byte_order: str
    sample_type: str
    codec: str


class AudioFormat(QtMultimedia.QAudioFormat):
    def __getitem__(self, index: str):
        return self.to_dict()[index]

    def __setitem__(self, index: str, value):
        if index == "sample_rate":
            self.setSampleRate(value)
        elif index == "channel_count":
            self.setChannelCount(value)
        elif index == "sample_size":
            self.setSampleSize(value)
        elif index == "byte_order":
            self.set_byte_order(value)
        elif index == "sample_type":
            self.set_sample_type(value)
        elif index == "codec":
            self.setCodec(value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict().keys())

    def __len__(self):
        return len(self.to_dict())

    def set_sample_type(self, mode: str):
        if mode not in SAMPLE_TYPES:
            raise InvalidParamError(mode, SAMPLE_TYPES)
        self.setSampleType(SAMPLE_TYPES[mode])

    def get_sample_type(self) -> str:
        return SAMPLE_TYPES.inverse[self.sampleType()]

    def set_byte_order(self, order: str):
        if order not in ENDIAN:
            raise InvalidParamError(order, ENDIAN)
        self.setByteOrder(ENDIAN[order])

    def get_byte_order(self) -> str:
        return ENDIAN.inverse[self.byteOrder()]

    def to_dataclass(self) -> Settings:
        return Settings(
            sample_rate=self.sampleRate(),
            channel_count=self.channelCount(),
            sample_type=self.get_sample_type(),
            byte_order=self.get_byte_order(),
            sample_size=self.sampleSize(),
            codec=self.codec(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self.to_dataclass())

    @classmethod
    def from_dataclass(cls, data: Settings) -> AudioFormat:
        instance = cls()
        instance.setSampleRate(data.sample_rate)
        instance.setChannelCount(data.channel_count)
        instance.set_sample_type(data.sample_type)
        instance.set_byte_order(data.byte_order)
        instance.setSampleSize(data.sample_size)
        instance.setCodec(data.codec)
        return instance

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AudioFormat:
        settings = Settings(**data)
        return cls.from_dataclass(settings)


if __name__ == "__main__":
    fmt = AudioFormat()

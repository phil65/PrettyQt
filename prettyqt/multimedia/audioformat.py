from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtMultimedia
from prettyqt.utils import InvalidParamError, bidict


SAMPLE_FORMAT = bidict(
    unknown=QtMultimedia.QAudioFormat.SampleFormat.Unknown,
    u_int8=QtMultimedia.QAudioFormat.SampleFormat.UInt8,
    int16=QtMultimedia.QAudioFormat.SampleFormat.Int16,
    int32=QtMultimedia.QAudioFormat.SampleFormat.Int32,
    float=QtMultimedia.QAudioFormat.SampleFormat.Float,
)

SampleFormatStr = Literal["unknown", "u_int8", "int16", "int32", "float"]

CHANNEL_CONFIG = bidict(
    **{
        "unknown": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigUnknown,
        "mono": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigMono,
        "stereo": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigStereo,
        "2_1": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfig2Dot1,
        "3_0": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfig3Dot0,
        "3_1": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfig3Dot1,
        "5_0": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigSurround5Dot0,
        "5_1": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigSurround5Dot1,
        "7_0": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigSurround7Dot0,
        "7_1": QtMultimedia.QAudioFormat.ChannelConfig.ChannelConfigSurround7Dot1,
    }
)

ChannelConfigStr = Literal[
    "unknown", "mono", "stereo", "2_1", "3_0", "3_1", "5_0", "5_1", "7_0", "7_1"
]


class AudioFormat(QtMultimedia.QAudioFormat):
    def set_sample_format(self, mode: SampleFormatStr):
        if mode not in SAMPLE_FORMAT:
            raise InvalidParamError(mode, SAMPLE_FORMAT)
        self.setSampleFormat(SAMPLE_FORMAT[mode])

    def get_sample_format(self) -> SampleFormatStr:
        return SAMPLE_FORMAT.inverse[self.sampleFormat()]

    def set_channel_config(self, config: ChannelConfigStr):
        if config not in CHANNEL_CONFIG:
            raise InvalidParamError(config, CHANNEL_CONFIG)
        self.setChannelConfig(CHANNEL_CONFIG[config])

    def get_channel_config(self) -> ChannelConfigStr:
        return CHANNEL_CONFIG.inverse[self.channelConfig()]


if __name__ == "__main__":
    fmt = AudioFormat()

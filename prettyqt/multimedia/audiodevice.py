from __future__ import annotations

from typing import Literal

from prettyqt import multimedia
from prettyqt.utils import bidict


MODE = bidict(
    null=multimedia.QAudioDevice.Mode.Null,
    input=multimedia.QAudioDevice.Mode.Input,
    output=multimedia.QAudioDevice.Mode.Output,
)

ModeStr = Literal["null", "input", "output"]


class AudioDevice(multimedia.QAudioDevice):
    def get_mode(self) -> ModeStr:
        return MODE.inverse[self.mode()]

    def get_supported_sample_formats(
        self,
    ) -> list[multimedia.audioformat.SampleFormatStr]:
        return multimedia.audioformat.SAMPLE_FORMAT.get_list(
            self.supportedSampleFormats()
        )

    def get_channel_config(self) -> multimedia.audioformat.ChannelConfigStr:
        return multimedia.audioformat.CHANNEL_CONFIG.inverse[self.channelConfiguration()]

    def get_id(self) -> str:
        return self.id().data().decode()


if __name__ == "__main__":
    fmt = AudioDevice()
    print(fmt.get_channel_config())

from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtSpatialAudio
from prettyqt.utils import bidict


OutputModeStr = Literal["infinite", "once"]

OUTPUT_MODE: bidict[OutputModeStr, QtSpatialAudio.QAudioEngine.OutputMode] = bidict(
    surround=QtSpatialAudio.QAudioEngine.OutputMode.Surround,
    stereo=QtSpatialAudio.QAudioEngine.OutputMode.Stereo,
    headphone=QtSpatialAudio.QAudioEngine.OutputMode.HeadPhone,
)


class AudioEngine(core.ObjectMixin, QtSpatialAudio.QAudioEngine):
    def set_output_mode(
        self, mode: OutputModeStr | QtSpatialAudio.QAudioEngine.OutputMode
    ):
        """Set the output mode.

        Args:
            mode: output mode
        """
        self.setOutputMode(OUTPUT_MODE.get_enum_value(mode))

    def get_output_mode(self) -> OutputModeStr:
        """Return current output mode.

        Returns:
            output mode
        """
        return OUTPUT_MODE.inverse[self.outputMode()]


if __name__ == "__main__":
    engine = AudioEngine()
    engine.set_output_mode("infinite")

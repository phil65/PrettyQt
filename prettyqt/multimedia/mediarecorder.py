from __future__ import annotations

import os
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict, datatypes


EncodingModeStr = Literal[
    "constant_quality", "constant_bit_rate", "average_bit_rate", "two_pass"
]

ENCODING_MODE: bidict[EncodingModeStr, QtMultimedia.QMediaRecorder.EncodingMode] = bidict(
    constant_quality=QtMultimedia.QMediaRecorder.EncodingMode.ConstantQualityEncoding,
    constant_bit_rate=QtMultimedia.QMediaRecorder.EncodingMode.ConstantBitRateEncoding,
    average_bit_rate=QtMultimedia.QMediaRecorder.EncodingMode.AverageBitRateEncoding,
    two_pass=QtMultimedia.QMediaRecorder.EncodingMode.TwoPassEncoding,
)

ErrorStr = Literal["none", "resource", "format", "out_of_space", "location_not_writable"]

ERROR: bidict[ErrorStr, QtMultimedia.QMediaRecorder.Error] = bidict(
    none=QtMultimedia.QMediaRecorder.Error.NoError,
    resource=QtMultimedia.QMediaRecorder.Error.ResourceError,
    format=QtMultimedia.QMediaRecorder.Error.FormatError,
    out_of_space=QtMultimedia.QMediaRecorder.Error.OutOfSpaceError,
    location_not_writable=QtMultimedia.QMediaRecorder.Error.LocationNotWritable,
)

QualityStr = Literal[
    "very_low",
    "low",
    "normal",
    "high",
    "very_high",
]

QUALITY: bidict[QualityStr, QtMultimedia.QMediaRecorder.Quality] = bidict(
    very_low=QtMultimedia.QMediaRecorder.Quality.VeryLowQuality,
    low=QtMultimedia.QMediaRecorder.Quality.LowQuality,
    normal=QtMultimedia.QMediaRecorder.Quality.NormalQuality,
    high=QtMultimedia.QMediaRecorder.Quality.HighQuality,
    very_high=QtMultimedia.QMediaRecorder.Quality.VeryHighQuality,
)

RecorderStateStr = Literal["stopped", "recording", "paused"]

RECORDER_STATE: bidict[RecorderStateStr, QtMultimedia.QMediaRecorder.RecorderState] = (
    bidict(
        stopped=QtMultimedia.QMediaRecorder.RecorderState.StoppedState,
        recording=QtMultimedia.QMediaRecorder.RecorderState.RecordingState,
        paused=QtMultimedia.QMediaRecorder.RecorderState.PausedState,
    )
)


class MediaRecorder(core.ObjectMixin, QtMultimedia.QMediaRecorder):
    def set_output_location(self, url: datatypes.UrlType | os.PathLike | None = None):
        url = datatypes.to_local_url(url)
        self.setOutputLocation(url)

    def get_recorder_state(self) -> RecorderStateStr:
        """Return current recorder state.

        Returns:
            recorder state
        """
        return RECORDER_STATE.inverse[self.recorderState()]

    def get_encoding_mode(self) -> EncodingModeStr:
        """Return current encoding mode.

        Returns:
            encoding mode
        """
        return ENCODING_MODE.inverse[self.encodingMode()]

    def set_encoding_mode(self, mode: EncodingModeStr):
        """Set encoding mode.

        Args:
            mode: encoding mode to use
        """
        self.setEncodingMode(ENCODING_MODE[mode])

    def get_quality(self) -> QualityStr:
        """Return current quality setting.

        Returns:
            quality setting
        """
        return QUALITY.inverse[self.quality()]

    def set_quality(self, quality: QualityStr):
        """Set quality.

        Args:
            quality: quality to use
        """
        self.setQuality(QUALITY[quality])

    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return ERROR.inverse[self.error()]


if __name__ == "__main__":
    player = MediaRecorder()
    source = player.get_source()
    print(source.isValid())

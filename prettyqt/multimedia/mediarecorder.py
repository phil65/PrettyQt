import pathlib
from typing import Literal, Union

from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import bidict


STATES = bidict(
    stopped=QtMultimedia.QMediaRecorder.StoppedState,
    recording=QtMultimedia.QMediaRecorder.RecordingState,
    paused=QtMultimedia.QMediaRecorder.PausedState,
)

StateStr = Literal["stopped", "recording", "paused"]

ERRORS = bidict(
    none=QtMultimedia.QMediaRecorder.NoError,
    resource=QtMultimedia.QMediaRecorder.ResourceError,
    format=QtMultimedia.QMediaRecorder.FormatError,
    out_of_space=QtMultimedia.QMediaRecorder.OutOfSpaceError,
)

ErrorStr = Literal["none", "resource", "format", "out_of_space"]

MEDIA_STATUS = bidict(
    unavailable=QtMultimedia.QMediaRecorder.UnavailableStatus,
    unloaded=QtMultimedia.QMediaRecorder.UnloadedStatus,
    loading=QtMultimedia.QMediaRecorder.LoadingStatus,
    loaded=QtMultimedia.QMediaRecorder.LoadedStatus,
    starting=QtMultimedia.QMediaRecorder.StartingStatus,
    recording=QtMultimedia.QMediaRecorder.RecordingStatus,
    paused=QtMultimedia.QMediaRecorder.PausedStatus,
    finalizing=QtMultimedia.QMediaRecorder.FinalizingStatus,
)

MediaStatusStr = Literal[
    "unavailable",
    "unloaded",
    "loading",
    "loaded",
    "starting",
    "recording",
    "paused",
    "finalizing",
]

AVAILABILITY_STATUS = bidict(
    available=QtMultimedia.QMultimedia.Available,
    service_missing=QtMultimedia.QMultimedia.ServiceMissing,
    resource_error=QtMultimedia.QMultimedia.ResourceError,
    busy=QtMultimedia.QMultimedia.Busy,
)

AvailabilityStatusStr = Literal["available", "service_missing", "resource_error", "busy"]


QtMultimedia.QMediaRecorder.__bases__ = (core.Object, multimedia.MediaBindableInterface)


class MediaRecorder(QtMultimedia.QMediaRecorder):
    def set_video_settings(self, settings):
        if isinstance(settings, multimedia.videoencodersettings.Settings):
            settings = multimedia.VideoEncoderSettings.from_dataclass(settings)
        elif isinstance(settings, dict):
            settings = multimedia.VideoEncoderSettings.from_dict(settings)
        self.setVideoSettings(settings)

    def get_video_settings(self) -> multimedia.VideoEncoderSettings:
        return multimedia.VideoEncoderSettings(self.videoSettings())

    def set_audio_settings(self, settings):
        if isinstance(settings, multimedia.audioencodersettings.Settings):
            settings = multimedia.AudioEncoderSettings.from_dataclass(settings)
        elif isinstance(settings, dict):
            settings = multimedia.AudioEncoderSettings.from_dict(settings)
        self.setAudioSettings(settings)

    def get_audio_settings(self) -> multimedia.AudioEncoderSettings:
        return multimedia.AudioEncoderSettings(self.audioSettings())

    def get_availability(self) -> AvailabilityStatusStr:
        """Return availability status.

        Returns:
            availability status
        """
        return AVAILABILITY_STATUS.inverse[self.availability()]

    def set_output_location(self, path: Union[pathlib.Path, str]):
        self.setOutputLocation(core.Url(path))

    def get_output_location(self) -> str:
        return str(core.Url(self.outputLocation()))

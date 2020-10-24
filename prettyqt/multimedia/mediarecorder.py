# -*- coding: utf-8 -*-

import pathlib
from typing import Union

from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import bidict


STATES = bidict(
    stopped=QtMultimedia.QMediaRecorder.StoppedState,
    recording=QtMultimedia.QMediaRecorder.RecordingState,
    paused=QtMultimedia.QMediaRecorder.PausedState,
)

ERRORS = bidict(
    none=QtMultimedia.QMediaRecorder.NoError,
    resource=QtMultimedia.QMediaRecorder.ResourceError,
    format=QtMultimedia.QMediaRecorder.FormatError,
    out_of_space=QtMultimedia.QMediaRecorder.OutOfSpaceError,
)

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

AVAILABILITY_STATUS = bidict(
    available=QtMultimedia.QMultimedia.Available,
    service_missing=QtMultimedia.QMultimedia.ServiceMissing,
    resource_error=QtMultimedia.QMultimedia.ResourceError,
    busy=QtMultimedia.QMultimedia.Busy,
)


QtMultimedia.QMediaRecorder.__bases__ = (core.Object, multimedia.MediaBindableInterface)


class MediaRecorder(QtMultimedia.QMediaRecorder):
    def set_video_settings(self, settings):
        if isinstance(settings, multimedia.videoencodersettings.Settings):
            settings = settings.VideoEncoderSettings.from_dataclass(settings)
        elif isinstance(settings, dict):
            settings = settings.VideoEncoderSettings.from_dict(settings)
        self.setVideoSettings(settings)

    def get_video_settings(self) -> multimedia.VideoEncoderSettings:
        return multimedia.VideoEncoderSettings(self.videoSettings())

    def set_audio_settings(self, settings):
        if isinstance(settings, multimedia.audioencodersettings.Settings):
            settings = settings.AudioEncoderSettings.from_dataclass(settings)
        elif isinstance(settings, dict):
            settings = settings.AudioEncoderSettings.from_dict(settings)
        self.setAudioSettings(settings)

    def get_audio_settings(self) -> multimedia.AudioEncoderSettings:
        return multimedia.AudioEncoderSettings(self.audioSettings())

    def get_availability(self) -> str:
        """Return availability status.

        Possible values: "available", "service_missing", "resource_error", "busy"

        Returns:
            availability status
        """
        return AVAILABILITY_STATUS.inv[self.availability()]

    def set_output_location(self, path: Union[pathlib.Path, str]):
        self.setOutputLocation(core.Url(path))

    def get_output_location(self) -> str:
        return str(core.Url(self.outputLocation()))

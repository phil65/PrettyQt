"""Tests for `prettyqt` package."""

import pytest

from prettyqt import multimedia, qt
from prettyqt.utils import InvalidParamError


def test_audioformat():
    fmt = multimedia.AudioFormat()
    fmt.set_sample_format("int32")
    assert fmt.get_sample_format() == "int32"
    with pytest.raises(InvalidParamError):
        fmt.set_sample_format("test")
    fmt.set_channel_config("5_1")
    assert fmt.get_channel_config() == "5_1"
    with pytest.raises(InvalidParamError):
        fmt.set_channel_config("test")


def test_camera():
    cam = multimedia.Camera()
    cam.set_exposure_mode("auto")
    assert cam.get_exposure_mode() == "auto"
    cam.set_exposure_mode("theatre")
    assert "theatre" in multimedia.camera.EXPOSURE_MODE
    assert "none" in multimedia.camera.FEATURE
    with pytest.raises(InvalidParamError):
        cam.set_exposure_mode("test")
    cam.set_torch_mode("off")
    assert cam.get_torch_mode() == "off"
    with pytest.raises(InvalidParamError):
        cam.set_torch_mode("test")
    cam.set_flash_mode("off")
    assert cam.get_flash_mode() == "off"
    with pytest.raises(InvalidParamError):
        cam.set_flash_mode("test")
    cam.set_white_balance_mode("auto")
    assert cam.get_white_balance_mode() == "auto"
    with pytest.raises(InvalidParamError):
        cam.set_white_balance_mode("test")
    if qt.API == "pyside6":  # PyQt6 falsely returns enum.Enum intead of enum.Flag.
        cam.get_supported_features()
    assert cam.get_error() in ["none", "camera"]
    cam.get_camera_format()


def test_cameradevice():
    cam = multimedia.CameraDevice()
    assert cam.get_position() == "unspecified"
    cam.get_video_formats()


def test_cameraformat():
    fmt = multimedia.CameraFormat()
    assert not fmt


def test_mediaplayer():
    player = multimedia.MediaPlayer()
    # file = core.File()
    # player.set_source_device(file, "")
    # player.set_source("")
    assert player.get_source() is None
    assert player.get_error() in {"none", "resource"}
    assert player.get_playback_state() == "stopped"
    assert player.get_media_status() == "none"


def test_mediametadata_mapping():
    metadata = multimedia.MediaMetaData()
    assert len(metadata) == 0
    if qt.API != "pyside6":
        pytest.skip("PyQt6 crashes in QMediaMetaData.keys() after insert()")
    metadata["title"] = "x"
    assert metadata["title"] == "x"
    assert len(metadata) == 1
    del metadata["title"]
    assert not metadata


def test_audiodevice_sample_formats(qapp):
    device = multimedia.AudioDevice()
    assert isinstance(device.get_supported_sample_formats(), list)


def test_mediarecorder(qapp):
    recorder = multimedia.MediaRecorder()
    recorder.set_encoding_mode("constant_bit_rate")
    assert recorder.get_encoding_mode() == "constant_bit_rate"
    recorder.set_encoding_mode(
        multimedia.QMediaRecorder.EncodingMode.ConstantQualityEncoding
    )
    assert recorder.get_encoding_mode() == "constant_quality"
    with pytest.raises(InvalidParamError):
        recorder.set_encoding_mode("test")
    recorder.set_quality("high")
    assert recorder.get_quality() == "high"
    recorder.set_quality(multimedia.QMediaRecorder.Quality.LowQuality)
    assert recorder.get_quality() == "low"
    with pytest.raises(InvalidParamError):
        recorder.set_quality("test")


def test_screencapture(qapp):
    capture = multimedia.ScreenCapture()
    assert capture.get_error() == "no_error"


def test_mediametadata_has_hdr_content():
    assert "has_hdr_content" in multimedia.mediametadata.KEY

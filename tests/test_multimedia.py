"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, multimedia
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
    cam.get_supported_features()
    assert cam.get_error() == "none"
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
    file = core.File()
    player.set_source_device(file, "")
    player.set_source("")
    assert player.get_source() is None
    assert player.get_error() == "resource"
    assert player.get_playback_state() == "stopped"
    assert player.get_media_status() == "none"

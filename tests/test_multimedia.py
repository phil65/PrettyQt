"""Tests for `prettyqt` package."""

import pathlib

import pytest
import pickle

from prettyqt import multimedia, core
from prettyqt.utils import InvalidParamError

URL = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"


def test_audioformat():
    fmt = multimedia.AudioFormat()
    dct = fmt.to_dict()
    new_fmt = multimedia.AudioFormat.from_dict(dct)
    for key in fmt:
        fmt[key] = fmt[key]
    assert len(fmt) == 6
    assert new_fmt.to_dict() == dct


def test_abstractvideobuffer():
    buf = multimedia.AbstractVideoBuffer("gl_texture")
    assert buf.get_handle_type() == "gl_texture"
    # assert buf.get_map_mode() == "not_mapped"


def test_camerainfo():
    info = multimedia.CameraInfo()
    repr(info)
    info.get_cameras()
    info.get_camera()


def test_camera():
    cam = multimedia.Camera()
    assert cam.get_availability() in ["available", "service_missing", "resource_error"]
    assert cam.get_state() == "unloaded"
    assert cam.get_status() in ["unloaded", "unavailable"]
    assert cam.get_lock_status() == "unlocked"
    assert cam.get_error() in ["none", "service_missing"]
    cam.set_capture_mode("still_image")
    with pytest.raises(InvalidParamError):
        cam.set_capture_mode("test")
    assert cam.get_capture_mode() == "still_image"
    cam.get_supported_locks()
    cam.get_requested_locks()


def test_camerafocus(qtlog):
    cam = multimedia.Camera()
    focus = cam.get_focus()
    with qtlog.disabled():
        focus.set_focus_mode("auto")
    with pytest.raises(InvalidParamError):
        focus.set_focus_mode("test")
    assert focus.get_focus_mode() == "auto"
    with qtlog.disabled():
        focus.set_focus_point_mode("auto")
    with pytest.raises(InvalidParamError):
        focus.set_focus_point_mode("test")
    assert focus.get_focus_point_mode() == "auto"
    assert focus.get_custom_focus_point() == core.PointF(0.5, 0.5)
    assert focus.is_focus_mode_supported("manual") is False
    assert focus.is_focus_point_mode_supported("center") is False
    assert len(focus.get_focus_zones()) == 0


def test_cameraexposure():
    cam = multimedia.Camera()
    exposure = cam.get_exposure()
    exposure.set_exposure_mode("auto")
    with pytest.raises(InvalidParamError):
        exposure.set_exposure_mode("test")
    assert exposure.get_exposure_mode() == "auto"
    exposure.set_flash_mode("flash_off")
    with pytest.raises(InvalidParamError):
        exposure.set_flash_mode("test")
    assert exposure.get_flash_mode() == "flash_off"
    exposure.set_metering_mode("matrix")
    with pytest.raises(InvalidParamError):
        exposure.set_metering_mode("test")
    assert exposure.get_metering_mode() == "matrix"
    assert exposure.get_spot_metering_point() == core.PointF()
    assert exposure.is_exposure_mode_supported("manual") is False
    assert exposure.is_flash_mode_supported("manual") is False
    assert exposure.is_metering_mode_supported("average") is False


def test_cameraimageprocessing():
    cam = multimedia.Camera()
    processing = cam.get_image_processing()
    processing.set_color_filter("none")
    with pytest.raises(InvalidParamError):
        processing.set_color_filter("test")
    assert processing.get_color_filter() == "none"
    processing.set_white_balance_mode("auto")
    with pytest.raises(InvalidParamError):
        processing.set_white_balance_mode("test")
    assert processing.get_white_balance_mode() == "auto"
    assert processing.is_color_filter_supported("blackboard") is False
    assert processing.is_white_balance_mode_supported("flash") is False


# def test_camerafocuszone():
#     cam = multimedia.Camera()
#     focus = cam.get_focus()
#     zones = focus.get_focus_zones()
#     zone = zones[0]
#     assert zone.get_focus_mode() == "invalid"
#     assert zone.get_area() == core.RectF(0, 0)


def test_cameraviewfindersettings():
    settings = multimedia.CameraViewfinderSettings()
    dct = settings.to_dict()
    new_settings = multimedia.CameraViewfinderSettings.from_dict(dct)
    for key in settings:
        settings[key] = settings[key]
    assert len(settings) == 5
    assert new_settings.to_dict() == dct


def test_imageencodersettings():
    settings = multimedia.ImageEncoderSettings()
    dct = settings.to_dict()
    new_settings = multimedia.ImageEncoderSettings.from_dict(dct)
    for key in settings:
        settings[key] = settings[key]
    assert len(settings) == 4
    assert new_settings.to_dict() == dct


def test_mediatimerange():
    time_range = multimedia.MediaTimeRange(0, 1000)
    assert 500 in time_range
    del time_range[200:700]
    assert len(time_range) == 2
    assert time_range[0] == multimedia.MediaTimeInterval(0, 199)
    assert list(time_range) == [
        multimedia.MediaTimeInterval(0, 199),
        multimedia.MediaTimeInterval(701, 1000),
    ]


def test_mediatimeinterval():
    interval = multimedia.MediaTimeInterval(0, 1000)
    repr(interval)
    with open("data.pkl", "wb") as jar:
        pickle.dump(interval, jar)
    with open("data.pkl", "rb") as jar:
        interval = pickle.load(jar)
    assert 500 in interval


def test_mediaplaylist():
    playlist = multimedia.MediaPlaylist()
    assert len(playlist) == 0
    playlist.add_media(URL)
    playlist.add_media(URL, pos=0)
    assert len(playlist) == 2
    for item in playlist:
        pass
    assert playlist[0] is not None
    playlist.set_playback_mode("sequential")
    with pytest.raises(InvalidParamError):
        playlist.set_playback_mode("test")
    assert playlist.get_playback_mode() == "sequential"


def test_audioencodersettings():
    settings = multimedia.AudioEncoderSettings()
    dct = settings.to_dict()
    new_settings = multimedia.AudioEncoderSettings.from_dict(dct)
    for key in settings:
        settings[key] = settings[key]
    assert len(settings) == 7
    assert new_settings.to_dict() == dct


def test_videoencodersettings():
    settings = multimedia.VideoEncoderSettings()
    dct = settings.to_dict()
    new_settings = multimedia.VideoEncoderSettings.from_dict(dct)
    for key in settings:
        settings[key] = settings[key]
    assert len(settings) == 7
    assert new_settings.to_dict() == dct


def test_videoframe():
    size = core.Size(64, 64)
    frame = multimedia.VideoFrame(1000, size, 8, 1)
    assert frame.get_handle_type() == "none"
    assert frame.get_map_mode() == "not_mapped"
    assert frame.get_size() == size
    frame.get_image()
    assert frame.get_pixel_format() == "argb32"
    frame.set_field_type("top_field")
    with pytest.raises(InvalidParamError):
        frame.set_field_type("test")
    assert frame.get_field_type() == "top_field"


def test_mediaplayer():
    player = multimedia.MediaPlayer()
    assert player.get_state() == "stopped"
    assert player.get_media_status() == "no_media"


def test_mediarecorder():
    player = multimedia.MediaPlayer()
    recorder = multimedia.MediaRecorder(player)
    settings = recorder.get_video_settings()
    recorder.set_video_settings(settings)
    settings = recorder.get_audio_settings()
    recorder.set_audio_settings(settings)
    recorder.get_availability()
    p = pathlib.Path.home()
    recorder.set_output_location(p)
    recorder.get_output_location()
    # assert str(recorder.get_output_location()) == str(p)


def test_mediacontent():
    cont = multimedia.MediaContent()
    assert cont.get_url() == core.Url("")


def test_soundeffect():
    effect = multimedia.SoundEffect()
    assert effect.get_status() == "null"
    effect.set_loop_count("inf")
    url = ""  # "https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand3.wav"
    effect.set_source(url)
    assert str(effect.get_source()) == url

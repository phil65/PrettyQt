#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pathlib

import pytest

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
    assert cam.get_state() == "unloaded"
    assert cam.get_status() == "unloaded"
    assert cam.get_lock_status() == "unlocked"
    assert cam.get_error() == "none"
    cam.set_capture_mode("still_image")
    with pytest.raises(InvalidParamError):
        cam.set_capture_mode("test")
    assert cam.get_capture_mode() == "still_image"


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
    url = "https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand3.wav"
    effect.set_source(url)
    assert str(effect.get_source()) == url

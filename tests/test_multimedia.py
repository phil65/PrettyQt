#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import multimedia, core

URL = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"


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
    with pytest.raises(ValueError):
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


def test_mediacontent():
    cont = multimedia.MediaContent()
    assert cont.get_url() == core.Url("")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import multimedia

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


def test_mediaplayer():
    player = multimedia.MediaPlayer()
    assert player.get_state() == "stopped"
    assert player.get_media_status() == "no_media"

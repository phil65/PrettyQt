#!/usr/bin/env python

"""Tests for `prettyqt` package."""

# import pytest

from prettyqt import texttospeech

# from prettyqt.utils import InvalidParamError


def test_texttospeech(qtlog):
    with qtlog.disabled():
        tts = texttospeech.TextToSpeech()
    assert tts.get_state() in ["ready", "backend_error"]
    tts.get_locale()
    tts.get_available_locales()
    tts.get_voice()
    tts.get_available_voices()


def test_voice():
    voice = texttospeech.Voice()
    assert voice.get_age() == "other"
    assert voice.get_gender() == "unknown"

"""Tests for `prettyqt` package."""

import pathlib

import pytest

from prettyqt.utils import InvalidParamError


spatialaudio = pytest.importorskip("prettyqt.spatialaudio")


def test_audioengine(qapp):
    engine = spatialaudio.AudioEngine(qapp)
    engine.set_output_mode("stereo")
    assert engine.get_output_mode() == "stereo"
    engine.set_output_mode("headphone")
    assert engine.get_output_mode() == "headphone"
    engine.set_output_mode("surround")
    assert engine.get_output_mode() == "surround"
    with pytest.raises(InvalidParamError):
        engine.set_output_mode("test")


def test_audioroom(qapp):
    engine = spatialaudio.AudioEngine(qapp)
    room = spatialaudio.AudioRoom(engine)
    for wall, material in [
        ("floor", "linoleum_on_concrete"),
        ("ceiling", "plaster_rough"),
        ("left_wall", "plaster_smooth"),
    ]:
        room.set_wall_material(wall, material)
        assert room.get_wall_material(wall) == material
    with pytest.raises(InvalidParamError):
        room.set_wall_material("floor", "test")
    with pytest.raises(InvalidParamError):
        room.set_wall_material("test", "marble")
    room.set_dimensions((10.0, 5.0, 3.0))
    room.set_position((1.0, 2.0, 3.0))


def test_audiolistener(qapp):
    engine = spatialaudio.AudioEngine(qapp)
    listener = spatialaudio.AudioListener(engine)
    listener.set_position((1.0, 2.0, 3.0))


def test_ambientsound(qapp, tmp_path):
    engine = spatialaudio.AudioEngine(qapp)
    sound = spatialaudio.AmbientSound(engine)
    wav_path = tmp_path / "sample.wav"
    sound.set_source(wav_path)
    assert sound.get_source() == pathlib.Path(wav_path)


def test_spatialsound(qapp):
    engine = spatialaudio.AudioEngine(qapp)
    sound = spatialaudio.SpatialSound(engine)
    sound.set_distance_model("linear")
    assert sound.get_distance_model() == "linear"
    with pytest.raises(InvalidParamError):
        sound.set_distance_model("test")
    sound.set_position((1.0, 2.0, 3.0))

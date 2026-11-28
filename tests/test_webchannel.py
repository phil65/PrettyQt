"""Tests for `prettyqt` package."""

import pytest


webchannel = pytest.importorskip("prettyqt.webchannel")


def test_webchannel(qapp):
    channel = webchannel.WebChannel()
    assert isinstance(channel, webchannel.QWebChannel)
    channel.registerObject("test", channel)
    assert "test" in channel.registeredObjects()

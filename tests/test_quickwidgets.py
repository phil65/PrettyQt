"""Tests for `prettyqt` package."""

import pathlib

from prettyqt import quickwidgets


def test_quickview(qapp):
    view = quickwidgets.QuickWidget()
    path = pathlib.Path.cwd() / "tests" / "qmltest.qml"
    view.set_source(path)
    assert view.get_source() == path
    assert view.get_status() == "ready"

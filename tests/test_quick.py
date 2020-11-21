#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

# import pytest

from prettyqt import quick, core

# from prettyqt.utils import InvalidParamError
QML_CONTENT = """import QtQuick 2.3

Rectangle {
    width: 200
    height: 100
    color: "red"

    Text {
        anchors.centerIn: parent
        text: "Hello, World!"
    }
}"""


def test_quickview():
    view = quick.QuickView()
    location = core.StandardPaths.get_writable_location("cache")
    path = location / "test.qml"
    path.touch(exist_ok=True)
    path.write_text(QML_CONTENT)
    view.set_source(path)
    assert view.get_source() == path
    assert view.get_status() == "ready"

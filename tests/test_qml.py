#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import qml, core
from prettyqt.utils import InvalidParamError

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


# def test_jsvalue():
#     val = qml.JSValue(2)
#     val["test"] = 1
#     assert val["test"].toInt() == 1
#     assert "test" in val
#     assert val.get_value() == 2


def test_jsengine():
    engine = qml.JSEngine()
    engine.install_extensions("translation")


def test_qmlengine():
    engine = qml.QmlEngine()
    obj = core.Object()
    engine.set_object_ownership(obj, "javascript")
    with pytest.raises(InvalidParamError):
        engine.set_object_ownership(obj, "test")
    assert engine.get_object_ownership(obj) == "javascript"
    engine.add_plugin_path("")
    engine.add_import_path("")
    engine.get_plugin_paths()
    engine.get_import_paths()


def test_qmlapplicationengine(qtlog):
    with qtlog.disabled():
        engine = qml.QmlApplicationEngine()
    for item in engine:
        pass
    engine.load_data(QML_CONTENT)


def test_qmlcomponent():
    comp = qml.QmlComponent()
    assert comp.get_status() == "null"
    # comp.load_url("", mode="asynchronous")
    comp.get_url()


def test_jsvalue():
    val = qml.JSValue(1)
    assert val.get_error_type() is None
    assert val.get_value() == 1
    repr(val)
    engine = qml.JSEngine()
    val = engine.new_array(2)
    val["test1"] = 1
    val["test2"] = 2
    assert val["test1"] == 1
    assert "test2" in val
    assert len(val) == 2
    del val["test2"]
    for n, v in val:
        pass
    val = qml.JSValue.from_object(None, engine)
    val = qml.JSValue.from_object(1, engine)
    val = qml.JSValue.from_object(["test"], engine)
    val = qml.JSValue.from_object(dict(a="b"), engine)

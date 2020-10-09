#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import qml, core
from prettyqt.utils import InvalidParamError


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


def test_qmlapplicationengine():
    engine = qml.QmlApplicationEngine()
    for item in engine:
        pass
    engine.load_data("", "")


def test_qmlcomponent():
    comp = qml.QmlComponent()
    assert comp.get_status() == "null"
    # comp.load_url("", mode="asynchronous")
    comp.get_url()

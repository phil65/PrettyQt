"""Tests for `prettyqt` package."""

import pathlib

import pytest

from prettyqt import core, qml
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
    engine.eval("")


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
        for _item in engine:
            pass
        path = pathlib.Path.cwd() / "tests" / "qmltest.qml"
        engine.load_data(path.read_text())


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
    assert len(val) == 2  # noqa: PLR2004
    del val["test2"]
    for _n, _v in val:
        pass
    val = qml.JSValue.from_object(None, engine)
    val = qml.JSValue.from_object(1, engine)
    val = qml.JSValue.from_object(["test"], engine)
    val = qml.JSValue.from_object(dict(a="b"), engine)

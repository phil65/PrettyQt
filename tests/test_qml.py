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


def test_jsengine(qapp):
    engine = qml.JSEngine()
    engine.install_extensions("translation")
    with pytest.raises(InvalidParamError):
        engine.install_extensions("invalid")
    engine.eval("")


def test_qmlengine(qapp):
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


def test_qmlapplicationengine(qapp):
    engine = qml.QmlApplicationEngine()
    for _item in engine:
        pass
    path = pathlib.Path.cwd() / "tests" / "qmltest.qml"
    engine.load_data(path.read_text("utf-8"))


def test_qmlcomponent(qapp):
    comp = qml.QmlComponent()
    assert comp.get_status() == "null"
    with pytest.raises(InvalidParamError):
        comp.load_url("http://example.com", mode="invalid")
    comp.get_url()
    assert hasattr(qml, "QmlPropertyMapMixin")


def test_jsvalue(qapp):
    val = qml.JSValue(1)
    assert val.get_error_type() is None
    assert val.get_value() == 1
    assert "eval" in qml.jsvalue.ERROR_TYPES
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
    assert val.isArray()
    val = qml.JSValue.from_object(dict(a="b"), engine)
    assert not val.isArray()
    assert val.isObject()
    assert val["a"] == "b"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pathlib
import pickle

import pytest

from prettyqt import core


def test_abstracttablemodel():

    class Test(core.AbstractTableModel):
        def rowCount(self, parent=None):
            return 0

        def columnCount(self, parent=None):
            return 0

    model = Test()
    assert model.rowCount() == 0
    assert model.columnCount() == 0
    with model.change_layout():
        pass
    with model.reset_model():
        pass
    with model.remove_rows():
        pass
    with model.remove_columns():
        pass
    with model.insert_rows():
        pass
    with model.append_rows(1):
        pass
    with model.insert_columns():
        pass
    # qtmodeltester.check(model, force_py=True)


def test_buffer():
    buf = core.Buffer()
    with buf.open_file("read_only"):
        pass


def test_date():
    date = core.Date(1, 1, 2000)
    with open("data.pkl", "wb") as jar:
        pickle.dump(date, jar)
    with open("data.pkl", "rb") as jar:
        new = pickle.load(jar)
    assert date == new


def test_datetime():
    date = core.Date(2000, 11, 11)
    dt = core.DateTime(date)
    with open("data.pkl", "wb") as jar:
        pickle.dump(dt, jar)
    with open("data.pkl", "rb") as jar:
        new = pickle.load(jar)
    assert dt == new
    repr(dt)


def test_dir():
    directory = core.Dir()
    assert pathlib.Path(str(directory)) == directory.to_path()


def test_diriterator():
    for i in core.DirIterator(str(pathlib.Path.cwd())):
        pass


def test_file():
    buf = core.File()
    with buf.open_file("read_only"):
        pass


def test_mimedata():
    mime_data = core.MimeData()
    mime_data.set_data("type a", "data")
    assert mime_data.get_data("type a") == "data"
    dct = dict(a=2, b="test")
    mime_data.set_json_data("type a", dct)
    assert mime_data.get_json_data("type a") == dct


def test_modelindex():
    core.ModelIndex()


def test_object():
    obj = core.Object()
    obj.set_object_name("test")
    with open("data.pkl", "wb") as jar:
        pickle.dump(obj, jar)
    with open("data.pkl", "rb") as jar:
        obj = pickle.load(jar)
    assert obj.id == "test"
    obj.find_children(core.Object, recursive=False)


def test_point():
    p = core.Point()
    repr(p)


def test_pointf():
    p = core.PointF()
    repr(p)


def test_rect():
    rect = core.Rect()
    repr(rect)


def test_rectf():
    rect = core.RectF()
    repr(rect)


def test_regexp():
    regex = core.RegExp("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    repr(regex)


def test_regularexpressionmatch():
    match = core.RegularExpressionMatch()
    match.group()
    match.groups()
    match.groupdict()
    match.start()
    match.end()
    match.span()
    assert match.pos is None
    assert match.endpos is None


def test_regularexpressionmatchiterator():
    it = core.RegularExpressionMatchIterator()
    for i in it:
        pass


def test_regularexpression():
    regex = core.RegularExpression("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    repr(regex)


def test_runnable():
    core.Runnable()


def test_settings():
    settings = core.Settings("1", "2")
    settings.clear()
    settings.set_value("test", "value")
    assert len(settings) == 1
    assert "test" in settings
    assert settings.value("test") == "value"
    with core.Settings("ab", "cd", settings_id="test") as s:
        s.set_value("test2", "xx")
    with settings.write_array("test"):
        pass
    with settings.read_array("test"):
        pass
    with settings.group("test"):
        pass
    settings["test2"] = "xyz"
    assert settings["test2"] == "xyz"
    settings.setdefault("test3", "abc")
    assert settings.get("test3") == "abc"
    del settings["test3"]
    path = pathlib.Path.cwd()
    for i in settings:
        pass

    settings.set_default_format("ini")
    assert settings.get_default_format() == "ini"
    with pytest.raises(ValueError):
        settings.set_default_format("ino")
    assert settings.get_scope() == "user"
    settings.set_path("native", "user", path)
    with pytest.raises(ValueError):
        settings.set_path("error", "user", path)
    with pytest.raises(ValueError):
        settings.set_path("native", "error", path)
    s = core.Settings.build_from_dict(dict(a="b"))
    repr(s)


def test_size():
    size = core.Size()
    repr(size)


def test_sizef():
    size = core.SizeF()
    repr(size)


def test_sortfilterproxymodel():
    core.SortFilterProxyModel()


def test_thread():
    core.ThreadPool()


def test_threadpool():
    core.ThreadPool()


def test_timer():
    def test():
        pass
    core.Timer.single_shot(test)


def test_translator():
    core.Translator()


def test_url():
    url = core.Url()
    url.to_path()
    assert not url.is_local_file()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pathlib
import pickle

import pytest

from prettyqt import core


def test_abstractitemmodel():
    model = core.AbstractItemModel()
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
    with model.insert_columns():
        pass
    # qtmodeltester.check(model, force_py=True)


def test_abstracttablemodel():
    model = core.AbstractTableModel()
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
    with model.insert_columns():
        pass
    # qtmodeltester.check(model, force_py=True)


def test_dir():
    directory = core.Dir()
    assert pathlib.Path(str(directory)) == directory.to_path()


def test_diriterator():
    for i in core.DirIterator(str(pathlib.Path.cwd())):
        pass


def test_mimedata():
    mime_data = core.MimeData()
    mime_data.set_data("type a", "data")


def test_modelindex():
    core.ModelIndex()


def test_object():
    core.Object()


def test_point():
    core.Point()


def test_rect():
    core.Rect()


def test_rectf():
    core.RectF()


def test_regexp():
    regex = core.RegExp("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(regex, jar)
    with open("data.pkl", "rb") as jar:
        regex = pickle.load(jar)
    a = list(regex.matches_in_text("0a4"))
    assert len(a) == 2


def test_runnable():
    core.Runnable()


def test_settings():
    settings = core.Settings("1", "2")
    settings.set_value("test", "value")
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
    path = pathlib.Path.cwd()
    settings.set_default_format("ini")
    with pytest.raises(ValueError):
        settings.set_default_format("ino")
    settings.set_path("native", "user", path)
    with pytest.raises(ValueError):
        settings.set_path("error", "user", path)
    with pytest.raises(ValueError):
        settings.set_path("native", "error", path)
    s = core.Settings.from_dict(dict(a="b"))


def test_size():
    core.Size()


def test_sizef():
    core.SizeF()


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

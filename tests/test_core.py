#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pathlib

from prettyqt import core, widgets


def test_transposeproxymodel():
    source = widgets.FileSystemModel()
    model = core.transposeproxymodel.TransposeProxyModel(source)
    idx = model.index(0, 0)
    model.data(idx)
    model.columnCount()
    model.rowCount()


def test_settings():
    settings = core.Settings("1", "2")
    settings.set_value("test", "value")
    assert "test" in settings
    assert settings.value("test") == "value"
    with core.Settings("ab") as s:
        s.set_value("test2", "xx")
    with settings.write_array("test"):
        pass
    with settings.read_array("test"):
        pass
    with settings.group("test"):
        pass
    path = pathlib.Path.cwd()
    settings.set_default_format("ini")
    settings.set_path("native", "user", path)


def test_abstractitemmodel():
    model = core.AbstractItemModel()
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


def test_regexp():
    regex = core.RegExp("[0-9]")
    a = list(regex.matches_in_text("0a4"))
    assert len(a) == 2


def test_threadpool():
    core.ThreadPool()


def test_timer():
    def test():
        pass
    core.Timer.single_shot(test)

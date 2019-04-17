#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core


def test_filesystemmodel():
    model = core.FileSystemModel()
    idx = model.index(0, 0)
    data = model.data(idx, model.DATA_ROLE)
    model.yield_child_indexes(idx)


def test_settings():
    settings = core.Settings("1", "2")
    settings.set_value("test", "value")
    assert settings.contains("test")
    assert settings.value("test") == "value"


def test_regexp():
    regex = core.RegExp("[0-9]")
    a = list(regex.matches_in_text("0a4"))
    assert len(a) == 2


def test_threadpool():
    pool = core.ThreadPool()


def test_timer():
    def test():
        pass
    core.Timer.single_shot(test)

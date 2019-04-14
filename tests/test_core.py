#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core


def test_filesystemmodel():
    model = core.FileSystemModel()


def test_settings():
    settings = core.Settings("1", "2")
    settings.set_value("test", "value")
    assert settings.contains("test")
    assert settings.value("test") == "value"


def test_threadpool():
    pool = core.ThreadPool()

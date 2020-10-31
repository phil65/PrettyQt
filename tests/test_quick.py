#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

# import pytest
import pathlib

from prettyqt import quick

# from prettyqt.utils import InvalidParamError


def test_quickview():
    view = quick.QuickView()
    path = pathlib.Path.home()
    view.set_source(path)
    assert view.get_source() == path
    assert view.get_status() == "error"

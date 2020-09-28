#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import webenginewidgets
from prettyqt.utils import InvalidParamError


def test_webengineview(qapp):
    widget = webenginewidgets.WebEngineView()
    widget.set_zoom(1.5)
    widget.set_url("http://www.google.de")
    widget.load_url("http://www.google.de")
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)


def test_webenginepage(qapp):
    widget = webenginewidgets.WebEnginePage()
    widget.set_zoom(1.5)
    widget.set_url("http://www.google.de")
    widget.load_url("http://www.google.de")
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)


def test_webengineprofile(qapp):
    profile = webenginewidgets.WebEngineProfile()
    profile.set_persistent_cookie_policy("allow")
    with pytest.raises(InvalidParamError):
        profile.set_persistent_cookie_policy("test")
    assert profile.get_persistent_cookie_policy() == "allow"
    profile.set_http_cache_type("disk")
    with pytest.raises(InvalidParamError):
        profile.set_http_cache_type("test")
    assert profile.get_http_cache_type() == "disk"

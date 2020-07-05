#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import webenginewidgets


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

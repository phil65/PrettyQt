#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import widgets

app = widgets.Application.create_default_app()


def test_application():
    app.set_icon("mdi.timer")
    app.set_metadata(app_name="test",
                     app_version="1.0.0",
                     org_name="test",
                     org_domain="test")
    app.get_mainwindow()
    return True

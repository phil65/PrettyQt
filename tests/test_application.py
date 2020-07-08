#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""


def test_application(qapp):
    qapp.set_icon("mdi.timer")
    qapp.set_icon(None)
    qapp.set_metadata(
        app_name="test", app_version="1.0.0", org_name="test", org_domain="test"
    )
    qapp.get_mainwindow()
    qapp.copy_to_clipboard("test")
    return True

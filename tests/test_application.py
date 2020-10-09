#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest
from qtpy import QtGui

from prettyqt import widgets
from prettyqt.utils import InvalidParamError


def test_application(qapp):
    qapp.set_icon("mdi.timer")
    qapp.set_icon(None)
    qapp.use_hdpi_bitmaps()
    qapp.disable_window_help_button()
    qapp.set_metadata(
        app_name="test", app_version="1.0.0", org_name="test", org_domain="test"
    )
    assert qapp.get_mainwindow() is None
    wnd = widgets.MainWindow()
    mw_widget = widgets.Widget()
    mw_widget.set_id("test")
    wnd.setCentralWidget(mw_widget)
    assert qapp.get_mainwindow() == wnd
    widget = qapp.get_widget(name="test")
    assert widget == mw_widget
    qapp.copy_to_clipboard("test")
    with pytest.raises(InvalidParamError):
        qapp.get_icon("testus")
    icon = qapp.get_icon("warning")
    assert isinstance(icon, QtGui.QIcon)
    qapp.set_effect_enabled("animate_toolbox")
    with pytest.raises(InvalidParamError):
        qapp.set_effect_enabled("test")
    assert qapp.is_effect_enabled("animate_toolbox")
    qapp.set_navigation_mode("keypad_directional")
    with pytest.raises(InvalidParamError):
        qapp.set_navigation_mode("test")
    assert qapp.get_navigation_mode("keypad_directional")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import widgets

app = widgets.Application.create_default_app()


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return widgets.Callout()


def test_textbrowser():
    reader = widgets.TextBrowser()
    reader.show()
    reader.close()
    assert True


def test_action():
    action = widgets.Action()
    return True


def test_application():
    return True


def test_boxlayout():
    layout = widgets.BoxLayout("horizontal")
    return True


def test_buttongroup():
    group = widgets.ButtonGroup()
    return True


def test_checkbox():
    chk = widgets.CheckBox()
    chk.show()
    chk.close()


def test_colordialog():
    dlg = widgets.ColorDialog()
    dlg.show()
    dlg.close()


def test_combobox():
    box = widgets.ComboBox()
    box.show()
    box.close()


def test_desktopwidget():
    box = widgets.DesktopWidget()
    return True


def test_dialog():
    dlg = widgets.Dialog()
    dlg.show()
    dlg.close()


def test_dialogbuttonbox():
    box = widgets.DialogButtonBox()
    box.show()
    box.close()

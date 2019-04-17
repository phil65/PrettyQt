#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import gui
from qtpy import QtCore


def test_color():
    color = gui.Color()
    color.set_color("gray")


def test_icon():
    color = gui.Icon()


def test_keysequence():
    assert(gui.KeySequence.to_shortcut_str(0x41, QtCore.Qt.ShiftModifier) == "Shift+A")


def test_standarditemmodel():
    model = gui.StandardItemModel()
    model.add_item("test")


def test_textcharformat():
    fmt = gui.TextCharFormat()
    fmt.set_font_weight("bold")
    fmt.set_foreground_color("yellow")

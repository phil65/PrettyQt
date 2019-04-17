#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import gui, core
from qtpy import QtCore


def test_color():
    color = gui.Color()
    color.set_color("gray")


def test_icon():
    icon = gui.Icon()


def test_keysequence():
    assert(gui.KeySequence.to_shortcut_str(0x41, QtCore.Qt.ShiftModifier) == "Shift+A")


def test_standarditemmodel():
    model = gui.StandardItemModel()
    model.add_item("test")


def test_textcharformat():
    fmt = gui.TextCharFormat()
    fmt.set_font_weight("bold")
    fmt.set_foreground_color("yellow")


def test_painter():
    painter = gui.Painter()
    painter.use_antialiasing()
    painter.set_pen("none")
    painter.fill_rect(core.Rect(), "transparent")
    painter.set_color("black")
    painter.set_composition_mode("source_at_top")


def test_pdfwriter():
    writer = gui.PdfWriter("test")
    writer.setup(core.RectF())

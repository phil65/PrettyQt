#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle

from qtpy import QtCore

from prettyqt import core, gui


def test_brush():
    gui.Brush()


def test_color():
    color = gui.Color()
    color.set_color("gray")
    with open("data.pkl", "wb") as jar:
        pickle.dump(color, jar)
    with open("data.pkl", "rb") as jar:
        color = pickle.load(jar)
    assert str(color) == "#808080"


def test_doublevalidator():
    val = gui.DoubleValidator()
    val.setRange(0, 9)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_icon():
    icon = gui.Icon()
    icon.for_color("black")
    with open("data.pkl", 'wb') as jar:
        pickle.dump(icon, jar)
    with open("data.pkl", 'rb') as jar:
        icon = pickle.load(jar)


def test_intvalidator():
    val = gui.IntValidator()
    val.setRange(0, 9)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")


def test_keysequence():
    assert(gui.KeySequence.to_shortcut_str(0x41, QtCore.Qt.ShiftModifier) == "Shift+A")


def test_standarditem():
    s = gui.StandardItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(s, jar)
    with open("data.pkl", "rb") as jar:
        s = pickle.load(jar)


def test_standarditemmodel():
    model = gui.StandardItemModel()
    model.add_item("test")
    for item in model:
        pass
    with open("data.pkl", "wb") as jar:
        pickle.dump(model, jar)
    with open("data.pkl", "rb") as jar:
        model = pickle.load(jar)
    model += gui.StandardItem("Item")


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


def test_pen():
    gui.Pen()


def test_picture():
    gui.Picture()


def test_pixmap():
    gui.Pixmap()


def test_polygonf():
    poly = gui.PolygonF()
    with open("data.pkl", 'wb') as jar:
        pickle.dump(poly, jar)
    with open("data.pkl", 'rb') as jar:
        poly = pickle.load(jar)


def test_regexpvalidator():
    val = gui.RegExpValidator()
    val.set_regex("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")


def test_syntaxhighlighter():
    gui.SyntaxHighlighter(None)


def test_textcharformat():
    fmt = gui.TextCharFormat()
    fmt.set_font_weight("bold")
    fmt.set_foreground_color("yellow")


def test_validator():
    gui.Validator()

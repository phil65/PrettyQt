#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import pytest

from qtpy import QtCore
import qtpy

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
    repr(color)
    # color.as_qt()


def test_cursor():
    cursor = gui.Cursor()
    cursor.set_shape("arrow")
    with pytest.raises(ValueError):
        cursor.set_shape("test")
    assert cursor.get_shape() == "arrow"


def test_doublevalidator():
    val = gui.DoubleValidator()
    val.setRange(0, 9)
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")
    repr(val)


def test_font():
    font = gui.Font("Consolas")
    repr(font)
    font.metrics
    font = gui.Font.mono()


def test_fontmetrics():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetrics(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    assert len(val) == 3


def test_icon():
    icon = gui.Icon()
    icon.for_color("black")
    with open("data.pkl", "wb") as jar:
        pickle.dump(icon, jar)
    with open("data.pkl", "rb") as jar:
        icon = pickle.load(jar)


def test_intvalidator():
    val = gui.IntValidator()
    val.setRange(0, 9)
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.is_valid_value("4")
    assert not val.is_valid_value("10")
    repr(val)


def test_keysequence():
    assert gui.KeySequence.to_shortcut_str(0x41, QtCore.Qt.ShiftModifier) == "Shift+A"


def test_standarditem():
    s = gui.StandardItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(s, jar)
    with open("data.pkl", "rb") as jar:
        s = pickle.load(jar)
    repr(s)
    s.set_icon("mdi.timer")


def test_standarditemmodel():
    model = gui.StandardItemModel()
    model.add("test")
    for item in model:
        pass
    with open("data.pkl", "wb") as jar:
        pickle.dump(model, jar)
    with open("data.pkl", "rb") as jar:
        model = pickle.load(jar)
    model += gui.StandardItem("Item")
    model[0]
    assert len(model.find_items("test")) == 1
    with pytest.raises(ValueError):
        model.find_items("test", mode="wrong_mode")


def test_textcursor():
    cursor = gui.TextCursor()
    cursor.set_position(1, "move")
    cursor.move_position("start", "move", 1)
    cursor.select("document")
    cursor.select_text(1, 3)


def test_painter():
    painter = gui.Painter(gui.Image())
    painter.use_antialiasing()
    painter.set_pen("none")
    painter.fill_rect((0, 1, 3, 5), "transparent")
    painter.fill_rect(core.Rect(), "transparent")
    with pytest.raises(ValueError):
        painter.fill_rect(core.Rect(), "testus")
    painter.set_color("black")
    painter.set_composition_mode("source_atop")
    with pytest.raises(ValueError):
        painter.set_composition_mode("test")
    with pytest.raises(ValueError):
        painter.set_pen("test")
    # assert painter.get_composition_mode() == "source_atop"


def test_pdfwriter():
    writer = gui.PdfWriter("test")
    writer.setup(core.RectF())


def test_pen():
    pen = gui.Pen()
    pen.set_color("blue")


def test_picture():
    gui.Picture()


def test_pixmap():
    gui.Pixmap()


def test_polygonf():
    poly = gui.PolygonF()
    with open("data.pkl", "wb") as jar:
        pickle.dump(poly, jar)
    with open("data.pkl", "rb") as jar:
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
    repr(val)


@pytest.mark.skipif(qtpy.API == "pyside2",
                    reason="Only supported in PyQt5")
def test_regularexpressionvalidator():
    val = gui.RegularExpressionValidator()
    val.set_regex("[0-9]")
    with open("data.pkl", "wb") as jar:
        pickle.dump(val, jar)
    with open("data.pkl", "rb") as jar:
        val = pickle.load(jar)
    assert val.get_regex() == "[0-9]"
    assert val.is_valid_value("0")
    repr(val)


def test_syntaxhighlighter():
    gui.SyntaxHighlighter(None)


def test_textcharformat():
    fmt = gui.TextCharFormat()
    fmt.set_font_weight("bold")
    assert fmt.get_font_weight() == "bold"
    fmt.set_foreground_color("yellow")
    fmt.set_background_color("yellow")
    with pytest.raises(ValueError):
        fmt.set_font_weight("test")


def test_validator():
    gui.Validator()

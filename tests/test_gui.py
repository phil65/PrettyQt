#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle
import pytest
import pathlib

from qtpy import QtCore
import qtpy

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError


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
    with pytest.raises(InvalidParamError):
        cursor.set_shape("test")
    assert cursor.get_shape() == "arrow"


def test_desktopservices():
    gui.DesktopServices.open_url("test")


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
    with pytest.raises(InvalidParamError):
        font.set_style_hint("test")
    font.set_style_hint("monospace")
    font.set_weight("thin")
    with pytest.raises(InvalidParamError):
        font.set_weight("test")


def test_fontdatabase():
    db = gui.FontDatabase()
    p = pathlib.Path()
    db.add_fonts_from_folder(p)
    db.get_system_font("smallest_readable")


def test_fontmetrics():
    font = gui.Font("Consolas")
    fontmetrics = gui.FontMetrics(font)
    val = fontmetrics.elided_text("This is a test", mode="right", width=40)
    assert len(val) < 5


def test_gradient():
    grad = gui.Gradient()
    grad.set_coordinate_mode("object")
    assert grad.get_coordinate_mode() == "object"
    with pytest.raises(InvalidParamError):
        grad.set_coordinate_mode("test")
    grad.set_spread("repeat")
    assert grad.get_spread() == "repeat"
    with pytest.raises(InvalidParamError):
        grad.set_spread("test")
    assert grad.get_type() == "none"


def test_guiapplication():
    with gui.GuiApplication.override_cursor("forbidden"):
        pass


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
    seq = gui.KeySequence("Ctrl+C")
    assert seq.get_matches("Ctrl+C") == "exact"


def test_standarditem():
    s = gui.StandardItem()
    with open("data.pkl", "wb") as jar:
        pickle.dump(s, jar)
    with open("data.pkl", "rb") as jar:
        s = pickle.load(jar)
    repr(s)
    s.set_icon("mdi.timer")
    s.clone()


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
    with pytest.raises(InvalidParamError):
        model.find_items("test", mode="wrong_mode")


def test_textcursor():
    cursor = gui.TextCursor()
    cursor.set_position(1, "move")
    cursor.move_position("start", "move", 1)
    cursor.select("document")
    cursor.replace_text(0, 2, "test")
    cursor.select_text(1, 3)
    cursor.span()
    with cursor.edit_block():
        pass


def test_painter():
    painter = gui.Painter(gui.Image())
    painter.use_antialiasing()
    painter.set_pen("none")
    painter.set_transparent_background(False)
    painter.set_transparent_background(True)
    painter.set_brush(gui.Brush())
    with painter.paint_on(widgets.Widget()):
        pass
    painter.set_brush(gui.Color("red"))
    painter.fill_rect((0, 1, 3, 5), "transparent")
    painter.fill_rect(core.Rect(), "transparent")
    with pytest.raises(ValueError):
        painter.fill_rect(core.Rect(), "testus")
    painter.set_color("black")
    painter.set_composition_mode("source_atop")
    with pytest.raises(InvalidParamError):
        painter.set_composition_mode("test")
    with pytest.raises(InvalidParamError):
        painter.set_pen("test")
    # assert painter.get_composition_mode() == "source_atop"


def test_painterpath():
    path = gui.PainterPath()
    rect = core.RectF(0, 0, 1, 1)
    path.addRect(rect)
    assert len(path) == 5
    assert bool(path)
    assert core.PointF(0.5, 0.5) in path
    path[1] = (0.5, 0.5)
    path.add_rect(QtCore.QRect(0, 0, 1, 1))


def test_palette():
    pal = gui.Palette()
    assert len(pal.get_colors()) == 11
    pal.highlight_inactive()
    pal.set_color("background", "red")
    color = gui.Color("red")
    pal["button"] = color
    assert pal["button"] == color


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


def test_polygon():
    poly = gui.Polygon()
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


@pytest.mark.skipif(qtpy.API == "pyside2", reason="Only supported in PyQt5")
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
    with pytest.raises(InvalidParamError):
        fmt.set_font_weight("test")
    fmt = gui.TextCharFormat(bold=True)
    assert fmt.get_font_weight() == "bold"
    fmt.select_full_width()


def test_validator():
    gui.Validator()

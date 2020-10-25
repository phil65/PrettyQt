#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pickle

import pytest
from qtpy import QtCore

from prettyqt import charts
from prettyqt.utils import InvalidParamError


def test_barseries(qtbot):
    series = charts.BarSeries()
    barset = charts.BarSet("Test")
    series.append(barset)
    assert series[0] == barset
    del series[0]
    series.set_labels_position("inside_base")
    with pytest.raises(InvalidParamError):
        series.set_labels_position("test")
    assert series.get_labels_position() == "inside_base"


def test_barcategoryaxis(qtbot):
    obj = QtCore.QObject()
    axis = charts.BarCategoryAxis(obj)
    axis += "a"
    axis += "b"
    assert axis[0] == "a"
    axis["a"] = "c"
    assert list(axis) == ["c", "b"]
    del axis["b"]


def test_boxset(qtbot):
    boxset = charts.BoxSet()
    repr(boxset)
    boxset.get_pen()
    boxset.get_brush()
    boxset["median"] = 1.0
    assert boxset["median"] == 1.0


def test_candlestickset(qtbot):
    candlestickset = charts.CandlestickSet()
    repr(candlestickset)
    candlestickset.get_pen()
    candlestickset.get_brush()


def test_categoryaxis(qtbot):
    axis = charts.CategoryAxis()
    axis += ("a", 2)
    axis += ("b", 4)
    assert len(axis) == 2
    assert axis[0] == "a"
    axis["a"] = "c"
    assert list(axis) == ["c", "b"]
    del axis["c"]
    axis.set_labels_position("on_value")
    with pytest.raises(InvalidParamError):
        axis.set_labels_position("test")
    assert axis.get_labels_position() == "on_value"


def test_chart(qtbot):
    chart = charts.Chart()
    chart.hide_legend()
    chart.show_legend()
    chart.set_legend_alignment("right")
    chart.set_theme("Dark")
    chart.set_animation_options("series")


def test_chartview(qtbot):
    widget = charts.ChartView()
    widget.show()
    widget.get_image()
    qtbot.addWidget(widget)
    qtbot.keyPress(widget, QtCore.Qt.Key_F11)
    # qtbot.keyPress(widget, QtCore.Qt.Key_Minus)
    # qtbot.keyPress(widget, QtCore.Qt.Key_Plus)
    qtbot.keyPress(widget, QtCore.Qt.Key_Left)
    qtbot.keyPress(widget, QtCore.Qt.Key_Right)
    qtbot.keyPress(widget, QtCore.Qt.Key_Up)
    qtbot.keyPress(widget, QtCore.Qt.Key_Down)
    qtbot.mousePress(widget, QtCore.Qt.RightButton)
    qtbot.mouseMove(widget, delay=100)


def test_lineseries(qtbot):
    line = charts.LineSeries()
    with open("data.pkl", "wb") as jar:
        pickle.dump(line, jar)
    with open("data.pkl", "rb") as jar:
        line = pickle.load(jar)


def test_datetimeaxis(qtbot):
    axis = charts.DateTimeAxis()
    axis.get_min()
    axis.get_max()


def test_scatterseries(qtbot):
    charts.ScatterSeries()


def test_pieslice(qtbot):
    pieslice = charts.PieSlice()
    repr(pieslice)
    pieslice.set_label_position("inside_tangential")
    with pytest.raises(InvalidParamError):
        pieslice.set_label_position("test")
    assert pieslice.get_label_position() == "inside_tangential"
    pieslice.get_label_font()
    pieslice.get_label_brush()
    pieslice.get_label_color()
    pieslice.get_pen()
    pieslice.get_brush()
    pieslice.get_color()
    pieslice.get_border_color()


def test_polarchart(qtbot):
    chart = charts.PolarChart()
    chart.add_axis(charts.ValueAxis(), "radial")


def test_valueaxis(qtbot):
    axis = charts.ValueAxis()
    axis.set_tick_type("fixed")
    with pytest.raises(InvalidParamError):
        axis.set_tick_type("test")
    assert axis.get_tick_type() == "fixed"
    assert axis.get_alignment() is None
    assert axis.get_orientation() is None
    # assert axis.get_orientation() == "horizontal"
    axis.get_grid_line_color()
    axis.get_grid_line_pen()
    axis.get_line_pen()
    axis.get_line_pen_color()
    axis.get_labels_color()
    axis.get_labels_brush()
    axis.get_labels_font()
    axis.get_title_font()
    axis.get_title_brush()
    axis.get_shades_color()
    axis.get_shades_brush()
    axis.get_shades_pen()
    axis.get_shades_border_color()
    axis.get_minor_grid_line_pen()
    axis.get_minor_grid_line_color()

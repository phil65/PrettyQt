"""Tests for `prettyqt` package."""

import pytest

from prettyqt import constants
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


charts = pytest.importorskip("prettyqt.charts")


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


def test_chartview(qtbot, qttester):
    widget = charts.ChartView()
    widget.show()
    widget.get_image()
    qtbot.add_widget(widget)
    qttester.send_keypress(widget, constants.Key.Key_F11)
    # qttester.send_keypress(widget, constants.Key.Key_Minus)
    # qttester.send_keypress(widget, constants.Key.Key_Plus)
    qttester.send_keypress(widget, constants.Key.Key_Left)
    qttester.send_keypress(widget, constants.Key.Key_Right)
    qttester.send_keypress(widget, constants.Key.Key_Up)
    qttester.send_keypress(widget, constants.Key.Key_Down)
    qttester.send_mousepress(widget, constants.MouseButton.RightButton)
    qttester.send_mousemove(widget, delay=100)


def test_legend(qtbot):
    chart = charts.Chart()
    legend = chart.get_legend()
    legend.set_alignment("bottom")
    with pytest.raises(InvalidParamError):
        legend.set_alignment("test")
    assert legend.get_alignment() == "bottom"
    legend.set_marker_shape("circle")
    with pytest.raises(InvalidParamError):
        legend.set_marker_shape("test")
    assert legend.get_marker_shape() == "circle"
    legend.get_border_color()
    legend.get_color()
    legend.get_label_color()
    legend.get_font()


def test_lineseries(qtbot):
    line = charts.LineSeries()
    line += QtCore.QPointF(1, 1)
    line += QtCore.QPointF(2, 2)
    line[1] = QtCore.QPointF(0, 0)
    line.get_brush()
    line.get_pen()
    del line[1]


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

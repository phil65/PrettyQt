"""The charts module provides a set of easy-to-use chart components."""

from __future__ import annotations

from prettyqt.qt.QtCharts import *  # noqa: F403

from .barset import BarSet
from .boxset import BoxSet
from .candlestickset import CandlestickSet
from .pieslice import PieSlice
from .abstractaxis import AbstractAxis, AbstractAxisMixin
from .valueaxis import ValueAxis, ValueAxisMixin
from .datetimeaxis import DateTimeAxis
from .categoryaxis import CategoryAxis
from .logvalueaxis import LogValueAxis
from .barcategoryaxis import BarCategoryAxis
from .abstractseries import AbstractSeries, AbstractSeriesMixin
from .abstractbarseries import AbstractBarSeries, AbstractBarSeriesMixin
from .barseries import BarSeries
from .percentbarseries import PercentBarSeries
from .horizontalbarseries import HorizontalBarSeries
from .horizontalpercentbarseries import HorizontalPercentBarSeries
from .stackedbarseries import StackedBarSeries
from .horizontalstackedbarseries import HorizontalStackedBarSeries
from .xyseries import XYSeries, XYSeriesMixin
from .scatterseries import ScatterSeries
from .lineseries import LineSeries
from .legend import Legend
from .chart import Chart, ChartMixin
from .polarchart import PolarChart
from .chartview import ChartView
from prettyqt.qt import QtCharts

QT_MODULE = QtCharts

__all__ = [
    "AbstractAxis",
    "AbstractAxisMixin",
    "AbstractBarSeries",
    "AbstractBarSeriesMixin",
    "AbstractSeries",
    "AbstractSeriesMixin",
    "BarCategoryAxis",
    "BarSeries",
    "BarSet",
    "BoxSet",
    "CandlestickSet",
    "CategoryAxis",
    "Chart",
    "ChartMixin",
    "ChartView",
    "DateTimeAxis",
    "HorizontalBarSeries",
    "HorizontalPercentBarSeries",
    "HorizontalStackedBarSeries",
    "Legend",
    "LineSeries",
    "LogValueAxis",
    "PercentBarSeries",
    "PieSlice",
    "PolarChart",
    "ScatterSeries",
    "StackedBarSeries",
    "ValueAxis",
    "ValueAxisMixin",
    "XYSeries",
    "XYSeriesMixin",
]

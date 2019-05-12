# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore
from qtpy.QtCharts import QtCharts

THEMES = {"Light": QtCharts.QChart.ChartThemeLight,
          "Blue Cerulean": QtCharts.QChart.ChartThemeBlueCerulean,
          "Dark": QtCharts.QChart.ChartThemeDark,
          "Brown Sand": QtCharts.QChart.ChartThemeBrownSand,
          "Blue NCS": QtCharts.QChart.ChartThemeBlueNcs,
          "High Contrast": QtCharts.QChart.ChartThemeHighContrast,
          "Blue Icy": QtCharts.QChart.ChartThemeBlueIcy,
          "Qt": QtCharts.QChart.ChartThemeQt}

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)

ANIMATION_OPTS = dict(series=QtCharts.QChart.SeriesAnimations)


class Chart(QtCharts.QChart):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def update_boundaries(self):
        """
        set new min/max values based on axis
        """
        self.max_x = self.axisX().max()
        self.max_y = self.axisY().max()
        self.min_x = self.axisX().min()
        self.min_y = self.axisY().min()

    def hide_legend(self):
        self.legend().hide()

    def show_legend(self):
        self.legend().show()

    def set_legend_alignment(self, alignment: str):
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment} not a valid alignment.")
        self.legend().setAlignment(ALIGNMENTS[alignment])

    def set_theme(self, theme_name: str):
        self.setTheme(THEMES[theme_name])

    def set_animation_options(self, option: str):
        self.setAnimationOptions(ANIMATION_OPTS[option])

    def apply_nice_numbers(self):
        """
        adjust both axis to display nice round numbers
        """
        self.axisX().applyNiceNumbers()
        self.axisY().applyNiceNumbers()

    def zoom_by_factor(self, factor: float):
        """
        zoom in/out by factor (1.0 = no change)
        make sure that we dont zoom out too far
        """
        self.zoom(factor)
        if self.axisX().min() < self.min_x:
            self.axisX().setMin(self.min_x)
        if self.axisX().max() > self.max_x:
            self.axisX().setMax(self.max_x)
        if self.axisY().max() > self.max_y:
            self.axisY().setMax(self.max_y)

        # always bottom-align when zooming for now. should perhaps become optional.
        # if self.axisY().min() < self.min_y:
        self.axisY().setMin(max(0, self.min_y))

from __future__ import annotations

from typing import Literal

from prettyqt import charts, constants, core, widgets
from prettyqt.qt import QtCharts, QtCore
from prettyqt.utils import InvalidParamError, bidict, datatypes


THEMES = bidict(
    {
        "Light": QtCharts.QChart.ChartTheme.ChartThemeLight,
        "Blue Cerulean": QtCharts.QChart.ChartTheme.ChartThemeBlueCerulean,
        "Dark": QtCharts.QChart.ChartTheme.ChartThemeDark,
        "Brown Sand": QtCharts.QChart.ChartTheme.ChartThemeBrownSand,
        "Blue NCS": QtCharts.QChart.ChartTheme.ChartThemeBlueNcs,
        "High Contrast": QtCharts.QChart.ChartTheme.ChartThemeHighContrast,
        "Blue Icy": QtCharts.QChart.ChartTheme.ChartThemeBlueIcy,
        "Qt": QtCharts.QChart.ChartTheme.ChartThemeQt,
    }
)

ThemeStr = Literal[
    "Light",
    "Blue Cerulean",
    "Dark",
    "Brown Sand",
    "Blue NCS",
    "High Contrast",
    "Blue Icy",
    "Qt",
]

ANIMATION_OPTIONS = bidict(
    none=QtCharts.QChart.AnimationOption.NoAnimation,
    grid_axis=QtCharts.QChart.AnimationOption.GridAxisAnimations,
    series=QtCharts.QChart.AnimationOption.SeriesAnimations,
    all=QtCharts.QChart.AnimationOption.AllAnimations,
)

AnimationOptionStr = Literal["none", "grid_axis", "series", "all"]

CHART_TYPES = bidict(
    undefined=QtCharts.QChart.ChartType.ChartTypeUndefined,
    cartesian=QtCharts.QChart.ChartType.ChartTypeCartesian,
    polar=QtCharts.QChart.ChartType.ChartTypePolar,
)

ChartTypeStr = Literal["undefined", "cartesian", "polar"]


class ChartMixin(widgets.GraphicsWidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def get_axes(
        self,
        orientation: constants.OrientationStr | None = None,
        series: QtCharts.QAbstractBarSeries | None = None,
    ) -> list[QtCharts.QAbstractAxis]:
        if orientation is None:
            orientation = constants.HORIZONTAL | constants.VERTICAL
        return self.axes(constants.ORIENTATION[orientation], series)

    def update_boundaries(self):
        """Set new min/max values based on axis."""
        if axis_x := self.get_axes("horizontal"):
            self.max_x = axis_x[0].max()
            self.min_x = axis_x[0].min()
        if axis_y := self.get_axes("vertical"):
            self.max_y = axis_y[0].max()
            self.min_y = axis_y[0].min()

    def hide_legend(self):
        self.legend().hide()

    def show_legend(self):
        self.legend().show()

    def get_legend(self) -> charts.Legend:
        return charts.Legend(self.legend())

    def set_legend_alignment(self, alignment: constants.SideStr):
        if alignment not in constants.SIDES:
            raise InvalidParamError(alignment, constants.SIDES)
        self.legend().setAlignment(constants.SIDES[alignment])

    def set_theme(self, theme_name: ThemeStr):
        self.setTheme(THEMES[theme_name])

    def set_margins(self, margins: datatypes.MarginsType):
        if isinstance(margins, tuple):
            margins = QtCore.QMargins(*margins)
        self.setMargins(margins)

    def set_animation_options(self, option: AnimationOptionStr):
        self.setAnimationOptions(ANIMATION_OPTIONS[option])

    def apply_nice_numbers(self):
        """Adjust both axis to display nice round numbers."""
        for axis in self.get_axes():
            axis.applyNiceNumbers()

    def zoom_by_factor(self, factor: float):
        """Zoom in/out by factor (1.0 = no change).

        Make sure that we dont zoom out too far
        """
        self.zoom(factor)
        if axis_x := self.get_axes("horizontal"):
            if axis_x[0].min() < self.min_x:
                axis_x[0].setMin(self.min_x)
            if axis_x[0].max() > self.max_x:
                axis_x[0].setMax(self.max_x)
        if axis_y := self.get_axes("vertical"):
            if axis_y[0].max() > self.max_y:
                axis_y[0].setMax(self.max_y)

            # always bottom-align when zooming for now. should perhaps become optional.
            # if axis_y[0].min() < self.min_y:
            axis_y[0].setMin(max(0, self.min_y))

    def get_chart_type(self) -> ChartTypeStr:
        return CHART_TYPES.inverse[self.chartType()]

    def get_margins(self) -> core.Margins:
        return core.Margins(self.margins())

    def get_plot_area(self) -> core.RectF:
        return core.RectF(self.plotArea())

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def get_theme(self) -> ThemeStr:
        return THEMES.inverse[self.theme()]

    def get_animation_options(self) -> list[AnimationOptionStr]:
        return ANIMATION_OPTIONS.get_list(self.animationOptions())

    def get_animation_easing_curve(self) -> core.EasingCurve:
        return core.EasingCurve(self.animationEasingCurve())


class Chart(ChartMixin, QtCharts.QChart):
    pass


if __name__ == "__main__":
    app = widgets.app()
    chart = Chart()
    legend = chart.get_legend()
    legend.set_alignment("bottom")

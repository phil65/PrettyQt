from __future__ import annotations

from typing import Literal

from prettyqt import charts, constants, core, widgets
from prettyqt.qt import QtCharts, QtCore
from prettyqt.utils import InvalidParamError, bidict, types


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


QtCharts.QChart.__bases__ = (widgets.GraphicsWidget,)


class Chart(QtCharts.QChart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def serialize_fields(self):
        return dict(
            animation_duration=self.animationDuration(),
            animation_easing_curve=self.get_animation_easing_curve(),
            animation_options=self.get_animation_options(),
            background_roundness=self.backgroundRoundness(),
            background_visible=self.isBackgroundVisible(),
            chart_type=self.get_chart_type(),
            drop_shadow_enabled=self.isDropShadowEnabled(),
            locale=self.get_locale(),
            localize_numbers=self.localizeNumbers(),
            margins=self.get_margins(),
            plot_area=self.get_plot_area(),
            plot_area_background_visible=self.isPlotAreaBackgroundVisible(),
            theme=self.get_theme(),
            title=self.title(),
        )

    def update_boundaries(self):
        """Set new min/max values based on axis."""
        self.max_x = self.axisX().max()
        self.max_y = self.axisY().max()
        self.min_x = self.axisX().min()
        self.min_y = self.axisY().min()

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

    def set_margins(self, margins: types.MarginsType):
        if isinstance(margins, tuple):
            margins = QtCore.QMargins(*margins)
        self.setMargins(margins)

    def set_animation_options(self, option: AnimationOptionStr):
        self.setAnimationOptions(ANIMATION_OPTIONS[option])

    def apply_nice_numbers(self):
        """Adjust both axis to display nice round numbers."""
        self.axisX().applyNiceNumbers()
        self.axisY().applyNiceNumbers()

    def zoom_by_factor(self, factor: float):
        """Zoom in/out by factor (1.0 = no change).

        Make sure that we dont zoom out too far
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
        return [k for k, v in ANIMATION_OPTIONS.items() if v & self.animationOptions()]

    def get_animation_easing_curve(self) -> core.EasingCurve:
        return core.EasingCurve(self.animationEasingCurve())


if __name__ == "__main__":
    chart = Chart()
    legend = chart.get_legend()
    legend.set_alignment("bottom")

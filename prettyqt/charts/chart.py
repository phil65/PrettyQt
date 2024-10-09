from __future__ import annotations

from typing import Literal

from prettyqt import charts, constants, core, gui, widgets
from prettyqt.utils import bidict, datatypes


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

THEMES: bidict[ThemeStr, charts.QChart.ChartTheme] = bidict({
    "Light": charts.QChart.ChartTheme.ChartThemeLight,
    "Blue Cerulean": charts.QChart.ChartTheme.ChartThemeBlueCerulean,
    "Dark": charts.QChart.ChartTheme.ChartThemeDark,
    "Brown Sand": charts.QChart.ChartTheme.ChartThemeBrownSand,
    "Blue NCS": charts.QChart.ChartTheme.ChartThemeBlueNcs,
    "High Contrast": charts.QChart.ChartTheme.ChartThemeHighContrast,
    "Blue Icy": charts.QChart.ChartTheme.ChartThemeBlueIcy,
    "Qt": charts.QChart.ChartTheme.ChartThemeQt,
})


AnimationOptionStr = Literal["none", "grid_axis", "series", "all"]

ANIMATION_OPTIONS: bidict[AnimationOptionStr, charts.QChart.AnimationOption] = bidict(
    none=charts.QChart.AnimationOption.NoAnimation,
    grid_axis=charts.QChart.AnimationOption.GridAxisAnimations,
    series=charts.QChart.AnimationOption.SeriesAnimations,
    all=charts.QChart.AnimationOption.AllAnimations,
)

ChartTypeStr = Literal["undefined", "cartesian", "polar"]

CHART_TYPES: bidict[ChartTypeStr, charts.QChart.ChartType] = bidict(
    undefined=charts.QChart.ChartType.ChartTypeUndefined,
    cartesian=charts.QChart.ChartType.ChartTypeCartesian,
    polar=charts.QChart.ChartType.ChartTypePolar,
)


class ChartMixin(widgets.GraphicsWidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.adjust_style_to_palette()
        gui.GuiApplication.styleHints().colorSchemeChanged.connect(
            self.adjust_style_to_palette
        )

    def adjust_style_to_palette(self):
        """Adjusts the chart theme to current Palette.

        Checks if palette is dark-ish and applies an appropriate theme to the chart.
        """
        pal = gui.GuiApplication.get_palette()
        style = "Dark" if pal.is_dark() else "Light"
        self.set_theme(style)

    def get_axes(
        self,
        orientation: constants.OrientationStr | constants.Orientation | None = None,
        series: charts.QAbstractBarSeries | None = None,
    ) -> list[charts.QAbstractAxis]:
        """Get axes of chart.

        Arguments:
            orientation: Orientation of the axes that should get returned.
            series: Series to return axes for. Returns all axes if None.
        """
        if orientation is None:
            orientation = constants.HORIZONTAL | constants.VERTICAL
        return self.axes(constants.ORIENTATION.get_enum_value(orientation), series)

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

    def set_legend_alignment(
        self, alignment: constants.SideStr | constants.AlignmentFlag
    ):
        """Set alignment of the chart legend."""
        self.legend().setAlignment(constants.SIDES.get_enum_value(alignment))

    def set_theme(self, theme_name: ThemeStr | charts.QChart.ChartTheme):
        self.setTheme(THEMES.get_enum_value(theme_name))

    def set_margins(self, margins: datatypes.MarginsType):
        margins = datatypes.to_margins(margins)
        self.setMargins(margins)

    def set_animation_options(
        self, option: AnimationOptionStr | charts.QChart.AnimationOption
    ):
        self.setAnimationOptions(ANIMATION_OPTIONS.get_enum_value(option))

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


class Chart(ChartMixin, charts.QChart):
    pass


if __name__ == "__main__":
    app = widgets.app()
    chart = Chart()
    legend = chart.get_legend()
    legend.set_alignment("bottom")

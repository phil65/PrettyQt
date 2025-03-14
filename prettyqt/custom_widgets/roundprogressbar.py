from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui, widgets


if TYPE_CHECKING:
    from collections.abc import Sequence


BarStyleStr = Literal["donut", "pie", "line", "expand"]

VALUE_TYPE = ["value", "percent", "max"]
ValueTypeStr = Literal["value", "percent", "max"]

VALUE_MAP: dict[str, ValueTypeStr] = {
    r"%v": "value",
    r"%p": "percent",
    r"%m": "max",
}


class RoundProgressBar(widgets.Widget):
    class Position(float, enum.Enum):
        """Start position of progress bar in degrees."""

        Left = 180.0
        Top = 90.0
        Right = 0.0
        Bottom = -90.0

    class BarStyle(enum.IntEnum):
        """Progress bar style."""

        Donut = 1
        Pie = 2
        Line = 3
        Expand = 4

    class ValueType(enum.IntEnum):
        """Value type."""

        value = 1
        percent = 2
        maximum = 3

    def __init__(self, parent: widgets.QWidget | None = None):
        super().__init__(parent)
        self._min_value = 0.0
        self._max_value = 100.0
        self.current_value = 0.0
        self.null_pos = self.Position.Top
        self.bar_style: RoundProgressBar.BarStyle = self.BarStyle.Donut
        self.outline_pen_width = 1.0
        self.data_pen_width = 1.0
        self._rebuild_brush = False
        self.number_format = "%p%"
        self.decimals = 1
        self._update_flags: ValueTypeStr = "percent"
        self.gradient_data: Sequence[gui.QColor] = []

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value

    # SETTERS -------------------------------------------------------

    def set_null_position(self, position: RoundProgressBar.Position):
        if position != self.null_pos:
            self.null_pos = position
            self._rebuild_brush = True
            self.update()

    def get_null_position(self):
        return self.null_pos

    def set_bar_style(self, style: BarStyleStr | RoundProgressBar.BarStyle):
        if isinstance(style, str):
            bar_style = dict(
                donut=RoundProgressBar.BarStyle.Donut,
                pie=RoundProgressBar.BarStyle.Pie,
                line=RoundProgressBar.BarStyle.Line,
                expand=RoundProgressBar.BarStyle.Expand,
            )
            style = bar_style[style]
        if style != self.bar_style:
            self.bar_style = style
            self._rebuild_brush = True
            self.update()

    def set_outline_pen_width(self, width: float):
        if width != self.outline_pen_width:
            self.outline_pen_width = width
            self.update()

    def set_data_pen_width(self, width: float):
        if width != self.data_pen_width:
            self.data_pen_width = width
            self.update()

    def set_data_colors(self, stop_points: list[gui.QColor]):
        if stop_points != self.gradient_data:
            self.gradient_data = stop_points
            self._rebuild_brush = True
            self.update()

    def set_format(self, val: str):
        if val != self.number_format:
            self.number_format = val
            self._value_format_changed()

    def set_decimals(self, count: int):
        if count >= 0 and count != self.decimals:
            self.decimals = count
            self._value_format_changed()

    # SLOTS ---------------------------------------------------------

    @core.Slot(float, float)
    def set_range(self, minval: float, maxval: float):
        self._min_value = min(minval, maxval)
        self._max_value = max(minval, maxval)
        self.current_value = min(
            self._max_value, max(self._min_value, self.current_value)
        )
        self._rebuild_brush = True
        self.update()

    @core.Slot(float)
    def setMinimum(self, val: float):
        self.set_range(val, self._max_value)

    @core.Slot(float)
    def setMaximum(self, val: float):
        self.set_range(self._min_value, val)

    @core.Slot(float)
    def set_value(self, val: float):
        if self.current_value != val:
            self.current_value = min(self._max_value, max(self._min_value, val))
            self.update()

    def get_value(self) -> float:
        return self.current_value

    # PAINTING ------------------------------------------------------

    def paintEvent(self, event: gui.PaintEvent):
        outer_radius = min(self.width(), self.height())
        rect = core.RectF(1, 1, outer_radius - 2, outer_radius - 2)
        with gui.Painter(self) as painter:
            painter.use_antialiasing()
            if self.bar_style != self.BarStyle.Line:
                self._rebuild_data_brush_if_needed()
            painter.fillRect(0, 0, outer_radius, outer_radius, self.palette().window())
            self._draw_base(painter, rect)
            self._draw_value(painter, rect, self.current_value)
            inner_rect, inner_radius = self._calculate_inner_rect(outer_radius)
            self._draw_inner_background(painter, inner_rect)
            self._draw_text(painter, inner_rect, inner_radius, self.current_value)

    def _draw_base(self, painter: gui.Painter, rect: core.RectF):
        match self.bar_style:
            case self.BarStyle.Donut:
                color = self.palette().shadow().color()
                painter.set_pen(color=color, width=self.outline_pen_width)
                painter.setBrush(self.palette().base())
                painter.drawEllipse(rect)
            case self.BarStyle.Line:
                base_color = self.palette().base().color()
                painter.set_pen(color=base_color, width=self.outline_pen_width)
                painter.setBrush(constants.BrushStyle.NoBrush)
                width = self.outline_pen_width / 2
                adjusted = rect.adjusted(width, width, -width, -width)
                painter.drawEllipse(adjusted)
            case self.BarStyle.Pie | self.BarStyle.Expand:
                base_color = self.palette().base().color()
                painter.set_pen(color=base_color, width=self.outline_pen_width)
                painter.setBrush(self.palette().base())
                painter.drawEllipse(rect)

    def _draw_value(self, painter: gui.Painter, rect: core.RectF, value: float):
        if value == self._min_value:
            return
        diff = self.current_value - self._min_value
        value_range = self._max_value - self._min_value
        delta = max(value_range / diff, 0)
        match self.bar_style:
            case self.BarStyle.Expand:
                painter.setBrush(self.palette().highlight())
                color = self.palette().shadow().color()
                painter.set_pen(color=color, width=self.data_pen_width)
                radius = (rect.height() / 2) / delta
                painter.drawEllipse(rect.center(), radius, radius)
            case self.BarStyle.Line:
                color = self.palette().highlight().color()
                painter.set_pen(color=color, width=self.data_pen_width)
                painter.setBrush(constants.BrushStyle.NoBrush)
                pen_width = self.outline_pen_width / 2
                adjusted = rect.adjusted(pen_width, pen_width, -pen_width, -pen_width)
                if value == self._max_value:
                    painter.drawEllipse(adjusted)
                else:
                    arc_length = 360 / delta
                    arc_length = int(-arc_length * 16)
                    painter.drawArc(adjusted, int(self.null_pos * 16), arc_length)
            case self.BarStyle.Donut | self.BarStyle.Pie:
                data_path = gui.PainterPath()
                data_path.set_fill_rule("winding")
                if value == self._max_value:
                    data_path.addEllipse(rect)
                else:
                    arc_length = 360 / delta
                    center_point = rect.center()
                    data_path.moveTo(center_point)
                    data_path.arcTo(rect, self.null_pos, -arc_length)
                    data_path.lineTo(center_point)
                painter.setBrush(self.palette().highlight())
                shadow_color = self.palette().shadow().color()
                painter.set_pen(color=shadow_color, width=self.data_pen_width)
                painter.drawPath(data_path)

    def _calculate_inner_rect(self, outer_radius: float) -> tuple[core.RectF, float]:
        if self.bar_style in (self.BarStyle.Line, self.BarStyle.Expand):
            inner_radius = outer_radius - self.outline_pen_width
        else:
            inner_radius = outer_radius * 0.75
        delta = (outer_radius - inner_radius) / 2
        inner_rect = core.RectF(delta, delta, inner_radius, inner_radius)
        return inner_rect, inner_radius

    def _draw_inner_background(self, painter: gui.Painter, inner_rect: core.RectF):
        if self.bar_style == self.BarStyle.Donut:
            painter.setBrush(self.palette().base())
            painter.drawEllipse(inner_rect)

    def _draw_text(
        self,
        painter: gui.Painter,
        inner_rect: core.RectF,
        inner_radius: float,
        value: float,
    ):
        if not self.number_format:
            return
        font = self.get_font()
        font.setPixelSize(10)
        metrics = gui.FontMetricsF(font)
        max_width = metrics.horizontalAdvance(self._value_to_text(self._max_value))
        delta = inner_radius / max_width
        font_size = int(font.pixelSize() * delta * 0.75)
        font.setPixelSize(max(font_size, 1))
        painter.setFont(font)
        painter.setPen(self.palette().text().color())
        text = self._value_to_text(value)
        painter.drawText(inner_rect, constants.ALIGN_CENTER, text)  # type: ignore

    def _value_to_text(self, value: float) -> str:
        text_to_draw = self.number_format
        match self._update_flags:
            case "value":
                val = round(value, self.decimals)
                return text_to_draw.replace(r"%v", str(val))
            case "percent":
                diff = self._max_value - self._min_value
                pct = (value - self._min_value) / diff * 100
                val = round(pct, self.decimals)
                return text_to_draw.replace(r"%p", str(val))
            case "max":
                val = round(self._max_value - self._min_value + 1, self.decimals)
                return text_to_draw.replace(r"%m", str(val))
            case _:
                raise ValueError(self._update_flags)

    def _value_format_changed(self):
        for k, v in VALUE_MAP.items():
            if k in self.number_format:
                self._update_flags = v
        self.update()

    def _rebuild_data_brush_if_needed(self):
        if not self._rebuild_brush or not self.gradient_data:
            return
        self._rebuild_brush = False
        if self.bar_style == "expand":
            data_brush = gui.RadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
            for i in self.gradient_data:
                data_brush[i[0]] = i[1]
        else:
            data_brush = gui.ConicalGradient(0.5, 0.5, self.null_pos)
            for i in self.gradient_data:
                data_brush[1 - i[0]] = i[1]
        data_brush.set_coordinate_mode("stretch_to_device")
        with self.edit_palette() as palette:
            palette.set_brush("highlight", data_brush)

    nullPosition = core.Property(  # noqa: N815
        enum.Enum,
        get_null_position,
        set_null_position,
        doc="Position for value = 0",
    )


if __name__ == "__main__":
    app = widgets.app()
    pb = RoundProgressBar()
    pb.set_bar_style("pie")
    pb.show()
    app.exec()

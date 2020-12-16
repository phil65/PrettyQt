from typing import Dict, List, Literal, Optional, Tuple

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError


BAR_STYLE = ["donut", "pie", "line", "expand"]
BarStyleStr = Literal["donut", "pie", "line", "expand"]

VALUE_TYPE = ["value", "percent", "max"]
ValueTypeStr = Literal["value", "percent", "max"]

VALUE_MAP: Dict[str, ValueTypeStr] = {
    r"%v": "value",
    r"%p": "percent",
    r"%m": "max",
}


class RoundProgressBar(widgets.Widget):
    # CONSTANTS

    POSITION_LEFT = 180.0
    POSITION_TOP = 90.0
    POSITION_RIGHT = 0.0
    POSITION_BOTTOM = -90.0

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.min_value = 0.0
        self.max_value = 100.0
        self.current_value = 0.0
        self.null_pos = self.POSITION_TOP
        self.bar_style: BarStyleStr = "donut"
        self.outline_pen_width = 1.0
        self.data_pen_width = 1.0
        self._rebuild_brush = False
        self.number_format = "%p%"
        self.decimals = 1
        self._update_flags: ValueTypeStr = "percent"
        self.gradient_data: List[QtGui.QColor] = list()

    def minimum(self):
        return self.min_value

    def maximum(self):
        return self.max_value

    # SETTERS -------------------------------------------------------

    def set_null_position(self, position: float):
        if position != self.null_pos:
            self.null_pos = position
            self._rebuild_brush = True
            self.update()

    def set_bar_style(self, style: BarStyleStr):
        if style not in BAR_STYLE:
            raise InvalidParamError(style, BAR_STYLE)
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

    def set_data_colors(self, stop_points: List[QtGui.QColor]):
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
        self.min_value = min(minval, maxval)
        self.max_value = max(minval, maxval)
        self.current_value = min(self.max_value, max(self.min_value, self.current_value))
        self._rebuild_brush = True
        self.update()

    @core.Slot(float)
    def setMinimum(self, val: float):
        self.set_range(val, self.max_value)

    @core.Slot(float)
    def setMaximum(self, val: float):
        self.set_range(self.min_value, val)

    @core.Slot(float)
    def set_value(self, val: float):
        if self.current_value != val:
            self.current_value = min(self.max_value, max(self.min_value, val))
            self.update()

    def get_value(self) -> float:
        return self.current_value

    # PAINTING ------------------------------------------------------

    def paintEvent(self, event: gui.PaintEvent):
        outer_radius = min(self.width(), self.height())
        rect = core.RectF(1, 1, outer_radius - 2, outer_radius - 2)
        with gui.Painter(self) as painter:
            painter.use_antialiasing()
            if self.bar_style != "line":
                self._rebuild_data_brush_if_needed()
            bg_rect = core.RectF(0, 0, outer_radius, outer_radius)
            painter.fillRect(bg_rect, self.palette().window())
            self._draw_base(painter, rect)
            self._draw_value(painter, rect, self.current_value)
            inner_rect, inner_radius = self._calculate_inner_rect(outer_radius)
            self._draw_inner_background(painter, inner_rect)
            self._draw_text(painter, inner_rect, inner_radius, self.current_value)

    def _draw_base(self, painter: gui.Painter, rect: core.RectF):
        if self.bar_style == "donut":
            painter.setPen(
                gui.Pen(self.palette().shadow().color(), self.outline_pen_width)
            )
            painter.setBrush(self.palette().base())
            painter.drawEllipse(rect)
        elif self.bar_style == "line":
            painter.setPen(gui.Pen(self.palette().base().color(), self.outline_pen_width))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawEllipse(
                rect.adjusted(
                    self.outline_pen_width / 2,
                    self.outline_pen_width / 2,
                    -self.outline_pen_width / 2,
                    -self.outline_pen_width / 2,
                )
            )
        elif self.bar_style in ("pie", "expand"):
            painter.setPen(gui.Pen(self.palette().base().color(), self.outline_pen_width))
            painter.setBrush(self.palette().base())
            painter.drawEllipse(rect)

    def _draw_value(self, painter: gui.Painter, rect: core.RectF, value: float):
        if value == self.min_value:
            return
        diff = self.current_value - self.min_value
        value_range = self.max_value - self.min_value
        delta = max(value_range / diff, 0)
        if self.bar_style == "expand":
            painter.setBrush(self.palette().highlight())
            painter.setPen(gui.Pen(self.palette().shadow().color(), self.data_pen_width))
            radius = (rect.height() / 2) / delta
            painter.drawEllipse(rect.center(), radius, radius)
            return
        elif self.bar_style == "line":
            painter.setPen(
                gui.Pen(self.palette().highlight().color(), self.data_pen_width)
            )
            painter.setBrush(QtCore.Qt.NoBrush)
            p1_width = self.outline_pen_width / 2
            p2_width = -self.outline_pen_width / 2
            adjusted = rect.adjusted(p1_width, p1_width, p2_width, p2_width)
            if value == self.max_value:
                painter.drawEllipse(adjusted)
            else:
                arc_length = 360 / delta
                painter.drawArc(adjusted, int(self.null_pos * 16), int(-arc_length * 16))
            return
        data_path = gui.PainterPath()
        data_path.set_fill_rule("winding")
        if value == self.max_value:
            data_path.addEllipse(rect)
        else:
            arc_length = 360 / delta
            data_path.moveTo(rect.center())
            data_path.arcTo(rect, self.null_pos, -arc_length)
            data_path.lineTo(rect.center())
        painter.setBrush(self.palette().highlight())
        painter.setPen(gui.Pen(self.palette().shadow().color(), self.data_pen_width))
        painter.drawPath(data_path)

    def _calculate_inner_rect(self, outer_radius: float) -> Tuple[core.RectF, float]:
        if self.bar_style in ("line", "expand"):
            inner_radius = outer_radius - self.outline_pen_width
        else:
            inner_radius = outer_radius * 0.75
        delta = (outer_radius - inner_radius) / 2
        inner_rect = core.RectF(delta, delta, inner_radius, inner_radius)
        return inner_rect, inner_radius

    def _draw_inner_background(self, painter: gui.Painter, inner_rect: core.RectF):
        if self.bar_style == "donut":
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
        max_width = metrics.width(self._value_to_text(self.max_value))
        delta = inner_radius / max_width
        font_size = int(font.pixelSize() * delta * 0.75)
        font.setPixelSize(max(font_size, 1))
        painter.setFont(font)
        painter.setPen(self.palette().text().color())
        painter.drawText(inner_rect, QtCore.Qt.AlignCenter, self._value_to_text(value))

    def _value_to_text(self, value: float) -> str:
        text_to_draw = self.number_format
        if self._update_flags == "value":
            val = round(value, self.decimals)
            return text_to_draw.replace(r"%v", str(val))
        elif self._update_flags == "percent":
            procent = (value - self.min_value) / (self.max_value - self.min_value) * 100
            val = round(procent, self.decimals)
            return text_to_draw.replace(r"%p", str(val))
        elif self._update_flags == "max":
            val = round(self.max_value - self.min_value + 1, self.decimals)
            return text_to_draw.replace(r"%m", str(val))

    def _value_format_changed(self):
        for k, v in VALUE_MAP.items():
            if k in self.number_format:
                self._update_flags = v
        self.update()

    def _rebuild_data_brush_if_needed(self):
        if not self._rebuild_brush or not self.gradient_data:
            return
        self._rebuild_brush = False
        with self.edit_palette() as palette:
            if self.bar_style == "expand":
                data_brush = gui.RadialGradient(0.5, 0.5, 0.5, 0.5, 0.5)
                for i in self.gradient_data:
                    data_brush[i[0]] = i[1]
            else:
                data_brush = gui.ConicalGradient(0.5, 0.5, self.null_pos)
                for i in self.gradient_data:
                    data_brush[1 - i[0]] = i[1]
            data_brush.set_coordinate_mode("stretch_to_device")
            palette.set_brush("highlight", data_brush)


if __name__ == "__main__":
    app = widgets.app()
    pb = RoundProgressBar()
    pb.set_bar_style("donut")
    pb.show()
    app.main_loop()

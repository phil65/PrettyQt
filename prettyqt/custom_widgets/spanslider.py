# The MIT License (MIT)

# Copyright (c) 2011-2014 Marvin Killing

from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import colors, types


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


SLIDER_STYLE = widgets.Style.ComplexControl.CC_Slider
HANDLE_STYLE = widgets.Style.SubControl.SC_SliderHandle
GROOVE_STYLE = widgets.Style.SubControl.SC_SliderGroove


MOVEMENT_MODE = ["no_crossing", "no_overlap", "free"]

MovementModeStr = Literal["no_crossing", "no_overlap", "free"]

HandleStr = Literal["upper", "lower"]

ActionStr = Literal[
    "single_step_add", "single_step_sub", "to_minimum", "to_maximum", "move", "none"
]


def clamp(v: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, v))


class SpanSlider(widgets.Slider):
    value_changed = core.Signal(object)
    lower_pos_changed = core.Signal(float)
    upper_pos_changed = core.Signal(float)
    slider_pressed = core.Signal(object)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__("horizontal", parent)
        self.rangeChanged.connect(self.update_range)
        self.sliderReleased.connect(self._move_pressed_handle)

        self.lower_val = 0.0
        self.upper_val = 0.0
        self.lower_pos = 0.0
        self.upper_pos = 0.0
        self.offset = 0
        self.position = 0.0
        self.last_pressed: str | None = None
        self.upper_pressed = widgets.Style.SubControl.SC_None
        self.lower_pressed = widgets.Style.SubControl.SC_None
        self.movement: MovementModeStr = "no_crossing"
        self._main_control: Literal["lower", "upper"] = "lower"
        self._first_movement = False
        self._block_tracking = False
        dark_color = self.palette().color(gui.Palette.ColorRole.Dark)
        self.gradient_left = dark_color.lighter(110)
        self.gradient_right = dark_color.lighter(110)

    def mousePressEvent(self, event):
        if self.minimum() == self.maximum() or event.buttons() ^ event.button():
            event.ignore()
            return

        self.upper_pressed = self._handle_mouse_press(
            event.position(), self.upper_pressed, self.upper_val, "upper"
        )
        if self.upper_pressed != HANDLE_STYLE:
            self.lower_pressed = self._handle_mouse_press(
                event.position(), self.lower_pressed, self.lower_val, "lower"
            )

        self._first_movement = True
        event.accept()

    def mouseMoveEvent(self, event):
        if self.lower_pressed != HANDLE_STYLE and self.upper_pressed != HANDLE_STYLE:
            event.ignore()
            return

        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        m = self.style().pixelMetric(
            widgets.Style.PixelMetric.PM_MaximumDragDistance, opt, self
        )
        pixel_pos = self.pick(event.position()) - self.offset
        new_pos = float(self._pixel_pos_to_value(pixel_pos))
        if m >= 0:
            r = self.rect().adjusted(-m, -m, m, m)
            if not r.contains(event.position()):
                new_pos = self.position

        # pick the preferred handle on the first movement
        if self._first_movement:
            if self.lower_val == self.upper_val:
                if new_pos < self.lower_value:
                    self._swap_controls()
                    self._first_movement = False
            else:
                self._first_movement = False

        if self.lower_pressed == HANDLE_STYLE:
            if self.movement == "no_crossing":
                new_pos = min(new_pos, self.upper_val)
            elif self.movement == "no_overlap":
                new_pos = min(new_pos, self.upper_val - 1)

            if self.movement == "free" and new_pos > self.upper_val:
                self._swap_controls()
                self.set_upper_pos(new_pos)
            else:  # movement "none"
                self.set_lower_pos(new_pos)
        elif self.upper_pressed == HANDLE_STYLE:
            if self.movement == "no_crossing":
                new_pos = max(new_pos, self.lower_value)
            elif self.movement == "no_overlap":
                new_pos = max(new_pos, self.lower_value + 1)

            if self.movement == "free" and new_pos < self.lower_val:
                self._swap_controls()
                self.set_lower_pos(new_pos)
            else:  # movement "none"
                self.set_upper_pos(new_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setSliderDown(False)
        self.lower_pressed = self.upper_pressed = widgets.Style.SubControl.SC_None
        self.update()

    def paintEvent(self, event):
        painter = widgets.StylePainter(self)

        # ticks
        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        opt.subControls = widgets.Style.SubControl.SC_SliderTickmarks
        painter.draw_complex_control("slider", opt)

        # groove
        opt.sliderPosition = 20
        opt.sliderValue = 0
        opt.subControls = GROOVE_STYLE
        painter.draw_complex_control("slider", opt)

        # handle rects
        opt.sliderPosition = self.lower_pos
        lr = self.style().subControlRect(SLIDER_STYLE, opt, HANDLE_STYLE, self)
        lrv = self.pick(lr.center())
        opt.sliderPosition = self.upper_pos
        ur = self.style().subControlRect(SLIDER_STYLE, opt, HANDLE_STYLE, self)
        urv = self.pick(ur.center())

        # span
        minv = min(lrv, urv)
        maxv = max(lrv, urv)
        c = self.style().subControlRect(SLIDER_STYLE, opt, GROOVE_STYLE, self).center()
        if self.is_horizontal():
            rect = core.Rect(core.Point(minv, c.y() - 2), core.Point(maxv, c.y() + 1))
        else:
            rect = core.Rect(core.Point(c.x() - 2, minv), core.Point(c.x() + 1, maxv))
        self._draw_span(painter, rect)

        # handles
        if self.last_pressed == "lower":
            self.draw_handle(painter, "upper")
            self.draw_handle(painter, "lower")
        else:
            self.draw_handle(painter, "lower")
            self.draw_handle(painter, "upper")

    @core.Property(float)
    def lower_value(self) -> float:
        return min(self.lower_val, self.upper_val)

    def set_lower_value(self, lower: float):
        self.set_span(lower, self.upper_val)

    @core.Property(float)
    def upper_value(self) -> float:
        return max(self.lower_val, self.upper_val)

    def set_upper_value(self, upper: float):
        self.set_span(self.lower_val, upper)

    def on_value_change(self):
        self.value_changed.emit((self.lower_val, self.upper_val))

    def get_value(self) -> tuple[float, float]:
        return (self.lower_val, self.upper_val)

    def set_value(self, value: tuple[float, float]):
        self.set_lower_value(value[0])
        self.set_upper_value(value[1])

    def get_movement_mode(self) -> MovementModeStr:
        return self.movement

    def set_movement_mode(self, mode: MovementModeStr):
        """Set movement mode.

        Args:
            mode: movement mode for the main window

        Raises:
            ValueError: movement mode type does not exist
        """
        if mode not in MOVEMENT_MODE:
            raise ValueError("Invalid movement mode")
        self.movement = mode

    def set_span(self, lower: float, upper: float):
        low = clamp(min(lower, upper), self.minimum(), self.maximum())
        upp = clamp(max(lower, upper), self.minimum(), self.maximum())
        changed = False
        if low != self.lower_val:
            self.lower_val = low
            self.lower_pos = low
            changed = True
        if upp != self.upper_val:
            self.upper_val = upp
            self.upper_pos = upp
            changed = True
        if changed:
            self.on_value_change()
            self.update()

    def set_lower_pos(self, lower: float):
        if self.lower_pos == lower:
            return
        self.lower_pos = lower
        if not self.hasTracking():
            self.update()
        if self.isSliderDown():
            self.lower_pos_changed.emit(lower)
        if self.hasTracking() and not self._block_tracking:
            main = self._main_control == "lower"
            self.trigger_action("move", main)

    def set_upper_pos(self, upper: float):
        if self.upper_pos == upper:
            return
        self.upper_pos = upper
        if not self.hasTracking():
            self.update()
        if self.isSliderDown():
            self.upper_pos_changed.emit(upper)
        if self.hasTracking() and not self._block_tracking:
            main = self._main_control == "upper"
            self.trigger_action("move", main)

    def set_left_color(self, color: types.ColorType):
        self.gradient_left = colors.get_color(color)
        self.update()

    def set_right_color(self, color: types.ColorType):
        self.gradient_right = colors.get_color(color)
        self.update()

    def _move_pressed_handle(self):
        if self.last_pressed == "lower":
            if self.lower_pos != self.lower_val:
                main = self._main_control == "lower"
                self.trigger_action("move", main)
        elif self.last_pressed == "upper":
            if self.upper_pos != self.upper_val:
                main = self._main_control == "upper"
                self.trigger_action("move", main)

    def pick(self, p: types.PointType) -> int:
        if isinstance(p, tuple):
            return p[0] if self.is_horizontal() else p[1]
        else:
            return p.x() if self.is_horizontal() else p.y()

    def trigger_action(self, action: ActionStr, main: bool):
        value = 0.0
        no = False
        up = False
        my_min = self.minimum()
        my_max = self.maximum()
        self._block_tracking = True
        main_control = main and self._main_control == "upper"
        alt_control = not main and self._main_control == "lower"
        is_upper_handle = main_control or alt_control
        val = self.upper_val if is_upper_handle else self.lower_val
        if action == "single_step_add":
            up = is_upper_handle
            value = clamp(val + self.singleStep(), my_min, my_max)
        elif action == "single_step_sub":
            up = is_upper_handle
            value = clamp(val - self.singleStep(), my_min, my_max)
        elif action == "to_minimum":
            up = is_upper_handle
            value = my_min
        elif action == "to_maximum":
            up = is_upper_handle
            value = my_max
        elif action == "move":
            up = is_upper_handle
            no = True
        elif action == "none":
            no = True

        if not no and not up:
            if self.movement == "no_crossing":
                value = min(value, self.upper_val)
            elif self.movement == "no_overlap":
                value = min(value, self.upper_val - 1)

            if self.movement == "free" and value > self.upper_val:
                self._swap_controls()
                self.set_upper_pos(value)
            else:
                self.set_lower_pos(value)
        elif not no:
            if self.movement == "no_crossing":
                value = max(value, self.lower_val)
            elif self.movement == "no_overlap":
                value = max(value, self.lower_val + 1)

            if self.movement == "free" and value < self.lower_val:
                self._swap_controls()
                self.set_lower_pos(value)
            else:
                self.set_upper_pos(value)

        self._block_tracking = False
        self.set_lower_value(self.lower_pos)
        self.set_upper_value(self.upper_pos)

    def _swap_controls(self):
        self.lower_val, self.upper_val = self.upper_val, self.lower_val
        self.lower_pressed, self.upper_pressed = self.upper_pressed, self.lower_pressed
        self.last_pressed = "upper" if self.last_pressed == "lower" else "lower"
        self._main_control = "upper" if self._main_control == "lower" else "lower"

    def update_range(self, min_, max_):
        # set_span() takes care of keeping span in range
        self.set_span(self.lower_val, self.upper_val)

    def _setup_painter(
        self,
        painter: widgets.StylePainter,
        orientation: Literal["horizontal", "vertical"],
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):
        highlight = self.palette().color(gui.Palette.ColorRole.Highlight)
        gradient = gui.LinearGradient(x1, y1, x2, y2)
        gradient[0] = highlight.darker(120)
        gradient[1] = highlight.lighter(108)
        painter.setBrush(gradient)

        val = 130 if orientation == "horizontal" else 150
        painter.set_pen(color=highlight.darker(val), width=0)

    def _draw_span(self, painter: widgets.StylePainter, rect: core.Rect):
        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        painter.set_pen(color=self.gradient_left, width=0)
        groove = self.style().subControlRect(SLIDER_STYLE, opt, GROOVE_STYLE, self)
        if opt.is_horizontal():
            groove.adjust(0, 0, -1, 0)
            self._setup_painter(
                painter,
                opt.get_orientation(),
                groove.center().x(),
                groove.top(),
                groove.center().x(),
                groove.bottom(),
            )
        else:
            groove.adjust(0, 0, 0, -1)
            self._setup_painter(
                painter,
                opt.get_orientation(),
                groove.left(),
                groove.center().y(),
                groove.right(),
                groove.center().y(),
            )

        # draw groove
        intersected = core.RectF(rect.intersected(groove))
        gradient = gui.LinearGradient(intersected.topLeft(), intersected.topRight())
        gradient[0] = self.gradient_left
        gradient[1] = self.gradient_right
        painter.fillRect(intersected, gradient)

    def draw_handle(self, painter: widgets.StylePainter, handle: HandleStr):
        opt = self.get_style_option(handle)
        opt.subControls = HANDLE_STYLE
        pressed = self.upper_pressed
        if handle == "lower":
            pressed = self.lower_pressed

        if pressed == HANDLE_STYLE:
            opt.activeSubControls = pressed
            opt.state |= widgets.Style.StateFlag.State_Sunken
        painter.draw_complex_control("slider", opt)

    def get_style_option(self, handle: HandleStr) -> widgets.StyleOptionSlider:
        option = widgets.StyleOptionSlider()
        self.initStyleOption(option)
        if handle == "lower":
            option.sliderPosition = self.lower_pos
            option.sliderValue = self.lower_val
        else:
            option.sliderPosition = self.upper_pos
            option.sliderValue = self.upper_val
        return option

    def _handle_mouse_press(
        self, pos: QtCore.QPoint, control, value: float, handle: HandleStr
    ):
        opt = self.get_style_option(handle)
        old_control = control
        control = self.style().hitTestComplexControl(SLIDER_STYLE, opt, pos, self)
        sr = self.style().subControlRect(SLIDER_STYLE, opt, HANDLE_STYLE, self)
        if control == HANDLE_STYLE:
            self.position = value
            self.offset = self.pick(pos - sr.topLeft())
            self.last_pressed = handle
            self.setSliderDown(True)
            self.slider_pressed.emit(handle)
        if control != old_control:
            self.update(sr)
        return control

    def _pixel_pos_to_value(self, pos: int) -> int:
        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(SLIDER_STYLE, opt, GROOVE_STYLE, self)
        sr = self.style().subControlRect(SLIDER_STYLE, opt, HANDLE_STYLE, self)
        if self.is_horizontal():
            len_slider = sr.width()
            slider_min = gr.x()
            slider_end = gr.right()
        else:
            len_slider = sr.height()
            slider_min = gr.y()
            slider_end = gr.bottom()

        return widgets.Style.sliderValueFromPosition(
            self.minimum(),
            self.maximum(),
            pos - slider_min,
            slider_end - len_slider + 1 - slider_min,
            opt.upsideDown,
        )


class SpanSliderWidget(widgets.Widget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.set_layout("grid")
        self.slider = SpanSlider()
        self.label_lower = widgets.Label()
        self.label_upper = widgets.Label()
        self.box[0, 0:3] = self.slider
        self.box[1, 0] = self.label_lower
        self.box[1, 3] = self.label_upper
        self.slider.value_changed.connect(self.on_value_change)

    def __getattr__(self, value):
        return self.slider.__getattribute__(value)

    def on_value_change(self):
        self.label_lower.set_text(str(self.slider.lower_pos))
        self.label_upper.set_text(str(self.slider.upper_pos))


if __name__ == "__main__":
    app = widgets.app()
    layout = widgets.BoxLayout("horizontal")
    slider = SpanSliderWidget()
    slider.set_span(30, 70)
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    # color = gui.Color("blue").lighter(150)
    # slider.set_left_color(color)
    # slider.set_right_color(color)
    slider.show()
    app.main_loop()

# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2011-2014 Marvin Killing

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

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets

SLIDER_STYLE = widgets.Style.CC_Slider
HANDLE_STYLE = widgets.Style.SC_SliderHandle
GROOVE_STYLE = widgets.Style.SC_SliderGroove


def clamp(v, lower, upper):
    return min(upper, max(lower, v))


class SpanSlider(widgets.Slider):
    NO_HANDLE = None
    LOWER_HANDLE = 1
    UPPER_HANDLE = 2

    value_changed = core.Signal(int, int)
    lower_pos_changed = core.Signal(int)
    upper_pos_changed = core.Signal(int)
    slider_pressed = core.Signal(object)

    def __init__(self, parent=None):
        QtWidgets.QSlider.__init__(self, QtCore.Qt.Horizontal, parent)
        self.rangeChanged.connect(self.update_range)
        self.sliderReleased.connect(self.move_pressed_handle)

        self.lower = 0
        self.upper = 0
        self.lower_pos = 0
        self.upper_pos = 0
        self.offset = 0
        self.position = 0
        self.last_pressed = self.NO_HANDLE
        self.upper_pressed = widgets.Style.SC_None
        self.lower_pressed = widgets.Style.SC_None
        self.movement = "free"
        self.main_control = self.LOWER_HANDLE
        self.first_movement = False
        self.block_tracking = False
        self.gradient_left = self.palette().color(gui.Palette.Dark).lighter(110)
        self.gradient_right = self.palette().color(gui.Palette.Dark).lighter(110)

    @core.Property(int)
    def lower_value(self):
        return min(self.lower, self.upper)

    def set_lower_value(self, lower):
        self.set_span(lower, self.upper)

    @core.Property(int)
    def upper_value(self):
        return max(self.lower, self.upper)

    def set_upper_value(self, upper):
        self.set_span(self.lower, upper)

    @core.Property(object)
    def movement_mode(self):
        return self.movement

    def set_movement_mode(self, mode):
        self.movement = mode

    def set_span(self, lower, upper):
        low = clamp(min(lower, upper), self.minimum(), self.maximum())
        upp = clamp(max(lower, upper), self.minimum(), self.maximum())
        changed = False
        if low != self.lower:
            self.lower = low
            self.lower_pos = low
            changed = True
        if upp != self.upper:
            self.upper = upp
            self.upper_pos = upp
            changed = True
        if changed:
            self.value_changed.emit(self.lower, self.upper)
            self.update()

    def set_lower_pos(self, lower):
        if self.lower_pos == lower:
            return None
        self.lower_pos = lower
        if not self.hasTracking():
            self.update()
        if self.isSliderDown():
            self.lower_pos_changed.emit(lower)
        if self.hasTracking() and not self.block_tracking:
            main = self.main_control == self.LOWER_HANDLE
            self.trigger_action(self.SliderMove, main)

    def set_upper_pos(self, upper):
        if self.upper_pos == upper:
            return None
        self.upper_pos = upper
        if not self.hasTracking():
            self.update()
        if self.isSliderDown():
            self.upper_pos_changed.emit(upper)
        if self.hasTracking() and not self.block_tracking:
            main = self.main_control == self.UPPER_HANDLE
            self.trigger_action(self.SliderMove, main)

    @core.Property(object)
    def left_color(self):
        return self.gradient_left

    def set_left_color(self, color):
        self.gradient_left = color
        self.update()

    @core.Property(object)
    def right_color(self):
        return self.gradient_right

    def set_right_color(self, color):
        self.gradient_right = color
        self.update()

    def move_pressed_handle(self):
        if self.last_pressed == self.LOWER_HANDLE:
            if self.lower_pos != self.lower:
                main = self.main_control == self.LOWER_HANDLE
                self.trigger_action(self.SliderMove, main)
        elif self.last_pressed == self.UPPER_HANDLE:
            if self.upper_pos != self.upper:
                main = self.main_control == self.UPPER_HANDLE
                self.trigger_action(self.SliderMove, main)

    def pick(self, p):
        return p.x() if self.is_horizontal() else p.y()

    def trigger_action(self, action, main):
        value = 0
        no = False
        up = False
        my_min = self.minimum()
        my_max = self.maximum()
        alt_control = self.LOWER_HANDLE
        if self.main_control == self.LOWER_HANDLE:
            alt_control = self.UPPER_HANDLE

        self.block_tracking = True
        main_control = main and self.main_control == self.UPPER_HANDLE
        alt_control = not main and alt_control == self.UPPER_HANDLE
        is_upper_handle = main_control or alt_control
        val = self.upper if is_upper_handle else self.lower
        if action == self.SliderSingleStepAdd:
            up = is_upper_handle
            value = clamp(val + self.singleStep(), my_min, my_max)
        elif action == self.SliderSingleStepSub:
            up = is_upper_handle
            value = clamp(val - self.singleStep(), my_min, my_max)
        elif action == self.SliderToMinimum:
            value = my_min
            up = is_upper_handle
        elif action == self.SliderToMaximum:
            value = my_max
            up = is_upper_handle
        elif action == self.SliderMove:
            up = is_upper_handle
            no = True
        elif action == self.SliderNoAction:
            no = True

        if not no and not up:
            if self.movement == "no_crossing":
                value = min(value, self.upper)
            elif self.movement == "no_overlap":
                value = min(value, self.upper - 1)

            if self.movement == "free" and value > self.upper:
                self.swap_controls()
                self.set_upper_pos(value)
            else:
                self.set_lower_pos(value)
        elif not no:
            if self.movement == "no_crossing":
                value = max(value, self.lower)
            elif self.movement == "no_overlap":
                value = max(value, self.lower + 1)

            if self.movement == "free" and value < self.lower:
                self.swap_controls()
                self.set_lower_pos(value)
            else:
                self.set_upper_pos(value)

        self.block_tracking = False
        self.set_lower_value(self.lower_pos)
        self.set_upper_value(self.upper_pos)

    def swap_controls(self):
        self.lower, self.upper = self.upper, self.lower
        self.lower_pressed, self.upper_pressed = self.upper_pressed, self.lower_pressed
        self.last_pressed = (self.UPPER_HANDLE if
                             self.last_pressed == self.LOWER_HANDLE
                             else self.LOWER_HANDLE)
        self.main_control = (self.UPPER_HANDLE if
                             self.main_control == self.LOWER_HANDLE
                             else self.LOWER_HANDLE)

    def update_range(self, min_, max_):
        # set_span() takes care of keeping span in range
        self.set_span(self.lower, self.upper)

    def paintEvent(self, event):
        painter = widgets.StylePainter(self)

        # ticks
        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        opt.subControls = widgets.Style.SC_SliderTickmarks
        painter.drawComplexControl(SLIDER_STYLE, opt)

        # groove
        opt.sliderPosition = 20
        opt.sliderValue = 0
        opt.subControls = GROOVE_STYLE
        painter.drawComplexControl(SLIDER_STYLE, opt)

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
        spanRect = core.Rect(core.Point(c.x() - 2, minv),
                             core.Point(c.x() + 1, maxv))
        if self.is_horizontal():
            spanRect = core.Rect(core.Point(minv, c.y() - 2),
                                 core.Point(maxv, c.y() + 1))
        self.draw_span(painter, spanRect)

        # handles
        if self.last_pressed == self.LOWER_HANDLE:
            self.draw_handle(painter, self.UPPER_HANDLE)
            self.draw_handle(painter, self.LOWER_HANDLE)
        else:
            self.draw_handle(painter, self.LOWER_HANDLE)
            self.draw_handle(painter, self.UPPER_HANDLE)

    def setup_painter(self, painter, orientation, x1, y1, x2, y2):
        highlight = self.palette().color(gui.Palette.Highlight)
        gradient = QtGui.QLinearGradient(x1, y1, x2, y2)
        gradient.setColorAt(0, highlight.darker(120))
        gradient.setColorAt(1, highlight.lighter(108))
        painter.setBrush(gradient)

        val = 130 if orientation == QtCore.Qt.Horizontal else 150
        painter.setPen(gui.Pen(highlight.darker(val), 0))

    def draw_span(self, painter, rect):
        opt = widgets.StyleOptionSlider()
        super().initStyleOption(opt)

        # area
        groove = self.style().subControlRect(SLIDER_STYLE, opt, GROOVE_STYLE, self)
        if opt.is_horizontal():
            groove.adjust(0, 0, -1, 0)
        else:
            groove.adjust(0, 0, 0, -1)

        # pen & brush
        painter.setPen(gui.Pen(self.left_color, 0))
        if opt.is_horizontal():
            self.setup_painter(painter, opt.orientation, groove.center().x(),
                               groove.top(), groove.center().x(), groove.bottom())
        else:
            self.setup_painter(painter, opt.orientation, groove.left(),
                               groove.center().y(), groove.right(), groove.center().y())

        # draw groove
        intersected = core.RectF(rect.intersected(groove))
        gradient = QtGui.QLinearGradient(intersected.topLeft(), intersected.topRight())
        gradient.setColorAt(0, self.gradient_left)
        gradient.setColorAt(1, self.gradient_right)
        painter.fillRect(intersected, gradient)

    def draw_handle(self, painter, handle):
        opt = widgets.StyleOptionSlider()
        self._initStyleOption(opt, handle)
        opt.subControls = HANDLE_STYLE
        pressed = self.upper_pressed
        if handle == self.LOWER_HANDLE:
            pressed = self.lower_pressed

        if pressed == HANDLE_STYLE:
            opt.activeSubControls = pressed
            opt.state |= widgets.Style.State_Sunken
        painter.drawComplexControl(SLIDER_STYLE, opt)

    def _initStyleOption(self, option, handle):
        self.initStyleOption(option)

        option.sliderPosition = self.upper_pos
        option.sliderValue = self.upper
        if handle == self.LOWER_HANDLE:
            option.sliderPosition = self.lower_pos
            option.sliderValue = self.lower

    def handle_mouse_press(self, pos, control, value, handle):
        opt = widgets.StyleOptionSlider()
        self._initStyleOption(opt, handle)
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

    def mousePressEvent(self, event):
        if self.minimum() == self.maximum() or event.buttons() ^ event.button():
            event.ignore()
            return

        self.upper_pressed = self.handle_mouse_press(event.pos(),
                                                     self.upper_pressed,
                                                     self.upper,
                                                     self.UPPER_HANDLE)
        if self.upper_pressed != HANDLE_STYLE:
            self.lower_pressed = self.handle_mouse_press(event.pos(),
                                                         self.lower_pressed,
                                                         self.lower,
                                                         self.LOWER_HANDLE)

        self.first_movement = True
        event.accept()

    def mouseMoveEvent(self, event):
        if (self.lower_pressed != HANDLE_STYLE and
                self.upper_pressed != HANDLE_STYLE):
            event.ignore()
            return

        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)
        m = self.style().pixelMetric(widgets.Style.PM_MaximumDragDistance, opt, self)
        new_pos = self.pixel_pos_to_value(self.pick(event.pos()) - self.offset)
        if m >= 0:
            r = self.rect().adjusted(-m, -m, m, m)
            if not r.contains(event.pos()):
                new_pos = self.position

        # pick the preferred handle on the first movement
        if self.first_movement:
            if self.lower == self.upper:
                if new_pos < self.lower_value:
                    self.swap_controls()
                    self.first_movement = False
            else:
                self.first_movement = False

        if self.lower_pressed == HANDLE_STYLE:
            if self.movement == "no_crossing":
                new_pos = min(new_pos, self.upper)
            elif self.movement == "no_overlap":
                new_pos = min(new_pos, self.upper - 1)

            if self.movement == "free" and new_pos > self.upper:
                self.swap_controls()
                self.set_upper_pos(new_pos)
            else:
                self.set_lower_pos(new_pos)
        elif self.upper_pressed == HANDLE_STYLE:
            if self.movement == "no_crossing":
                new_pos = max(new_pos, self.lower_value)
            elif self.movement == "no_overlap":
                new_pos = max(new_pos, self.lower_value + 1)

            if self.movement == "free" and new_pos < self.lower:
                self.swap_controls()
                self.set_lower_pos(new_pos)
            else:
                self.set_upper_pos(new_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setSliderDown(False)
        self.lower_pressed = widgets.Style.SC_None
        self.upper_pressed = widgets.Style.SC_None
        self.update()

    def pixel_pos_to_value(self, pos):
        opt = widgets.StyleOptionSlider()
        self.initStyleOption(opt)

        slider_min = 0
        slider_max = 0
        len_slider = 0
        gr = self.style().subControlRect(SLIDER_STYLE, opt, GROOVE_STYLE, self)
        sr = self.style().subControlRect(SLIDER_STYLE, opt, HANDLE_STYLE, self)
        if self.is_horizontal():
            len_slider = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - len_slider + 1
        else:
            len_slider = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - len_slider + 1

        return widgets.Style.sliderValueFromPosition(self.minimum(),
                                                     self.maximum(),
                                                     pos - slider_min,
                                                     slider_max - slider_min,
                                                     opt.upsideDown)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    slider = SpanSlider()
    slider.set_span(30, 70)
    slider.setRange(0, 100)
    color = gui.Color("blue").lighter(150)
    slider.set_left_color(color)
    slider.set_right_color(color)
    slider.show()
    app.exec_()

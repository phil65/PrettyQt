"""The MIT License (MIT).

Copyright (c) 2012-2014 Alexander Turkin
Copyright (c) 2014 William Hallatt
Copyright (c) 2015 Jacob Dawid
Copyright (c) 2016 Luca Weiss
Copyright (c) 2017 Philipp Temminghoff

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import math

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import colors, types


class BaseWaitingSpinner(widgets.Widget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        modality: constants.ModalityStr = "none",
    ):
        super().__init__(parent=parent)

        # WAS IN initialize()
        self._color = self.get_palette().get_color("text")
        self._roundness = 100.0
        self._minimum_trail_opacity = 3.14159265358979323846
        self._trail_fade_percentage = 80.0
        self._revolutions_per_second = 1.57079632679489661923
        self._line_num = 20
        self._line_length = 10
        self._line_width = 2
        self._inner_radius = 10
        self._current_counter = 0
        self._timer = core.Timer(self)
        self._timer.timeout.connect(self._rotate)
        self._update_size()
        self._update_timer()
        self.hide()
        # END initialize()

        self.set_modality(modality)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = gui.Painter(self)
        painter.fill_rect(self.rect(), "transparent")
        painter.use_antialiasing()

        if self._current_counter >= self._line_num:
            self._current_counter = 0

        painter.set_pen(style="none")
        painter.translate(
            self._inner_radius + self._line_length, self._inner_radius + self._line_length
        )
        rect = core.RectF(0, -self._line_width / 2, self._line_length, self._line_width)
        for i in range(self._line_num):
            with painter.backup_state():
                rotate_angle = 360 * i / self._line_num
                painter.rotate(rotate_angle)
                painter.translate(self._inner_radius, 0)
                distance = self.linecount_distance_from_primary(
                    i, self._current_counter, self._line_num
                )
                color = self._current_line_color(
                    distance,
                    self._line_num,
                    self._trail_fade_percentage,
                    self._minimum_trail_opacity,
                    self._color,
                )
                painter.setBrush(color)
                painter.drawRoundedRect(
                    rect,
                    self._roundness,
                    self._roundness,
                    QtCore.Qt.SizeMode.RelativeSize,
                )

    def start(self):
        self.show()
        if not self._timer.isActive():
            self._timer.start()
            self._current_counter = 0

    def stop(self):
        self.hide()
        if self._timer.isActive():
            self._timer.stop()
            self._current_counter = 0

    def set_line_num(self, lines: int):
        self._line_num = lines
        self._current_counter = 0
        self._update_timer()

    def set_line_length(self, length: int):
        self._line_length = length
        self._update_size()

    def set_line_width(self, width: int):
        self._line_width = width

    def set_inner_radius(self, radius: int):
        self._inner_radius = radius
        self._update_size()

    def color(self) -> gui.Color:
        return self._color

    def roundness(self) -> float:
        return self._roundness

    def minimum_trail_opacity(self) -> float:
        return self._minimum_trail_opacity

    def trail_fade_percentage(self) -> float:
        return self._trail_fade_percentage

    def revolutions_per_second(self) -> float:
        return self._revolutions_per_second

    def line_num(self) -> int:
        return self._line_num

    def line_length(self) -> int:
        return self._line_length

    def line_width(self) -> int:
        return self._line_width

    def inner_radius(self) -> int:
        return self._inner_radius

    def is_spinning(self) -> bool:
        return self._timer.isActive()

    def set_roundness(self, roundness: float):
        self._roundness = max(0.0, min(100.0, roundness))

    def set_color(self, color: types.ColorType = "black"):
        self._color = colors.get_color(color)

    def set_revolutions_per_second(self, _revolutions_per_second: float):
        self._revolutions_per_second = _revolutions_per_second
        self._update_timer()

    def set_trail_fade_percentage(self, trail: float):
        self._trail_fade_percentage = trail

    def set_minimum_trail_opacity(self, minimum_trail_opacity: float):
        self._minimum_trail_opacity = minimum_trail_opacity

    def _rotate(self):
        self._current_counter += 1
        if self._current_counter >= self._line_num:
            self._current_counter = 0
        self.update()

    def _update_size(self):
        size = (self._inner_radius + self._line_length) * 2
        self.setFixedSize(size, size)

    def _update_timer(self):
        divider = int(self._line_num * self._revolutions_per_second)
        self._timer.setInterval(1000 // divider)

    def linecount_distance_from_primary(
        self, current: int, primary: int, total_lines: int
    ) -> int:
        distance = primary - current
        if distance < 0:
            distance += total_lines
        return distance

    def _current_line_color(
        self,
        count_distance: int,
        total_lines: int,
        fade_perc: float,
        min_opacity: float,
        color: gui.Color,
    ) -> gui.Color:
        color = gui.Color(color)
        if count_distance == 0:
            return color
        min_alpha_f = min_opacity / 100
        dist_threshold = int(math.ceil((total_lines - 1) * fade_perc / 100))
        if count_distance > dist_threshold:
            color.setAlphaF(min_alpha_f)
        else:
            alpha = color.alphaF()
            alpha_diff = alpha - min_alpha_f
            gradient = alpha_diff / (dist_threshold + 1)
            result_alpha = alpha - gradient * count_distance
            # If alpha is out of bounds, clip it.
            result_alpha = min(1.0, max(0.0, result_alpha))
            color.setAlphaF(result_alpha)
        return color


class WaitingSpinner(BaseWaitingSpinner):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        center_on_parent: bool = True,
        disable_parent: bool = True,
        modality: constants.ModalityStr = "none",
        additional_disabled=None,
    ):
        super().__init__(parent=parent, modality=modality)
        self._center_on_parent = center_on_parent
        self._disable_parent = disable_parent
        self.additional_disabled = additional_disabled if additional_disabled else []

    def paintEvent(self, event):
        self._update_position()
        super().paintEvent(event)

    def start(self):
        self._update_position()
        super().start()
        if self.parentWidget and self._disable_parent:
            self.parentWidget().setEnabled(False)
            for item in self.additional_disabled:
                item.setEnabled(False)

    def stop(self):
        super().stop()
        if self.parentWidget() and self._disable_parent:
            self.parentWidget().setEnabled(True)
            for item in self.additional_disabled:
                item.setEnabled(True)

    def _update_position(self):
        parent = self.parentWidget()
        if parent and self._center_on_parent:
            self.move(
                parent.width() // 2 - self.width() // 2,
                parent.height() // 2 - self.height() // 2,
            )


if __name__ == "__main__":
    app = widgets.app()
    # app.set_theme("dark")
    mainwindow = widgets.MainWindow()
    spinner = WaitingSpinner(mainwindow)
    mainwindow.show()
    spinner.start()
    app.main_loop()

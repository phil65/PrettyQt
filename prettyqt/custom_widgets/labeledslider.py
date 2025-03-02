# credits to https://stackoverflow.com/a/54819051

from __future__ import annotations

from collections.abc import Sequence

from prettyqt import constants, core, gui, widgets


class LabeledSlider(widgets.Widget):
    value_changed = core.Signal(str)

    def __init__(
        self,
        labels: Sequence[str],
        orientation: constants.OrientationStr | constants.Orientation = "horizontal",
        parent: widgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        if not isinstance(labels, Sequence):
            msg = "<labels> must be a sequence."
            raise TypeError(msg)
        self.levels = labels
        orientation = constants.ORIENTATION.get_enum_value(orientation)
        self.set_layout(constants.ORIENTATION.inverse[orientation], margin=10)

        # gives some space to print labels
        self.left_margin = 10
        self.top_margin = 10
        self.right_margin = 10
        self.bottom_margin = 10

        self.sl = widgets.Slider(
            orientation,
            tick_interval=1,
            single_step=1,
            minimum=0,
            maximum=len(self.levels) - 1,
            value=0,
        )
        self.sl.value_changed.connect(self._on_value_change)
        if orientation == constants.HORIZONTAL:
            self.sl.set_tick_position("below")
            self.sl.setMinimumWidth(300)
        else:
            self.sl.set_tick_position("left")
            self.sl.setMinimumHeight(300)

        self.box.add(self.sl)

    def _on_value_change(self, value: int):
        self.value_changed.emit(self.levels[value])

    def paintEvent(self, e):
        super().paintEvent(e)

        style = self.sl.style()
        st_slider = widgets.StyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation = self.sl.orientation()

        length = style.pixelMetric(
            widgets.Style.PixelMetric.PM_SliderLength, st_slider, self.sl
        )
        available = style.pixelMetric(
            widgets.Style.PixelMetric.PM_SliderSpaceAvailable, st_slider, self.sl
        )

        with gui.Painter(self) as painter:
            for v, v_str in enumerate(self.levels):
                # get the size of the label
                rect = painter.get_text_rect(v_str)

                if self.sl.is_horizontal():
                    x_loc = widgets.Style.sliderPositionFromValue(
                        self.sl.minimum(), self.sl.maximum(), v, available
                    )
                    # I assume the offset is half the length of slider, therefore
                    # + length//2
                    x_loc += length // 2

                    # left bound of the text = center - half of text width + L_margin
                    left = x_loc - rect.width() // 2 + self.left_margin
                    bottom = self.rect().bottom()
                    # enlarge margins if clipping
                    if v == self.sl.minimum():
                        if left <= 0:
                            self.left_margin = rect.width() // 2 - x_loc
                        self.bottom_margin = max(self.bottom_margin, rect.height())
                        self.adjust_margins()
                    if v == self.sl.maximum() and rect.width() // 2 >= self.right_margin:
                        self.right_margin = rect.width() // 2
                        self.adjust_margins()
                else:
                    y_loc = widgets.Style.sliderPositionFromValue(
                        self.sl.minimum(),
                        self.sl.maximum(),
                        v,
                        available,
                        upsideDown=True,
                    )

                    bottom = (
                        y_loc + length // 2 + rect.height() // 2 + self.top_margin - 3
                    )
                    # there is a 3 px offset that I can't attribute to any metric

                    left = self.left_margin - rect.width()
                    if left <= 0:
                        self.left_margin = rect.width() + 2
                        self.adjust_margins()
                painter.drawText(left, bottom, v_str)

    @classmethod
    def setup_example(cls):
        return cls(labels=["a", "b", "c"])

    def adjust_margins(self):
        self.box.setContentsMargins(
            self.left_margin,
            self.top_margin,
            self.right_margin,
            self.bottom_margin,
        )


if __name__ == "__main__":
    app = widgets.app()
    frame = widgets.Widget()
    ha = widgets.HBoxLayout()
    frame.setLayout(ha)

    w = LabeledSlider(labels=["test", "test2", "test3"], orientation="vertical")
    w.value_changed.connect(print)
    ha.addWidget(w)
    frame.show()
    app.exec()

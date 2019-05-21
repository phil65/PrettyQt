# -*- coding: utf-8 -*-

# credits to https://stackoverflow.com/a/54819051

from prettyqt import widgets, core, gui

from qtpy import QtCore


class LabeledSlider(widgets.Widget):

    value_changed = core.Signal(int)

    def __init__(self, labels, orientation=QtCore.Qt.Horizontal, parent=None):
        super().__init__(parent=parent)

        levels = range(len(labels))
        if not isinstance(labels, (tuple, list)):
            raise Exception("<labels> is a list or tuple.")
        self.levels = list(zip(levels, labels))

        if orientation == QtCore.Qt.Horizontal:
            self.layout = widgets.BoxLayout("vertical", self)
        elif orientation == QtCore.Qt.Vertical:
            self.layout = widgets.BoxLayout("horizontal", self)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin = 10
        self.top_margin = 10
        self.right_margin = 10
        self.bottom_margin = 10

        self.layout.setContentsMargins(self.left_margin, self.top_margin,
                                       self.right_margin, self.bottom_margin)

        self.sl = widgets.Slider(orientation, self)
        self.sl.value_changed.connect(self.value_changed)
        self.sl.setMinimum(0)
        self.sl.setMaximum(len(labels) - 1)
        self.sl.setValue(0)
        if orientation == QtCore.Qt.Horizontal:
            self.sl.setTickPosition(widgets.Slider.TicksBelow)
            self.sl.setMinimumWidth(300)  # just to make it easier to read
        else:
            self.sl.setTickPosition(widgets.Slider.TicksLeft)
            self.sl.setMinimumHeight(300)  # just to make it easier to read
        self.sl.setTickInterval(1)
        self.sl.setSingleStep(1)

        self.layout.addWidget(self.sl)

    def paintEvent(self, e):

        super().paintEvent(e)

        style = self.sl.style()
        painter = gui.Painter(self)
        st_slider = widgets.StyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation = self.sl.orientation()

        length = style.pixelMetric(widgets.Style.PM_SliderLength, st_slider, self.sl)
        available = style.pixelMetric(
            widgets.Style.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:

            # get the size of the label
            rect = painter.drawText(core.Rect(), QtCore.Qt.TextDontPrint, v_str)

            if self.sl.orientation() == QtCore.Qt.Horizontal:
                x_loc = widgets.Style.sliderPositionFromValue(self.sl.minimum(),
                                                              self.sl.maximum(),
                                                              v,
                                                              available)
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
                    if self.bottom_margin <= rect.height():
                        self.bottom_margin = rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

                if v == self.sl.maximum() and rect.width() // 2 >= self.right_margin:
                    self.right_margin = rect.width() // 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            else:
                y_loc = widgets.Style.sliderPositionFromValue(self.sl.minimum(),
                                                              self.sl.maximum(),
                                                              v,
                                                              available,
                                                              upsideDown=True)

                bottom = y_loc + length // 2 + rect.height() // 2 + self.top_margin - 3
                # there is a 3 px offset that I can't attribute to any metric

                left = self.left_margin - rect.width()
                if left <= 0:
                    self.left_margin = rect.width() + 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            pos = core.Point(left, bottom)
            painter.drawText(pos, v_str)

        return


if __name__ == '__main__':
    app = widgets.Application([])
    frame = widgets.Widget()
    ha = widgets.BoxLayout("horizontal")
    frame.setLayout(ha)

    w = LabeledSlider(labels=["test", "test2", "test3"], orientation=QtCore.Qt.Vertical)

    ha.addWidget(w)
    frame.show()
    app.exec_()

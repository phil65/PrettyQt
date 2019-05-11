# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets
from qtpy.QtCharts import QtCharts

from prettyqt import charts, core, gui, widgets

ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                  right=QtCore.Qt.AlignRight,
                  top=QtCore.Qt.AlignTop,
                  bottom=QtCore.Qt.AlignBottom)

ZOOM_IN_FACTOR = 1.1
ZOOM_OUT_FACTOR = 1.0 / ZOOM_IN_FACTOR
SCROLL_STEP_SIZE = 10


class ChartView(QtCharts.QChartView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chart = charts.Chart()
        self.setChart(chart)
        self.setRenderHint(gui.Painter.Antialiasing)
        self.setRubberBand(self.RectangleRubberBand)
        # self.setDragMode(self.RubberBandDrag)

    def keyPressEvent(self, event):
        """
        handle keypress events to allow navigation via keyboard
        """
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.chart().zoomReset()
        elif key == QtCore.Qt.Key_Plus:
            self.chart().zoom_by_factor(ZOOM_IN_FACTOR)
        elif key == QtCore.Qt.Key_Minus:
            self.chart().zoom_by_factor(ZOOM_OUT_FACTOR)
        elif key == QtCore.Qt.Key_Left:
            self.chart().scroll(-SCROLL_STEP_SIZE, 0)
        elif key == QtCore.Qt.Key_Right:
            self.chart().scroll(SCROLL_STEP_SIZE, 0)
        elif key == QtCore.Qt.Key_Up:
            self.chart().scroll(0, SCROLL_STEP_SIZE)
        elif key == QtCore.Qt.Key_Down:
            self.chart().scroll(0, -SCROLL_STEP_SIZE)
        elif key == QtCore.Qt.Key_0:
            self.chart().apply_nice_numbers()
        else:
            return super().keyPressEvent(event)
        event.accept()

    def wheelEvent(self, event):
        """
        handle wheel event for zooming
        """
        fct = ZOOM_IN_FACTOR if event.angleDelta().y() > 0 else ZOOM_OUT_FACTOR
        self.chart().zoom_by_factor(fct)

    def mouseReleaseEvent(self, event):
        """
        override to allow dragging the chart
        """
        if event.button() == QtCore.Qt.RightButton:
            widgets.Application.restoreOverrideCursor()
            event.accept()
            return None
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        """
        override to allow dragging the chart
        """
        if event.button() == QtCore.Qt.RightButton:
            cursor = gui.Cursor(QtCore.Qt.SizeAllCursor)
            widgets.Application.setOverrideCursor(cursor)
            self.last_mouse_pos = event.pos()
            event.accept()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        override to allow dragging the chart
        """
        # pan the chart with a middle mouse drag
        if event.buttons() & QtCore.Qt.RightButton:
            if not self.last_mouse_pos:
                return None
            pos_diff = event.pos() - self.last_mouse_pos
            self.chart().scroll(-pos_diff.x(), pos_diff.y())

            self.last_mouse_pos = event.pos()
            event.accept()

            widgets.Application.restoreOverrideCursor()

        super().mouseMoveEvent(event)

    def get_image(self):
        image = self.grab()
        gl_widget = self.findChild(QtWidgets.QOpenGLWidget)
        if gl_widget:
            painter = gui.Painter(image)
            d = gl_widget.mapToGlobal(core.Point()) - self.mapToGlobal(core.Point())
            painter.set_composition_mode("source_at_top")
            painter.drawImage(d, gl_widget.grabFramebuffer())
            painter.end()
        return image

    # def hide_legend(self):
    #     self.chart().hide_legend()

    # def show_legend(self):
    #     self.chart().show_legend()

    # def set_legend_alignment(self, alignment: str):
    #     if alignment not in ALIGNMENTS:
    #         raise ValueError(f"{alignment} not a valid alignment.")
    #     self.chart().legend().setAlignment(ALIGNMENTS[alignment])

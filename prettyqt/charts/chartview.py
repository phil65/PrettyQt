# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from qtpy.QtCharts import QtCharts

from prettyqt import core, gui


class ChartView(QtCharts.QChartView):

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

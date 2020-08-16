# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui


QtGui.QLinearGradient.__bases__ = (gui.Gradient,)


class LinearGradient(QtGui.QLinearGradient):
    def serialize_fields(self):
        start = self.start()
        final_stop = self.finalStop()
        return dict(start=(start[0], start[1]), final_stop=(final_stop[0], final_stop[1]))

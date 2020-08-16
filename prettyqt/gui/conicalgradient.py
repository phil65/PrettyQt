# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui


QtGui.QConicalGradient.__bases__ = (gui.Gradient,)


class ConicalGradient(QtGui.QConicalGradient):
    def serialize_fields(self):
        center = self.center()
        return dict(angle=self.angle(), center=(center[0], center[1]))

# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui


QtGui.QRadialGradient.__bases__ = (gui.Gradient,)


class RadialGradient(QtGui.QRadialGradient):
    def serialize_fields(self):
        center = self.center()
        focal_point = self.focalPoint()
        return dict(
            center_radius=self.centerRadius(),
            radius=self.radius(),
            focal_radius=self.focalRadius(),
            center=(center[0], center[1]),
            focal_point=(focal_point[0], focal_point[1]),
        )

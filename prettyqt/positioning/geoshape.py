# -*- coding: utf-8 -*-

try:
    from PySide2 import QtPositioning
except ImportError:
    from PyQt5 import QtPositioning


class GeoShape(QtPositioning.QGeoShape):
    def __contains__(self, other: QtPositioning.QGeoCoordinate):
        return self.contains(other)

    def __str__(self):
        return self.toString()[1:]

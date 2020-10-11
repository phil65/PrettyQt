# -*- coding: utf-8 -*-

try:
    from PySide2 import QtPositioning
except ImportError:
    from PyQt5 import QtPositioning


class GeoAddress(QtPositioning.QGeoAddress):
    def __str__(self):
        return self.text()

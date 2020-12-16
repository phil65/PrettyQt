from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning


class GeoAddress(QtPositioning.QGeoAddress):
    def __str__(self):
        return self.text()

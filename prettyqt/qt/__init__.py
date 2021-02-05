"""Provides Qt init stuff."""

import os


class PythonQtError(ImportError):
    pass


os.environ.setdefault("QT_API", "pyqt5")

API = os.environ["QT_API"].lower()

PYQT5 = API == "pyqt5"
PYQT6 = API == "pyqt6"
PYSIDE2 = API == "pyside2"
PYSIDE6 = API == "pyside6"

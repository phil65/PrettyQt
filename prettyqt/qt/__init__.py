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

if API == "pyqt5":
    from PyQt5.QtCore import QT_VERSION_STR as QT_VERSION
elif API == "pyqt6":
    from PyQt6.QtCore import QT_VERSION_STR as QT_VERSION
elif API == "pyside2":
    from PySide2.QtCore import __version__ as QT_VERSION  # type: ignore
elif API == "pyside6":
    from PySide6.QtCore import __version__ as QT_VERSION  # type: ignore

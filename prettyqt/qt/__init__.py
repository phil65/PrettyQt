"""Provides Qt init stuff."""

import os


class PythonQtError(ImportError):
    pass


os.environ.setdefault("QT_API", "pyqt5")

API = os.environ["QT_API"].lower()

PYQT5 = API == "pyqt5"
PYSIDE2 = API == "pyside2"

if API == "pyqt5":
    from PyQt5.QtCore import QT_VERSION_STR as QT_VERSION
else:
    from PySide2.QtCore import __version__ as QT_VERSION  # type: ignore

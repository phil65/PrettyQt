"""Provides QtWebEngineWidgets classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    from PyQt5.QtWebEngineWidgets import *
elif PYSIDE2:
    from PySide2.QtWebEngineWidgets import *
else:
    raise PythonQtError("No Qt bindings could be found")

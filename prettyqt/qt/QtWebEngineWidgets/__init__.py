"""Provides QtWebEngineWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtWebEngineWidgets import *
elif PYSIDE6:
    from PySide6.QtWebEngineWidgets import *
else:
    raise PythonQtError("No Qt bindings could be found")

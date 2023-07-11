"""Provides QtWebEngineCore classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYSIDE6:
    from PySide6.QtWebChannel import *
elif PYQT6:
    from PyQt6.QtWebChannel import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")

"""Provides QtPositioning classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYSIDE6:
    from PySide6.QtPositioning import *
elif PYQT6:
    from PyQt6.QtPositioning import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")

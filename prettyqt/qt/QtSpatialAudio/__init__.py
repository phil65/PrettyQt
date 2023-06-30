"""Provides QtSpatialAudio classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtSpatialAudio import *
elif PYSIDE6:
    from PySide6.QtSpatialAudio import *
else:
    raise PythonQtError("No Qt bindings could be found")

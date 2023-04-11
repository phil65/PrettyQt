"""Provides QtMultimediaWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtMultimediaWidgets import *
elif PYSIDE6:
    from PySide6.QtMultimediaWidgets import *
else:
    raise PythonQtError("No Qt bindings could be found")

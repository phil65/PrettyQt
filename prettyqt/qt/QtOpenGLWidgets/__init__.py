"""Provides QtOpenGLWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    from PyQt6.QtOpenGLWidgets import *
elif PYSIDE6:
    from PySide6.QtOpenGLWidgets import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")

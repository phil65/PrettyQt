"""Provides QtPdfWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    from PyQt6.QtPdfWidgets import *
elif PYSIDE6:
    from PySide6.QtPdfWidgets import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
